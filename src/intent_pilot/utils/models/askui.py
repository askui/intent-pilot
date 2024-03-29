import json

import requests

from intent_pilot.utils.config import Config
from intent_pilot.utils.encoding import encode_image, encode_string
from intent_pilot.utils.img_utils import draw_bboxes, open_pil_image
import platform
from importlib.metadata import version

system_platform = platform.system()

config = Config()


def request_image_annotation(
    image_file: str,
    workspace_id: str,
    token_id: str,
    inference_endpoint: str = "https://inference.askui.com",
):
    image_base64 = encode_image(image_file)
    token_base64 = encode_string(token_id)
    payload = {
        "image": "," + image_base64,
        "modelComposition": [
                 {
                    "task": "e2e_ocr",
                    "architecture": "easy_ocr",
                    "version": "1",
                    "interface": "im2txtbox",
                    "useCase": "faster",
                    "tags": []
                },
                {
                    "task": "od",
                    "architecture": "yolo",
                    "interface": "c9",
                    "useCase": "default",
                    "version": "6",
                    "tags": [],
                }
        ]
    }
    payload_json = json.dumps(payload)
    response = requests.post(
        f"{inference_endpoint}/api/v3/workspaces/{workspace_id}/inference",
        data=payload_json,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {token_base64}",
            'User-Agent': f"AskUI-Intent-Pilot/{version('intent_pilot')}",
            'askui-user-agent': f"os:{system_platform}",
        },
    )
    return response


def get_label_coordinates(annotated_data, skip_labels=[]):
    label_coordinates = {}
    label_coordinates["indices"] = {}
    for skip_label in skip_labels:
        label_coordinates[skip_label] = {}

    for idx, element in enumerate(annotated_data["data"]["detected_elements"], 1):
        element_type = element["name"]
        if element_type in skip_labels:
            label_coordinates[element_type][element[element_type]] = element["bndbox"]
        else:
            label_coordinates["indices"][idx] = element["bndbox"]
    return label_coordinates


def get_labeled_image(filename, skip_labels=[]):
    annotated_data = request_image_annotation(
        filename, config.aui_workspace_id, config.aui_token
    )
    try:
        annotated_data = annotated_data.json()
    except Exception as exc:
        raise PermissionError(
            f"AskUI credentials down {str(annotated_data)} from {exc}"
        )
    image = open_pil_image(filename)
    label_coordinates = get_label_coordinates(annotated_data, skip_labels=skip_labels)
    pil_image_with_bboxes = draw_bboxes(image, label_coordinates["indices"])
    return pil_image_with_bboxes, label_coordinates
