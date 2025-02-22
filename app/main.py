import sys
import os
import shutil
from typing import NoReturn
from pathlib import Path

    

def handle_inputline(inputline: str) -> None:
    """parse and handle the codes and text from input line"""
    
    code, *args = inputline.strip().split(maxsplit=1) # make command to two part
    args = args[0].split() if args else []
    
    match code:
        case "exit":
            handle_exit()
        case "echo":
            handle_echo(args)
        case "type":
            handle_type(args[0]) if args else sys.stderr(f"type should have an argument")
        case _: 
            if os.path.isfile(inputline.split(" ")[0]):
                os.system(inputline)
            else:
                sys.stdout.write(f"{inputline}: command not found")

            
def handle_echo(args: list[str]) -> None:
    """handle echo command"""
    sys.stdout.write(f"{' '.join(args)}\n")
        
            
def handle_exit(code: str = "0") -> NoReturn:
    """Handle exit command and the optional status code"""
    try:
        sys.exit()
    except ValueError:
        sys.exit(f"invalid exit code: {code}")
    
def handle_type(command: str) -> None:
    """Handle type command and be cross platform to pass the tests"""
    default_command = {"type", "exit", "echo"}
    
    if command in default_command:
        sys.stdout.write(f"{command} is a shell builtin\n")
        return
    
    exe_path = shutil.which(command)
    
    if exe_path:
        unix_path = Path(exe_path).as_posix()
        sys.stdout.write(f"{command} is {unix_path}\n")
    else:
        sys.stdout.write(f"{command}: not found\n")
    



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
