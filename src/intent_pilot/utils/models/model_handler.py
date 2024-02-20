import os
import time
import json
import traceback


import uuid
from pathlib import Path
from intent_pilot.utils.screenshot import (
    capture_screen_with_cursor,
)
from PIL import Image
from intent_pilot.utils.config import AskUIIntentPilotConfig
from intent_pilot.utils.img_utils import extract_element_bbox
from intent_pilot.utils.models.askui import get_labeled_image
from intent_pilot.utils.encoding import encode_image
from intent_pilot.utils.models.prompts import get_user_first_message_prompt, get_user_prompt
from intent_pilot.utils.models.gpt4 import format_gpt4v_message, get_response_from_gpt4v
config = AskUIIntentPilotConfig()

def get_relative_user_prompt(messages_len):
    if messages_len == 1:
        return get_user_first_message_prompt()
    else:
        return get_user_prompt()

def capture_screenshot_in_a_folder(screenshots_dir: Path = Path("screenshots"), unique_id: str = None):
    screenshot_filename = os.path.join(screenshots_dir, f"{unique_id}.png")
    capture_screen_with_cursor(screenshot_filename)
    return screenshot_filename

def save_labeled_pil_img_in_folder(annotated_pil_image: Image, screenshots_dir: Path = Path("screenshots"), unique_id: str = None):
    labeled_img_path = os.path.join(screenshots_dir, f"{unique_id}_labelled.png")
    annotated_pil_image.save(labeled_img_path)
    return labeled_img_path

def remove_code_block(content):
    if content.startswith("```json"):
        content = content[len("```json") :]
        if content.endswith("```"):
            content = content[: -len("```")]
    return content


def call_gpt_4_vision_preview_labeled(openai_client, messages, objective, 
                                      screenshots_dir: Path = Path("screenshots"),
                                      skip_som_draw_labels=[]):
    time.sleep(1)

    try:
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        img_id = uuid.uuid4()

        screenshot_filename = capture_screenshot_in_a_folder(screenshots_dir, img_id)
        pil_image_with_bboxes, label_coordinates =  get_labeled_image(screenshot_filename, skip_labels=skip_som_draw_labels)
        labeled_img_path = save_labeled_pil_img_in_folder(pil_image_with_bboxes, screenshots_dir, img_id)
        img_base64_labeled = encode_image(labeled_img_path)
        user_prompt = get_relative_user_prompt(len(messages))
        vision_message = format_gpt4v_message(user_prompt, img_base64_labeled)
        messages.append(vision_message)
        content = get_response_from_gpt4v(openai_client, messages, temperature=config.openai_temperature, max_tokens=config.openai_max_tokens)
        print("[Intent Pilot][call_gpt_4_vision_preview_labeled] content", content)
        content = remove_code_block(content)
        assistant_message = {"role": "assistant", "content": content}
        messages.append(assistant_message)
        content = json.loads(content)

        processed_content = merge_click_operations(label_coordinates, content)

        if config.verbose:
            print(
                "[Intent Pilot][call_gpt_4_vision_preview_labeled] new processed_content",
                processed_content,
            )
        return processed_content

    except Exception as e:
        if config.verbose:
            print("[Self-Operating Computer][Operate] error", e)
            traceback.print_exc()
        return call_gpt_4_vision_preview_labeled(openai_client, messages, objective)

def calculate_center(bbox):
    return (bbox["xmin"] + bbox["xmax"]) / 2, (bbox["ymin"] + bbox["ymax"]) / 2

def process_click_operation(operation, label_coordinates):
    if operation.get("operation") == "click-text":
        text_bbox = extract_element_bbox(operation.get("text", None), label_coordinates["text"], flexible_search=True)
        x, y = calculate_center(text_bbox)
    elif operation.get("operation") == "click-icon":
        label_bbox = extract_element_bbox(int(operation.get("label", None)), label_coordinates["indices"])
        x, y = calculate_center(label_bbox)
    else:
        return operation

    operation["operation"] = "click"
    operation["x"] = x
    operation["y"] = y
    return operation

def merge_click_operations(label_coordinates, content):
    processed_content = [process_click_operation(operation, label_coordinates) for operation in content]
    return processed_content
