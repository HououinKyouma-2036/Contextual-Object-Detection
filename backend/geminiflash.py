import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
from PIL import Image
import io

load_dotenv()
## Set the API key and model name
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def describe_image(image):
    prompt = "Please list all objects in the scene that are out of place with reasoning in the following list format: 1. noun_1, reasoning_1 2. noun_2, reasoning_2 ... n. noun_n, reasoning_n with each noun being the best word to describe the object. For instance, 1. car, does not belong in the kitchen 2. bowling ball, should not be cooked on a frying pan 3. toothbrush, typically stored in the bathroom. Then, report me the corresponding matrix coordinate of the corresponding out of place object."
    response = model.generate_content([prompt, image], stream=True)
    response.resolve()
    # print(response.candidates[0].content.parts[0].text)
    return response.candidates[0].content.parts[0].text


# Open the image file and encode it as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# IMAGE_PATH = "asset/elephant_in_room.jpeg"
# base64_image = encode_image(IMAGE_PATH)
# describe_image(base64_image)