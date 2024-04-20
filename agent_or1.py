from agentshells.shell1 import AgentShell
import os
import json
import re
import sys
import argparse
from config import *
from challenge import get_challenge_by_id, Challenge
from utils import extract_xml_structures, get_completion

def start_agent(challenge, model, max_rounds):
    tw = AgentShell(cwd=challenge.workdir)
    messages = get_pre_prompt(challenge)
    for round_i in range(max_rounds):
        print('Round', round_i)
        response_text = get_completion(
            messages, model, OPENROUTER_API_KEY, add_assistant_response=True)
        print('messages length', len(messages))
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
    print('end of rounds')

# take command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run agent for challenge')
    parser.add_argument('--challenge_id',  type=str, help='Challenge ID')
    parser.add_argument('--max_rounds', type=int, default=10, help='Max rounds')
    parser.add_argument('--model', type=str, default='openai/gpt-3.5-turbo', help='Model')
    args = parser.parse_args()
    print('challenge id', args.challenge_id)
    challenge = get_challenge_by_id(args.challenge_id)
    print('loaded challenge', challenge.challenge_id)
    print('starting agent')
    start_agent(challenge, args.model, args.max_rounds)