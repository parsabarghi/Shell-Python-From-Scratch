import sys
import shutil
import os
import subprocess
import shlex
from typing import NoReturn
from pathlib import Path

COMMAND_MAP = {
    "exit": lambda _: handle_exit(),
    "echo": lambda args: handle_echo(args),
    "type": lambda args: handle_type(args[0] if args else ""),
    "pwd": lambda _: handle_pwd(),
    "cd": lambda args: handle_cd(args[0] if args else ""),
}
    

def handle_inputline(inputline: str) -> None:
    """Parse and route commands to appropriate handlers"""
    parts = shlex.split(inputline.strip())
    code = parts[0] if parts else ""
    args = parts[1].split() if len(parts) > 1 else []
    
    if code in COMMAND_MAP:
        COMMAND_MAP[code](args)
    else:
        exe_path = shutil.which(code)
        if exe_path:
            execute_external(exe_path, code, args)
        else:
            sys.stdout.write(f"{code}: command not found\n")


def execute_external(exe_path: str, command: str, args: list[str]) -> None:
    """Execute external program with arguments"""
    try:
        process = subprocess.run(
            [command] + args,  
            executable=exe_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        sys.stdout.write(process.stdout)
        sys.stderr.write(process.stderr)
    except PermissionError:
        sys.stderr.write(f"{command}: Permission denied\n")
    except Exception as e:
        sys.stderr.write(f"Error executing {command}: {str(e)}\n")
        

def handle_pwd() -> None:
    """Handle the PWD command and get the current dir"""
    current_dir = Path.cwd()
    sys.stdout.write(f"{current_dir}\n")

def handle_cd(directory: str) -> None:
    """handle the cd command and change the current dir"""
    try: 
        if directory == "~":
            home = os.path.expanduser("~")
            # print(home)
            os.chdir(home)
        else: os.chdir(directory)
    except OSError:
        print(f"cd: {directory}: No such file or directory")
    
    
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
    
    if command in COMMAND_MAP:
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
            sys.stdout.write("$ ")
            sys.stdout.flush()
            inputline = sys.stdin.readline().strip()
            if not inputline:
                continue
            handle_inputline(inputline)
        except (EOFError, KeyboardInterrupt):
            sys.stdout.write("\n")
            sys.exit(0)
        except Exception as e:
            sys.stderr.write(f"Error: {str(e)}\n")
    # Wait for user input
    # new_command = input()
    

if __name__ == "__main__":
    main()
