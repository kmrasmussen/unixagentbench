import subprocess
from uuid import uuid4

class TerminalWrapper:
    def __init__(self):
        # Open the output file in append mode so that each command's output is added to the end of the file
        self.output_file = open('out.txt', 'a')
        # Start a subprocess with a shell, directing stdout and stderr to the same output file
        self.process = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE, stdout=self.output_file, stderr=subprocess.STDOUT, text=True)

    def execute_command(self, command):
        # Write the command to the subprocess stdin, appending newline to execute it
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

    def put_delimiter(self, delimiter_id):
        # Write a delimiter to the output file to separate command outputs
        self.process.stdin.write(f'echo "---{delimiter_id}---"' + "\n")
        self.process.stdin.flush()

    def close(self):
        # Close the subprocess stdin and the output file when done
        self.process.stdin.close()
        self.output_file.close()

# Example usage
if __name__ == "__main__":
    tw = TerminalWrapper()
    tw.put_delimiter('start')
    try:
        print("Terminal Wrapper: Type your command and press enter. Type 'exit' to quit.")

        while True:
            command = input("$ ")
            if command.strip().lower() == "exit":
                print("Exiting Terminal Wrapper.")
                break
            tw.put_delimiter(str(uuid4()))
            tw.execute_command(command)
            
    finally:
        # Ensure resources are cleaned up properly
        tw.close()
