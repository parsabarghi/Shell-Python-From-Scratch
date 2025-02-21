import sys
from typing import NoReturn


def handle_inputline(inputline: str) -> None:
    """parse and handle the codes and text from input line"""
    
    code, *args = inputline.strip().split(maxsplit=1) # make command to two part
    args = args[0].split() if args else []
    
    match code:
        case "exit":
            handle_exit()
        case "echo":
            handle_echo(args)
        case _: 
            sys.stdout.write(f"{inputline}: command not found\n")

            
def handle_echo(args: list[str]) -> None:
    
    sys.stdout.write(f"{''.join(args)}\n")
        
            
def handle_exit(code: str = "0") -> NoReturn:
    """Handle exit command and the optional status code"""
    try:
        sys.exit()
    except ValueError:
        sys.exit(f"invalid exit code: {code}")
    

# def handle_command(command: str) -> str:
#     """Handle user inputs and commands"""
#     default_commands = ['exit', 'quit', 'type', 'echo']
#     try: 
#         if not command:
#             return
#         elif "echo" in command:
#             sys.stdout.write(f"{command.replace('echo','').lstrip()}\n")
#             sys.stdout.flush()
#         else:
#             sys.stdout.write(f"{command}: command not found \n")
#             sys.stdout.flush()
        
#     except Exception as e:
#         print(f"exception error: {e}")



def main():
    """REPL Loop"""
    # Uncomment this block to pass the first stage
    # sys.stdout.write("$ ")
    while True:
        try:
            handle_inputline(input("$ "))
        except (EOFError, KeyboardInterrupt):
            sys.stderr("\n Exiting")
        except Exception as e:
            sys.stderr(f"exception error: {e}")
    # Wait for user input
    # new_command = input()
    

if __name__ == "__main__":
    main()
