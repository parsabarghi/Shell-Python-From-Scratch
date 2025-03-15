import sys
import shutil
import os
import subprocess
import shlex
import readline
# from pyreadline import Readline
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
    args = parts[1::] if len(parts) > 1 else []
    
    
    if any(redir in args for redir in ('>', '1>', '2>', '>>', '1>>', '2>>')):
        handle_redirect(command=(' '.join(parts)))
        return
    if code in COMMAND_MAP:
        COMMAND_MAP[code](args)
    else:
        exe_path = shutil.which(code)
        if exe_path:
            execute_external(exe_path, code, args)
        else:
            sys.stdout.write(f"{code}: command not found\n")

def handle_show_matches(substitution: str, matches: list[str], longest_match_length) -> None:

    try:
        sys.stdout.write("\n")
        sys.stdout.write(" ".join(matches) + "\n")
        sys.stdout.write(f"$ {substitution}")
        sys.stdout.flush()
        readline.redisplay()

    except Exception as e:
        sys.stderr.write(f"{e}")
            
        
def handle_completer(text: str, state: int) -> str | None:
    """Handle autocompletion using <tab>"""
    internal_matches = [cmd for cmd in COMMAND_MAP.keys() 
                        if cmd.startswith(text)]
    
    external_matches = []
    seen = set()
    
    for dir_path in os.environ.get("PATH", "").split(os.pathsep):
        if not os.path.isdir(dir_path):
            continue
        try:
            with os.scandir(dir_path) as entries:  
                for entry in entries:
                    if entry.name in seen or not entry.name.startswith(text):
                        continue
                    if entry.is_file() and os.access(entry.path, os.X_OK):
                        external_matches.append(entry.name)
                        seen.add(entry.name)
        except OSError:
            continue
    
    all_matches = sorted(internal_matches + external_matches)
    return f"{all_matches[state]} " if state < len(all_matches) else None
    


def handle_redirect(command: str) -> None:
    """Handle redirections"""
    try: 
        os.system(command)
    except Exception as e:
        sys.stderr.write(f"Exception error on redirection: {e}")

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
        else:
            os.chdir(directory)
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
    
    readline.set_completer(handle_completer)
    readline.set_completion_display_matches_hook(handle_show_matches)
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(' \t\n`~!@#$%^&*()-=+[{]}\\|;:\'",<>?')  
    
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            inputline = input()
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
