import os
import requests
import json
from intent_pilot.utils.encoding import encode_string, encode_image
from intent_pilot.utils.img_utils import draw_bboxes, open_pil_image
from intent_pilot.utils.config import AskUIIntentPilotConfig

config = AskUIIntentPilotConfig()

def request_image_annotation(
    image_file: str, workspace_id: str, token_id: str, inference_endpoint: str = "https://inference.askui.com"
):
    image_base64 = encode_image(image_file)
    token_base64 = encode_string(token_id)
    payload = {"image": "," + image_base64}
    payload_json = json.dumps(payload)
    response = requests.post(
        f"{inference_endpoint}/api/v3/workspaces/{workspace_id}/inference",
        data=payload_json,
        headers={"Content-Type": "application/json", "Authorization": f"Basic {token_base64}"},
    )
    return response


def get_label_coordinates(annotated_data, skip_labels=[]):
    label_coordinates = {}
    label_coordinates['indices'] = {}
    for skip_label in skip_labels:
        label_coordinates[skip_label] = {}

    for idx, element in enumerate(annotated_data['data']['detected_elements'], 1):
        element_type = element["name"]
        if element_type in skip_labels:
            label_coordinates[element_type][element[element_type]] = element["bndbox"]
        else:
            label_coordinates['indices'][idx] = element["bndbox"]
    return label_coordinates

def get_labeled_image(filename, skip_labels=[]):
    annotated_data = request_image_annotation(filename, config.aui_workspace_id, config.aui_token)
    try:
        annotated_data = annotated_data.json()
    except Exception as exc:
        raise PermissionError(f"AskUI credentials down {str(annotated_data)} from {exc}")
    image = open_pil_image(filename)
    label_coordinates =  get_label_coordinates(annotated_data, skip_labels=skip_labels)
    pil_image_with_bboxes = draw_bboxes(image, label_coordinates["indices"])
    return pil_image_with_bboxes, label_coordinates