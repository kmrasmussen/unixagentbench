from agentshells.shell1 import AgentShell
import os
import json
import re
import sys
import argparse
from config import *
from challenge import get_challenge_by_id, Challenge
from utils import *
import uuid
from typing import List, Optional
import redis
import time

class SingleTaskAgent():
    def __init__(self, model : str, cwd : str, task_prompt : str,
                max_rounds : int, pre_prompt : Optional[List[str]],
                redis_client : Optional[redis.client.Redis],
                shell_redis_pubsub_channel : Optional[str],
                agent_redis_pubsub_channel : Optional[str]):
        self.model = model
        self.cwd = cwd
        self.task_prompt = task_prompt
        self.max_rounds = max_rounds
        self.tw = AgentShell(cwd=self.cwd,
                             redis_pubsub_channel=shell_redis_pubsub_channel,
                             redis_client=redis_client)
        self.messages = pre_prompt if not None else [task_prompt] #get_pre_prompt(self.task_prompt)
        assert pre_prompt is not None, 'NOT IMPLEMENTED: no preprompt'
        self.agent_id = str(uuid.uuid4())
        self.round_i = 0
        self.redis_client = redis_client
        self.shell_redis_pubsub_channel = shell_redis_pubsub_channel
        self.agent_redis_pubsub_channel = agent_redis_pubsub_channel
        print('Agent created', self.cwd, self.task_prompt)

    def perform_round(self):
        round_dict = {
            'round_i': self.round_i,
            'agent_id': self.agent_id,
            'processed_type': []
        }
        print('ROUND', self.round_i)
        response_text = get_completion(
            self.messages, self.model, OPENROUTER_API_KEY,
            add_assistant_response=False)
        self.messages.append({
            "role": "assistant",
            "content": response_text
        })
        round_dict['response_text'] = response_text
        print('ASSISTANT:', response_text)
        xml_structures = extract_xml_structures(response_text)
        round_dict['xml_structures'] = xml_structures
        print('XML:', xml_structures)
        if '<done />' in response_text or '<done/>' in response_text:
            print('Agent used <done /> tag to signal completion.')
            #assert len(xml_structures) == 0, "Expected no xml structures together with <done /> tag, should be implemented."
            round_dict['processed_type'].append('done')          
        
        if len(xml_structures) == 0 or 'done' in [xml_structure['tag'] for xml_structure in xml_structures]:
            print('NO XML CONTINUE')
            round_dict['processed_type'].append('no_xml')
            if 'done' not in round_dict['processed_type']:
                round_dict['user_content'] = "ERROR. No stdin or done tag found. Remember that all code to be executed in shell must be in <stdin> tags. If you think you're done with the task, use the <done /> tag."
            else:
                round_dict['user_content'] = 'USER REPLY EMPTY BECUASE OF DONE TAG.'
        elif xml_structures[0]['tag'] == 'stdin':
            stdout_string = ''
            for xml_structure in xml_structures:
                assert xml_structure['tag'] == 'stdin', 'Expected stdin tag'
                command_input = xml_structure['content']
                roundtrip_dict = self.tw.round_trip(command_input)
                command_id = roundtrip_dict['command_id']
                command_output = roundtrip_dict['command_output']
                stdout_string += '<stdout>' + command_output + '</stdout>'
            round_dict['processed_type'].append('stdin')
            round_dict['user_content'] = stdout_string
            round_dict['roundtrip_dict'] = roundtrip_dict
        else:
            assert False, 'NOT IMPLEMENTED: Expected stdin tag or done tag'
        print('USER:', round_dict['user_content'])
        self.messages.append({
            "role": "user",
            "content": round_dict['user_content']
        })
        if self.redis_client is not None and self.agent_redis_pubsub_channel is not None:
            print('AGENT PUBLISHING')
            self.redis_client.publish(self.agent_redis_pubsub_channel, json.dumps(round_dict))
        print('round return bool', ('done' in round_dict['processed_type']), round_dict['processed_type'])
        round_dict['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return round_dict
    
    def run(self):
        while self.round_i < self.max_rounds:
            round_dict = self.perform_round()
            if 'done' in round_dict['processed_type']:
                print('Round processed_type was done, breaking rounds', self.round_i)
                break
            self.round_i += 1
        print('END OF ROUNDS')

def start_agent_on_challenge(challenge, model, max_rounds):
    print('STARTAGENT NEW')
    redis_client = redis.Redis(password=os.environ['REDIS_PASSWORD'])
    shell_redis_pubsub_channel = 'myagentshellchannel'
    agent_redis_pubsub_channel = 'myagentchannel'

    task_prompt = challenge.task_prompt
    cwd = challenge.workdir
    pre_prompt = get_pre_prompt(challenge.task_prompt, challenge.workdir)
    agent = SingleTaskAgent(model, cwd, challenge.task_prompt,
                            max_rounds, pre_prompt,
                            redis_client, shell_redis_pubsub_channel,
                            agent_redis_pubsub_channel)
    agent.run()
    print('comparing work and postdir:', diff_workdir_postdir_compare(challenge.workdir, challenge.postdir))

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
    start_agent_on_challenge(challenge, args.model, args.max_rounds)