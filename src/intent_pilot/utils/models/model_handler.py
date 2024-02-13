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
from intent_pilot.utils.config import Config
from intent_pilot.utils.img_utils import extract_element_bbox
from intent_pilot.utils.models.askui import get_labeled_image
from intent_pilot.utils.encoding import encode_image
from intent_pilot.utils.models.prompts import get_user_first_message_prompt, get_user_prompt

config = Config()

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

def format_gpt4v_message(user_prompt, img_base64_labeled):
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": user_prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_base64_labeled}"
                },
            },
        ],
    }

def call_gpt_4_vision_preview_labeled(openai_client, messages, objective, screenshots_dir: Path = Path("screenshots")):
    time.sleep(1)

    try:
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        img_id = uuid.uuid4()

        screenshot_filename = capture_screenshot_in_a_folder(screenshots_dir, img_id)
        pil_image_with_bboxes, label_coordinates =  get_labeled_image(screenshot_filename)
        labeled_img_path = save_labeled_pil_img_in_folder(pil_image_with_bboxes, screenshots_dir, img_id)
        img_base64_labeled = encode_image(labeled_img_path)
        user_prompt = get_relative_user_prompt(len(messages))
        vision_message = format_gpt4v_message(user_prompt, img_base64_labeled)
        messages.append(vision_message)
        response = openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            presence_penalty=1,
            frequency_penalty=1,
            temperature=0.7,
            max_tokens=1000,
        )

        content = response.choices[0].message.content

        # content = content.removeprefix(prefix).removesuffix(suffix)
        if content.startswith("```json"):
            content = content[len("```json") :]  # Remove starting ```json
            if content.endswith("```"):
                content = content[: -len("```")]  # Remove ending

        assistant_message = {"role": "assistant", "content": content}
        messages.append(assistant_message)

        content = json.loads(content)

        processed_content = []

        for operation in content:
            if operation.get("operation") == "click":
                label = operation.get("label")

                coordinates = extract_element_bbox([int(label)], label_coordinates)
                operation["x"] = (coordinates[0] + coordinates[2])/2
                operation["y"] = (coordinates[1] + coordinates[3])/2
                if config.verbose:
                    print(
                        "[Intent Pilot][call_gpt_4_vision_preview_labeled] new click operation",
                        operation,
                    )
                processed_content.append(operation)
            else:
                processed_content.append(operation)

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
