import sys

def user_command() -> str:
    """Use $ for the first writing letter"""
    try:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        return sys.stdin.readline().strip()
    
    except KeyboardInterrupt:
        print(f"Exiting from the shell")

def handle_command(command: str) -> str:
    """Handle user inputs and commands"""
    try: 
        if not command:
            return 
        sys.stdout.write(f"{command}: command not found")
        sys.stdout.flush()
        
    except Exception as e:
        print(f"exception error: {e}")


def main():
    # Uncomment this block to pass the first stage
    # sys.stdout.write("$ ")
    while True: 
        command = user_command()
        if command.lower() in ('exit', 'quit'):
            break
        print(handle_command(command))
    
    # Wait for user input
    # new_command = input()
    # print(f"{new_command}: command not found")

if __name__ == "__main__":
    main()
