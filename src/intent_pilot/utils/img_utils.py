
from PIL import Image, ImageDraw
import json
import re
import base64
import json
import requests
import copy
import os
from PIL import ImageFont

openai_api_key = os.getenv("OPENAI_API_KEY")

def open_pil_image(image_file):
    image = Image.open(image_file).convert("RGB")
    return image

def save_pil_image(image, filename = "uploaded_image.png"):
    image.save(filename)
    return filename

def send_to_gpt(base64_image, query):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "temperature": 0.1,
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": f"Hey, imagine that you are guiding me navigating the UI elements in the provided image(s). All the UI elements are numbered for reference. The associated numbers are on top left of corresponding bbox. For the prompt/query asked, return the number associated to the target element to perform the action. query: {query}"
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()

def process_data(rawdata):
    data = copy.deepcopy(rawdata)
    newdata = {}
    newdata['detected_elements'] = []
    for element in data['data']['detected_elements']:
        # Remove 'colors' key
        if 'colors' in element:
            del element['colors']

        # Convert bbox coordinates to integers
        bbox = element['bndbox']
        for key in bbox:
            bbox[key] = int(bbox[key])

        # Convert bbox coordinates to center
        center_x = int((bbox['xmin'] + bbox['xmax']) / 2)
        center_y = int((bbox['ymin'] + bbox['ymax']) / 2)
        bbox['x'] = center_x
        bbox['y'] = center_y

        # Remove original bbox coordinates
        del bbox['xmin']
        del bbox['xmax']
        del bbox['ymin']
        del bbox['ymax']

        # convert dict to tuple
        element = [bbox['x'], bbox['y'], element['name'], element['text']]
        newdata['detected_elements'].append(element)
    return newdata

def draw_bboxes(image, data):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 20)  # Load a font of size 15 for 1024x768 images. Adjust as needed.
    
    for idx, element in enumerate(data["data"]["detected_elements"], 1):
        bbox = element["bndbox"]
        xmin = int(bbox["xmin"])
        ymin = int(bbox["ymin"])
        xmax = int(bbox["xmax"])
        ymax = int(bbox["ymax"])
        element["tagid"] = idx

        # Draw the bounding box
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="green")

        # Draw the number with a background
        num_str = str(idx)
        # text_width, text_height = draw.textsize(num_str, font=font)

        # Using textbbox to calculate the bounding box of the text
        left, top, right, bottom = draw.textbbox((0, 0), num_str, font=font)
        text_width = right - left
        text_height = bottom - top

        draw.rectangle([(xmin, ymin - text_height), (xmin + text_width, ymin+5)], fill="black")
        draw.text((xmin, ymin - text_height), num_str, font=font, fill="white")

        # For debugging, remove if not needed
        # draw.text((xmin, ymin-10-text_height), (element['name'] + "-" + element['text']).encode('utf-8'), fill="red")
    return image

def draw_transparent_bboxes(image, data):
    """
    Draws transparent bounding boxes on the image.
    """
    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))  # Transparent overlay
    draw_overlay = ImageDraw.Draw(overlay)

    for element in data["data"]["detected_elements"]:
        bbox = element["bndbox"]
        xmin = int(bbox["xmin"])
        ymin = int(bbox["ymin"])
        xmax = int(bbox["xmax"])
        ymax = int(bbox["ymax"])
        
        # Color can be changed as per requirement. Here, we're using green with 80/255 opacity.
        draw_overlay.rectangle([(xmin, ymin), (xmax, ymax)], fill=(0, 255, 0, 80))
    
    # Merge the overlay with the image
    combined = Image.alpha_composite(image.convert('RGBA'), overlay)
    return combined.convert("RGB")

def process_image(data, command, filename, rawdata):
    # Load the image
    image = Image.open(filename).convert("RGB")
    image_with_bboxes = draw_bboxes(image, rawdata)
    # Draw a red dot on the image at the given coordinates
    draw = ImageDraw.Draw(image_with_bboxes)

    return image

def extract_numbers(sentence):
    pattern = r'\d+'  # Match one or more digits
    numbers = re.findall(pattern, sentence)  # Find all matches in the sentence
    numbers = [int(num) for num in numbers if num.isnumeric()]  # Convert to integers
    return numbers


def extract_element_bbox(indices, raw_data):
    for num in indices:
        for inst in raw_data["data"]["detected_elements"]:
            if inst["tagid"] == num:
                return [inst["bndbox"]["xmin"],inst["bndbox"]["ymin"],inst["bndbox"]["xmax"],inst["bndbox"]["ymax"]]
    return -1