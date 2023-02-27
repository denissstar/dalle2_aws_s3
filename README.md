<h1 align="center"> 📸 dalle2_python 🏞 </h1>

<p align="center">
   Generating stunning images from the command line.
</p>

This is a simple working example on how to integrate the DALLE2 API into your own Python project and create amazing images directly from the command line.
Now with AWS S3 integration!

## How it works
Reads a string from the command line in natural language and creates an input prompt which is then fed to OpenAIs DALLE2. The response contains urls to the generated images. The images are downloaded and stored in an output folder.
To generate your own images you need to get access to the DALLE2 API (https://openai.com/dall-e-2/).

## Installation
For best practices install requirements in activated virtualenv
```bash
git clone git@github.com:denissstar/dalle2_aws_s3.git
cd dalle2_aws_s3
pip3 install -r requirements.txt
```

Update `self._s3_bucket` variable with your S3 bucket name

## Run example
```
python3 dalle2_python.py
What image should dalle create: Cats do cloud engineering, by Banksy (Street Art)
Generated images stored in: ./output/*.png
Generated images uploaded to S3 bucket with same key name as the filename
```
Now check the output folder:
<p float="left">
<img src="/output/Cats do cloud engineering, by Banksy (Street Art)_0.png" alt="example_of_prompt_in_terminal" width="200"/>
<img src="/output/Cats do cloud engineering, by Salvador Dali_1.png" alt="example_of_prompt_in_terminal" width="200"/>
</p>

Enjoy!
