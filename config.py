import os
challenges_dir = '/home/ec2-user/projects/unixagentbench/challenges/'
model = 'openai/gpt-3.5-turbo' #'mistralai/mixtral-8x7b'
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
'''
openai/gpt-4-turbo-preview
openai/gpt-3.5-turbo
01-ai/yi-34b-chat
google/gemini-pro
mistralai/mixtral-8x7b
'''
def get_pre_prompt(task_prompt, workdir):
    pre_prompt = [
        {
            "role": "user",
            "content": f"You are a friendly chatbot that has access to a stateful unix shell to help with the task described in the <task> tag. You can run commands and access the filesystem, by using the <stdin> tag to specify input to the shell. Instead of a human user that will interact with you, the user response will be the output from the shell given in the <stdout> command. \n Your current task is this:\n  <task>\n{task_prompt}\n</task>\nIf you (the assistant) think you're done with the entire task., you (the assistant) use the <done /> tag as a standalone tag (not inside stdin tag of course). DO NOT JUST RESPOND WITH CODE, THE CODE HAS TO BE INSIDE <stdin> TAGS TO WORK."
        },
        {
            "role": "assistant",
            "content": "Let's start by looking at the current dir to get a hang of it. \n <stdin>pwd</stdin>"
        },
        {
            "role": "user",
            "content": f"<stdout>{workdir}</stdout>"
        }
    ]
    return pre_prompt