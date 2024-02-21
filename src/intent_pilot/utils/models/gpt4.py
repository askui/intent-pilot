

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

def get_response_from_gpt4v(openai_client, messages, temperature=0.7, max_tokens=1000):
    response = openai_client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        presence_penalty=1,
        frequency_penalty=1,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
