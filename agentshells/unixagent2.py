import subprocess
import time
import select

class TerminalWrapper:
    def __init__(self):
        self.process = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=0, universal_newlines=True)

    def execute_command(self, command):
        command = command.strip() + '\n'
        self.process.stdin.write(command)
        self.process.stdin.flush()

        output = ""
        # Wait for command to execute and capture output
        while True:
            # Use select to wait for output to be available
            if select.select([self.process.stdout], [], [], 0.5)[0]:
                line = self.process.stdout.readline()
                print('line:', line)
                output += line
            else:
                # No more output, command execution likely finished
                print('no more lines')
                break
        
        return output

# Example usage
if __name__ == "__main__":
    tw = TerminalWrapper()
    print("Terminal Wrapper: Type your command and press enter. Type 'exit' to quit.")

    while True:
        command = input("$ ")
        if command.strip().lower() == "exit":
            print("Exiting Terminal Wrapper.")
            break
        output = tw.execute_command(command)
        print(output, end='')  # Use end='' to avoid adding extra newlines
