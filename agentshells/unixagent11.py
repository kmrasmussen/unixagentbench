import subprocess
from uuid import uuid4
from os.path import exists, join
from time import sleep
import time
import json
import re

stdout_file = open('stdout.txt', 'a')
stderr_file = open('stderr.txt', 'a')

if exists('stdout.txt'):
    open('stdout.txt', 'w').close()
if exists('stderr.txt'):
    open('stderr.txt', 'w').close()

examples = [
    ["python3", "challenges/program1.py"],
    ["ls", "-l"],
    ["echo", "hello"],
    ["python3"],
    ["bash"]
]

process = subprocess.Popen(
    examples[4],
    stdin=subprocess.PIPE, 
    stdout=stdout_file, 
    stderr=stderr_file, 
    text=True)


while True:
    command_input = input("$ ")
    if command_input.strip().lower() == "exit":
        print("Exiting Terminal Wrapper.")
        break
    process.stdin.write(command_input + "\n")
    #process.stdin.write(f"python3 challenges/program1.py\n")
    process.stdin.flush()    
    