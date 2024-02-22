import re
from pathlib import Path

from fuzzywuzzy import process
from PIL import Image, ImageDraw, ImageFont

ARIAL_FONT_PATH = Path(__file__).parent / "font_assets" / "arial.ttf"


def open_pil_image(image_file):
    image = Image.open(image_file).convert("RGB")
    return image


def save_pil_image(image, filename="uploaded_image.png"):
    image.save(filename)
    return filename


def draw_bboxes(image, label_coordinates, font_style=ARIAL_FONT_PATH, font_size=20):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(
        font_style, font_size
    )  # Load a font of size 15 for 1024x768 images. Adjust as needed.

    for idx in label_coordinates:
        bbox = label_coordinates[idx]
        xmin = int(bbox["xmin"])
        ymin = int(bbox["ymin"])
        xmax = int(bbox["xmax"])
        ymax = int(bbox["ymax"])

        area_of_rectangle = (xmax - xmin) * (ymax - ymin)
        if area_of_rectangle < 100:
            continue
        # Draw the bounding box
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=3)

        # Draw the number with a background
        num_str = str(idx)

        # Using textbbox to calculate the bounding box of the text
        left, top, right, bottom = draw.textbbox((0, 0), num_str, font=font)
        text_width = right - left
        text_height = bottom - top

        draw.rectangle(
            [(xmin, ymin - text_height), (xmin + text_width, ymin + 5)], fill="black"
        )
        draw.text((xmin, ymin - text_height), num_str, font=font, fill="white")
    return image


def draw_transparent_bboxes(image, data):
    """
    Draws transparent bounding boxes on the image.
    """
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))  # Transparent overlay
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
    combined = Image.alpha_composite(image.convert("RGBA"), overlay)
    return combined.convert("RGB")


def extract_numbers(sentence):
    pattern = r"\d+"  # Match one or more digits
    numbers = re.findall(pattern, sentence)  # Find all matches in the sentence
    numbers = [int(num) for num in numbers if num.isnumeric()]  # Convert to integers
    return numbers


def flexible_query_search(query, list_of_strings):
    match = process.extractOne(query, list_of_strings)
    return match[0]


def extract_element_bbox(query, raw_data, flexible_search=False):
    """
    Extracts the bounding box of an element based on the query from the raw data.

    Args:
        query (str): The label of the element to search for.
        raw_data (dict): The raw data containing the element labels and their corresponding bounding boxes.
        flexible_search (bool, optional): If True, performs a flexible search to find the closest matching label.
            Defaults to False.

    Returns:
        dict: The bounding box of the element.

    Raises:
        KeyError: If the element with the specified label is not found in the data and flexible_search is False.
    """
    try:
        return raw_data[query]
    except KeyError as exc:
        if flexible_search:
            closest_query = flexible_query_search(query, raw_data.keys())
            return raw_data[closest_query]
        raise KeyError(f"Element with label '{query}' not found in the data.") from exc
