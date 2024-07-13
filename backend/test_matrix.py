import gpt4o as gpt4o
import gpt4v as gpt4v
import geminiprov as geminiprov
import geminiflash as geminiflash
import llava as llava
import image_matrixization as matrixize
from image_matrixization import ObjectDetails
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv
from IPython.display import display, Audio, Markdown
import base64

IMAGE_PATH = "asset/output_image_04.jpg"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_img = encode_image(IMAGE_PATH)

image_bytes = base64.b64decode(str(base64_img))
img = Image.open(io.BytesIO(image_bytes))
matrixized_img = matrixize.process_image(img)
    # b64_matrixized_img = base64.b64encode(matrixized_img)
description, objects = gpt4o.describe_image(matrixized_img)
center_points = matrixize.center_points(objects, img)

print(description, "\n", objects, "\n", center_points)