from agentshells.shell1 import AgentShell
import redis
import os

redis_client = redis.Redis(password=os.environ['REDIS_PASSWORD'])
tw = AgentShell(cwd='/home/ec2-user/projects/unixagentbench/emptydir',
                redis_pubsub_channel='myagentshellchannel',
                redis_client=redis_client)
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