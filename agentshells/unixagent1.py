import subprocess

class TerminalWrapper:
    def __init__(self):
        # Start a subprocess with a shell
        self.process = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        self.output_history = []

    def execute_command(self, command):
        # Ensure the command executes in a way that its output can be captured
        # and it waits for the command to complete. Adding 'echo' at the end to capture command prompt.
        command = command.strip() + '; echo -e "\\n$?"'
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

        # Read command output
        output = ""
        while True:
            line = self.process.stdout.readline()
            if line == "\n":
                break
            output += line
        
        # Check the exit status
        exit_status = self.process.stdout.readline().strip()
        output += "Exit Status: " + exit_status

        self.output_history.append(output)
        return output

    def get_output_history(self):
        return self.output_history

def main():
    tw = TerminalWrapper()
    print("Terminal Wrapper: Type your command and press enter. Type 'exit' to quit.")

    while True:
        # Get user input
        command = input("$ ")
        
        # Check for exit condition
        if command.strip().lower() == "exit":
            print("Exiting Terminal Wrapper.")
            break

        # Execute the command and print the output
        output = tw.execute_command(command)
        print(output)

if __name__ == "__main__":
    main()
