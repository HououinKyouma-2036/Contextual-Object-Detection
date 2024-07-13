from openai import OpenAI 
import os
from io import BytesIO
from dotenv import load_dotenv
from IPython.display import Image, display, Audio, Markdown
import base64
import asyncio


# Load environment variables from .env file, and set the model
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL="gpt-4o"

async def describe_image(img):
    buffer = BytesIO()
    img.save(buffer, format='JPEG')  #  adjust format if necessary
    base64image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "\
             You are a helpful image analysis expert that can accurately recognize the scene and detect objects in the image. \
             The image is preprocessed using a matrix mask with a red matrix coordinate label on each grid. \
             The number labels (number1, number2) are used to help you identify the matrix grid that contains the object of interest. "},
            {"role": "user", "content": [
                {"type": "text", "text": "Please list all objects in the scene that are out of place with reasoning in the following list format: \
                  1. noun_1, reasoning_1 2. noun_2, reasoning_2 ... n. noun_n, reasoning_n with each noun being the best word to describe the object. \
                 For instance, 1. car, does not belong in the kitchen 2. bowling ball, should not be cooked on a frying pan 3. toothbrush, typically stored in the bathroom. \
                  \
                 Then, accurately report me the corresponding matrix coordinate covering the corresponding out of place object. Follow the is format: \
                 object_name1, (x_1, y_2), object_name2, (x_2, y_2), ... object_name_n, (x_n, y_n) \
                 Example: car, (1, 2), toothbrush, (3, 4), bowling ball, (5, 6)"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64image}"}
                }
            ]}
        ],
        temperature=0.1,
    )
    
    return response.choices[0].message.content





