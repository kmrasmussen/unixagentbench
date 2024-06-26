# unix-bench
using the terminal is an essential job for many people. The goal of unix-bench is to be a standard resource for evaluating the ability for LLMs to perform tasks through the terminal. Getting high-performing unix agents could be economically valuable in itself and could also be important building blocks for more advanced systems such as software engineering and data science agents.

The project consists of 
* AgentShell, an simple Python library for stateful sequential interactions with the terminal
* Challenges - a set of challenges that can be solved by using the terminal
* Evaluator - a script that evaluates an OpenRouter LLM on challenges to benchmark the performance

# TODO

## Challenges
The main problem atm is to design the structure of challenges: The current proposal is:

Every directory has:
- A prompt text: A text file that describes the task/challenge.
- Startup workdir: A directory that is either empty or contains files to be used in the task.
- Metadata
- Endup dir: A directory whose structure and files are as they are supposed to be after task has been completed
- Validation tests: Scripts or code that validates that the agent has solved the task it is supposed to be. The simplest case is comparing startup with endup dir, but for different challenges this can be insufficient and/or unneccessary.

### Automatic generation of challenges
Hopefully it is possible to find a way in which relatively high quality challenges can be generated by LLMs.

## AgentShell
AgentShell tries to turn unix stdin, stdout and stderr into sequential blocks of strings. The basic functionality works but more can be done to increase robustness. There are open design choices wrt to late stdout.
```
shell = AgentShell(cwd='~/')
command_input = 'pwd'
command_id, command_output = shell.round_trip(command_input) 
```
Each command has an input string, uuid4 id and output string.

## Evaluator
The current state of the evaluator is as follows:

- OpenRouter.ai is a service that allows a uniform interface to different LLMs. Using this service it will become easier to benchmark different models. A model name can be selected from OpenRouter. This requires and OpenRouter API key. For now OpenRouter should be sufficient but it might be worth extending to s

