import os
import configparser
import logging
import requests
import sys
import webbrowser
import urllib.request

import boto3
from botocore.exceptions import ClientError
import openai

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# based on https://github.com/alxschwrz/dalle2_python/blob/main/dalle2_python.py
class Dalle:
    def __init__(self, img_sz="512", n_images=2):
        self._api_keys_location = "./config"
        self._generated_image_location = "./output"
        self._s3_bucket = "dalle2-image-bucket"
        self._stream = True
        self._img_sz = img_sz
        self._n_images = n_images
        self._image_urls = []
        self._input_prompt = None
        self._response = None
        self.initialize_openai_api()

    def create_template_ini_file(self):
        """
        If the ini file does not exist create it and add the organization_id and
        secret_key
        """
        if not os.path.isfile(self._api_keys_location):
            with open(self._api_keys_location, "w") as f:
                f.write("[openai]\n")
                f.write("organization_id=\n")
                f.write("secret_key=\n")

            print(f"""OpenAI API config file created at {self._api_keys_location}
                Please edit it and add your organization ID and secret key
                If you do not yet have an organization ID and secret key, you\n
                need to register for OpenAI Codex: \n
                https://openai.com/blog/openai-codex/""")
            sys.exit(1)


    def initialize_openai_api(self):
        """
        Initialize the OpenAI API
        """
        # Check if file at API_KEYS_LOCATION exists
        self.create_template_ini_file()
        config = configparser.ConfigParser()
        config.read(self._api_keys_location)

        openai.organization_id = config["openai"]["organization_id"].strip('"').strip("'")
        openai.api_key = config["openai"]["secret_key"].strip('"').strip("'")
        del config

    def read_from_command_line(self):
        self._input_prompt = input("What image should dalle create: ")

    def generate_image_from_prompt(self):
        self._response = openai.Image.create(
            prompt=self._input_prompt,
            n=self._n_images,
            size=f"{self._img_sz}x{self._img_sz}",
        )
        
    def get_urls_from_response(self):
        for i in range(self._n_images):
            self._image_urls.append(self._response["data"][i]["url"])

    def open_urls_in_browser(self, image_urls=None):
        if image_urls is None:
            image_urls = self._image_urls
        for url in image_urls:
            webbrowser.open(url)

    def save_urls_as_image(self):
        if not os.path.isdir(self._generated_image_location):
            os.mkdir(self._generated_image_location)
        for idx, image_url in enumerate(self._image_urls):
            file_name = os.path.join(self._generated_image_location, f"{self._input_prompt}_{idx}.png")
            urllib.request.urlretrieve(image_url, file_name)
            logger.info(f"Generated image stored in: {file_name}")
    
    def generate_and_save_images(self):
        self.read_from_command_line()
        self.generate_image_from_prompt()
        self.get_urls_from_response()
        self.save_urls_as_image()
        self.save_urls_as_s3_objects()

    def save_urls_as_s3_objects(self):
        """Upload a url object to an S3 bucket
        """
        for idx, image_url in enumerate(self._image_urls):
            r = requests.get(image_url, stream=True)
            s3_client = boto3.client("s3")
            s3_object_name = f"{self._input_prompt}_{idx}.png"
            try:
                s3_client.upload_fileobj(r.raw, self._s3_bucket, s3_object_name)
            except ClientError as e:
                logger.error(e)
            logger.info(f"Generated image stored in: {self._s3_bucket} as {s3_object_name}")

commandLineDalle = Dalle()
commandLineDalle.generate_and_save_images()
commandLineDalle.open_urls_in_browser()