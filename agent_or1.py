from agentshells.unixagent9b import AgentShell

import os
import requests
import json
import re

'''
openai/gpt-4-turbo-preview
openai/gpt-3.5-turbo
01-ai/yi-34b-chat
google/gemini-pro
'''
model = 'openai/gpt-3.5-turbo'

# get OPENROUTER_API_KEY from env
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
print(OPENROUTER_API_KEY)

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

messages = [
    {
        "role": "user",
        "content": "You are a friendly chatbot that has access to a stateful unix shell to help with the task described in the <task> tag. You can run commands and access the filesystem, by using the <stdin> tag to specify input to the shell. Instead of a human user that will interact with you, the user response will be the output from the shell given in the <stdout> command. <task>Your current task is this: Make a new folder called hey, go into it and determine the absolute path. Then make a text file inside the folder called yo with the content 'hello world'. Finally, print the contents of the folder.</task>. If you think you're done with the entire task., use the <done /> tag. DO NOT JUST RESPOND WITH CODE, THE CODE HAS TO BE IN STDIN TAG TO WORK."
    },
    {
        "role": "assistant",
        "content": "Let's start by looking at the current dir to get a hang of it. \n <stdin>ls</stdin>"
    },
    {
        "role": "user",
        "content": "<stdout>README.md\nagent1.py\nagent_or1.py\nagentshells\nchallenges\nin.jsonl\nout.txt</stdout>"
    }
]

def get_response(add_assistant_response=True):
    global messages
    print('get response start', messages)
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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

tw = AgentShell()
max_rounds = 10
for round_i in range(max_rounds):
    print('Round', round_i)
    response_text = get_response()
    xml_structures = extract_xml_structures(response_text)
    print('xml structs', xml_structures)
    #assert len(xml_structures) > 0, 'Expected at least one xml structure'
    if len(xml_structures) == 0:
        print('No xml structures found.')
        messages.append({
            "role": "user",
            "content": "ERROR. No stdin or done tag found. Remember that all code to be executed in shell must be in <stdin> tags. If you think you're done with the task, use the <done /> tag."
        })
        continue
    #assert len(xml_structures) == 1, 'Expected one xml structure'
    stdout_string = ''
    for xml_structure in xml_structures:
        print('xml struct', xml_structure)
        if xml_structure['tag'] == 'done':
            print('Agent used <done /> tag to signal completion. Exiting.')
            break
        assert xml_structure['tag'] == 'stdin', 'Expected stdin tag'
        command_input = xml_structure['content']
        print('command input', command_input)
        command_id, command_output = tw.round_trip(command_input)
        print('%', command_id)
        print('command output', command_output)
        stdout_string += '<stdout>' + command_output + '</stdout>'
    print('user will reply:', stdout_string)
    messages.append({
        "role": "user",
        "content": stdout_string
    })
    print('Appended stdout')

print('END')