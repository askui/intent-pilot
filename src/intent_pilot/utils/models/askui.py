import os
import requests
import json
from intent_pilot.utils.encoding import encode_string, encode_image
from intent_pilot.utils.img_utils import draw_bboxes, open_pil_image

workspaceId=os.getenv("ASKUI_WORKSPACE_ID")
token=os.getenv("ASKUI_TOKEN")

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


def get_labeled_image(filename):
    annotated_data = request_image_annotation(filename, workspaceId, token)
    try:
        annotated_data = annotated_data.json()
    except Exception as exc:
        raise PermissionError(f"AskUI credentials down {str(annotated_data)} from {exc}")
    image = open_pil_image(filename)
    pil_image_with_bboxes = draw_bboxes(image, annotated_data)
    return pil_image_with_bboxes, annotated_data