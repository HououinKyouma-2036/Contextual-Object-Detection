from flask import Flask, request, jsonify
import gpt4o as gpt4o
import gpt4v as gpt4v
import geminiprov as geminiprov
import geminiflash as geminiflash
import llava as llava
import image_matrixization as matrixize
import base64
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask API!"

# gpt4o
@app.route('/gpt4o', methods=['POST'])
def ask_gpt4o():
    base64img = request.get_data(as_text=True)
    image_bytes = base64.b64decode(str(base64img))
    img = Image.open(io.BytesIO(image_bytes))
    matrixized_img = matrixize.process_image(img)
    # b64_matrixized_img = base64.b64encode(matrixized_img)
    description, objects = gpt4o.describe_image(matrixized_img)
    centroids = matrixize.get_centroid_coordinates(objects, img)
    # center_points = matrixize.center_points(objects, img)
    return jsonify({'description': description, 'centroids': centroids})

# gpt4v
@app.route('/gpt4v', methods=['POST'])
def ask_gpt4v():
    base64img = request.get_data(as_text=True)
    image_bytes = base64.b64decode(str(base64img))
    img = Image.open(io.BytesIO(image_bytes))
    matrixized_img = matrixize.process_image(img)
    # b64_matrixized_img = base64.b64encode(matrixized_img)
    description, objects = gpt4v.describe_image(matrixized_img)
    centroids = matrixize.get_centroid_coordinates(objects, img)
    #center_points = matrixize.center_points(objects, img)
    return jsonify({'description': description, 'centroids': centroids})


# gemini pro vision
@app.route('/geminiprov', methods=['POST'])
def ask_geminiprov():
    base64img = request.get_data(as_text=True)
    image_bytes = base64.b64decode(str(base64img))
    img = Image.open(io.BytesIO(image_bytes))
    matrixized_img = matrixize.process_image(img)

    description = geminiprov.describe_image(matrixized_img)
    return jsonify({'response': description})

# gemini flash
@app.route('/geminiflash', methods=['POST'])
def ask_geminiflash():
    base64img = request.get_data(as_text=True)
    image_bytes = base64.b64decode(str(base64img))
    img = Image.open(io.BytesIO(image_bytes))
    matrixized_img = matrixize.process_image(img)

    description = geminiflash.describe_image(matrixized_img)
    return jsonify({'response': description})

# Llava
# @app.route('/llava', methods=['POST'])
# def ask_llava():
#     base64img = request.get_data(as_text=True)
#     description = llava.describe_image(base64img)
#     return jsonify({'response': description})

if __name__ == '__main__':
    app.run(debug=True)

