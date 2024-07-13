# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# IMAGE_PATH = "asset/elephant_in_room.jpeg"
# display(Image(IMAGE_PATH))
# Test code, the comment need to be kept for later use
'''completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": "You are a helpful assistant. Help me with my math homework!"}, # <-- This is the system message that provides context to the model
    {"role": "user", "content": "Hello! Could you solve 2+2?"}  # <-- This is the user message for which the model will generate a response
  ]
)'''

# Open the image file and encode it as a base64 string
'''def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)
'''

# Request the model to describe the scene and objects in the image
'''response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful image analysis assistant that can accurately describe the scene and objects in the image."},
        {"role": "user", "content": [
            {"type": "text", "text": "Please describe the scene and objects in this image."},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}
            }
        ]}
    ],
    temperature=0.0,
)

print(response.choices[0].message.content)
# print("Assistant: " + completion.choices[0].message.content)'''