import os
from config import challenges_dir
from os.path import exists, join
import shutil

class Challenge:
    def __init__(self, challenge_id, challenge_dir, challenge_workdir, challenge_predir, challenge_postdir, task_prompt):
        self.challenge_id = challenge_id
        self.challenge_dir = challenge_dir
        self.workdir = challenge_workdir
        self.predir = challenge_predir
        self.postdir = challenge_postdir
        self.task_prompt = task_prompt
        print('Challenge created', self.workdir)
        
def get_challenge_by_id(challenge_id):
    challenge_dir = join(challenges_dir, challenge_id)
    dirs_path = join(challenge_dir, 'dirs')
    assert exists(dirs_path), f'Dirs file {dirs_path} does not exist'

    pre_dir = join(dirs_path, 'pre')
    post_dir = join(dirs_path, 'post')
    assert exists(pre_dir), f'Pre dir {pre_dir} does not exist'
    assert exists(post_dir), f'Post dir {post_dir} does not exist'
    work_dir = join(dirs_path, 'workdir')
    # if work_dir exists, delete it and all contents
    if exists(work_dir):
        shutil.rmtree(work_dir)
        assert not exists(work_dir), f'Work dir {work_dir} could not be removed'
    # create work_dir
    #os.makedirs(work_dir)
    # copy pre_dir to work_dir
    shutil.copytree(pre_dir, work_dir)

    task_prompt_txt_file_path = join(challenge_dir, 'task_prompt.txt')
    assert exists(task_prompt_txt_file_path), f'Task prompt file {task_prompt_txt_file_path} does not exist'
    task_prompt = open(task_prompt_txt_file_path).read().strip()
    
    # define challenge class
    challenge = Challenge(challenge_id, challenge_dir, work_dir, pre_dir, post_dir, task_prompt)
    return challenge   
