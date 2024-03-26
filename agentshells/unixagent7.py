import subprocess
from uuid import uuid4
from os.path import exists, join
from time import sleep

class TerminalWrapper:
    def __init__(self):
        # Open the output file in append mode so that each command's output is added to the end of the file
        self.output_file = open('out.txt', 'a')
        # Start a subprocess with a shell, directing stdout and stderr to the same output file
        self.process = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE, stdout=self.output_file, stderr=subprocess.STDOUT, text=True)

    def execute_command(self, command, delimiter_id):
        #print('execute_command start')
        # Write the command to the subprocess stdin, appending newline to execute it
        self.output_file = open(join('data', f'{delimiter_id}.txt'), 'a')

        self.process.stdin.write(f'echo "---{delimiter_id}---"' + "\n")
        self.process.stdin.flush()
        
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        self.process.stdin.write(f'echo "///{delimiter_id}///"' + "\n")
        self.process.stdin.flush()
        #print('execute_command end')

    def round_trip(self, command, delimiter_id, sleep_interval=0.1):
        tw.execute_command(command, current_command_id)
        output = self.read_output(current_command_id)
        while output is None:
            # Wait for 100 ms
            sleep(sleep_interval)
            output = self.read_output(current_command_id)
        return output

    # reads the output file and finds the output of the command with the given delimiter_id
    def read_output(self, delimiter_id):
        #print('red_output start')
        #print('printall:')
        output_text = ''
        # First print everything in the output file
        got_to_start = False
        with open('out.txt', 'r') as file:
            for line in file:
                if line == f"---{delimiter_id}---\n":
                    #print('THIS IS START!')
                    got_to_start = True
                elif line == f"///{delimiter_id}///\n":
                    #print('THIS IS END!')
                    return output_text
                elif got_to_start:
                    output_text += line
        return None

    def add_line(self, line, delimiter_id=None):
        self.process.stdin.write(f'echo "{line}"' + "\n")
        self.process.stdin.flush()

    def close(self):
        # Close the subprocess stdin and the output file when done
        self.process.stdin.close()
        self.output_file.close()

# thread that continually reads the output file and updates the output history

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
            output = tw.round_trip(command, current_command_id)
            print('%')
            print(output)

    finally:
        # Ensure resources are cleaned up properly
        tw.close()
