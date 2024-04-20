import os
from config import challenges_dir

class Challenge:
    def __init__(self, challenge_id, challenge_dir, challenge_workdir, task_prompt):
        self.challenge_id = challenge_id
        self.challenge_dir = challenge_dir
        self.workdir = challenge_workdir
        self.task_prompt = task_prompt
        
def get_challenge_by_id(challenge_id):
    challenge_dir = os.path.join(challenges_dir, challenge_id)
    challenge_workdir = os.path.join(challenge_dir, 'workdir')
    assert os.path.exists(challenge_dir), f'Challenge dir {challenge_dir} does not exist'
    assert os.path.exists(challenge_workdir), f'Challenge workdir {challenge_workdir} does not exist'
    task_prompt_txt_file_path = os.path.join(challenge_dir, 'task_prompt.txt')
    assert os.path.exists(task_prompt_txt_file_path), f'Task prompt file {task_prompt_txt_file_path} does not exist'
    task_prompt = open(task_prompt_txt_file_path).read().strip()
    
    # define challenge class
    challenge = Challenge(challenge_id, challenge_dir, challenge_workdir, task_prompt)
    return challenge   
