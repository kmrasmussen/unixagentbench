import subprocess
from uuid import uuid4
from os.path import exists, join

class TerminalWrapper:
    def __init__(self):
        # Open the output file in append mode so that each command's output is added to the end of the file
        self.output_file = open('out.txt', 'a')
        # Start a subprocess with a shell, directing stdout and stderr to the same output file
        self.process = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE, stdout=self.output_file, stderr=subprocess.STDOUT, text=True)

    def execute_command(self, command, delimiter_id=None):
        # Write the command to the subprocess stdin, appending newline to execute it
        self.output_file = open(join('data', f'{delimiter_id}.txt'), 'a')

        self.process.stdin.write(f'echo "---{delimiter_id}---"' + "\n")
        self.process.stdin.flush()
        
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        self.process.stdin.write(f'echo "///{delimiter_id}///"' + "\n")
        self.process.stdin.flush()

    def add_line(self, line, delimiter_id=None):
        self.process.stdin.write(f'echo "{line}"' + "\n")
        self.process.stdin.flush()

    def close(self):
        # Close the subprocess stdin and the output file when done
        self.process.stdin.close()
        self.output_file.close()

# Example usage
if __name__ == "__main__":
    tw = TerminalWrapper()
    tw.add_line('start')
    try:
        print("Terminal Wrapper: Type your command and press enter. Type 'exit' to quit.")

        while True:
            command = input("$ ")
            current_command_id = str(uuid4())
            if command.strip().lower() == "exit":
                print("Exiting Terminal Wrapper.")
                break
            tw.execute_command(command, current_command_id)
            
    finally:
        # Ensure resources are cleaned up properly
        tw.close()
