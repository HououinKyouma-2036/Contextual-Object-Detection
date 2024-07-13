from openai import OpenAI 
import os
from dotenv import load_dotenv
from IPython.display import Image, display, Audio, Markdown
import base64

IMAGE_PATH = "../asset/output_image_04.jpg"
display(Image(IMAGE_PATH))

# Load environment variables from .env file, Set the API key and model name
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL="gpt-4o"

class ObjectDetails:
    def __init__(self, object_name, coordinates):
        self.object_name = object_name
        self.coordinates = coordinates

    def __repr__(self):
        return f"{self.object_name}: {self.coordinates}"

# Open the image file and encode it as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)

# Request the model to describe the scene and objects in the image
response = client.chat.completions.create(
    model=MODEL,
    messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful image analysis expert that can accurately recognize the scene and detect objects in the image. "
                    "The image is preprocessed using a matrix mask with a red matrix coordinate label on each grid. "
                    "The number labels (number1, number2) are used to help you identify the matrix grid that contains the object of interest."
                )
            },
            {"role": "user", "content": [
                {"type": "text", 
                 "text": "Please list all objects in the scene that are out-of-place with reasoning in the following list format: \
                  1. noun_1, reasoning_1 \
                  2. noun_2, reasoning_2 ... \
                  n. noun_n, reasoning_n with each noun being the best word to describe the object. \
                 For instance: \
                  1. car, does not belong in the kitchen \
                  2. bowling ball, should not be cooked on a frying pan \
                  3. toothbrush, typically stored in the bathroom. \
                    \n\n Then, accurately report me all the corresponding matrix coordinate covering the corresponding out-of-place object. Follow the is format: \
                 object_name1: {(x_1, y_2)#(x_2, y_2)#... }\n \
                 object_name2: {(x_1, y_1)#(x_2, y_2)# ... }\n \
                 object_name_n: {(x_1, y_1)#(x_2, y_2)# ... }\n \
                 Example: \
                car: {(1, 2)#(7,8)#(9,10)#(11,12)}\n \
                Your general response format need to be: \
                Discription: [list of all objects in the scene that are out of place with reasoning following format above] \
                Objects: [object_name1, list of coordinates]\n \
                        [object_name2, list of coordinates]\n ..."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.1,
        max_tokens=1500,
    )
full_response = response.choices[0].message.content
split_response = full_response.split('Objects:')
description_part = split_response[0].strip()
objects_part = split_response[1].strip()
# Extracting objects
objects = []
lines = objects_part.split('\n')
for line in lines:
    if ':' in line:
        object_name, coords = line.split(':')
        object_name = object_name.strip()
        coords = coords.strip().strip('{}').split('#')
        coordinates = [tuple(map(int, coord.strip().strip('()').split(','))) for coord in coords]
        objects.append(ObjectDetails(object_name, coordinates))

print(description_part)
print(objects)
