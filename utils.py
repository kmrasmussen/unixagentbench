import requests
import json 
import re
from os.path import exists, join
from config import *

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

def extract_xml_structures2(input_string):
    pattern = r'<(\w+)(?:>(.*?)</\1>|/>)'  # Updated pattern to handle empty tags
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
    #print('get response start', messages)
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
    #print('data', data)
    assert len(data['choices']) == 1, 'Expected one choice'
    response_text = data['choices'][0]['message']['content']
    #print('res text', response_text)
    #print('get reponse end')
    if add_assistant_response:
        messages.append({
            "role": "assistant",
            "content": response_text
        })
    return response_text

import filecmp

def workdir_postdir_compare(dir1, dir2):
    dir1 = join(challenges_dir,'001/dirs/workdir')
    dir2 = join(challenges_dir,'001/dirs/post')

    dcmp = filecmp.dircmp(dir1, dir2)
    print("Files only in {}: {}".format(dir1, dcmp.left_only))
    print("Files only in {}: {}".format(dir2, dcmp.right_only))
    print("Common files, same content: {}".format(dcmp.common_files))
    print("Common files but different: {}".format(dcmp.diff_files))
    print("Common subdirectories: {}".format(dcmp.common_dirs))

def diff_workdir_postdir_compare(dir1, dir2):
    dir1 = join(challenges_dir,'001/dirs/workdir')
    dir2 = join(challenges_dir,'001/dirs/post')

    # using subprocess do diff -r dir1 dir2 and get string output
    import subprocess
    cmd = f'diff -r {dir1} {dir2}'
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output_str = output.decode('utf-8')
    if error is not None:
        # exception
        raise Exception(f'Error in diff command: {error}')
    return output_str
