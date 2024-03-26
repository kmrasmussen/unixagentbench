from agentshells.unixagent9b import AgentShell

tw = AgentShell()
try:
    print("Terminal Wrapper: Type your command and press enter. Type 'exit' to quit.")

    while True:
        command_input = input("AS$ ")
        if command_input.strip().lower() == "exit":
            print("Exiting Terminal Wrapper.")
            break
        command_id, command_output = tw.round_trip(command_input)
        print('%', command_id)
        print(command_output)

finally:
    # Ensure resources are cleaned up properly
    tw.close()

print(tw.get_completed_pairs_xml())