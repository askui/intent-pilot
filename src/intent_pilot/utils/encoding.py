import base64

def encode_string(input_str: str):
    return base64.b64encode(input_str.encode("utf-8")).decode("utf-8")

def encode_image(image_file: str):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string