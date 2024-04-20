import requests
import json 
import re


def extract_xml_structures(input_string):
    pattern = r'<(\w+)>(.+?)</\1>'
    matches = re.findall(pattern, input_string)
    
    result = []
    for match in matches:
        tag, content = match
        element = {
            'tag': tag,
            'content': content.strip()
        }
        result.append(element)
    
    return result

def get_completion(messages, model, or_api_key, add_assistant_response=True):
    print('get response start', messages)
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {or_api_key}",
    },
    data=json.dumps({
        "model": model, #"openai/gpt-3.5-turbo", # Optional'anthropic/claude-3-opus', #
        "messages": messages
    })
    )
    data = response.json()
    print('data', data)
    assert len(data['choices']) == 1, 'Expected one choice'
    response_text = data['choices'][0]['message']['content']
    print('res text', response_text)
    print('get reponse end')
    if add_assistant_response:
        messages.append({
            "role": "assistant",
            "content": response_text
        })
    return response_text
