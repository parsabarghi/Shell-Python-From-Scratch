import sys

def isInvalid() -> str:
    words = sys.stdin
    return words

def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")
    
    # Wait for user input
    new_command = input()
    print(f"{new_command}: command not found")

if __name__ == "__main__":
    main()
