import subprocess
import shlex


# Split a command line using the operator ->
# The operator is recognized only outside quotes.
def split_pipeline(command_line):
    commands = []
    current = []
    quote = None
    escaped = False
    i = 0

    while i < len(command_line):
        char = command_line[i]

        if escaped:
            current.append(char)
            escaped = False
            i += 1
            continue

        if char == "\\" and quote != "'":
            current.append(char)
            escaped = True
            i += 1
            continue

        if char in ("'", '"'):
            if quote is None:
                quote = char
            elif quote == char:
                quote = None

            current.append(char)
            i += 1
            continue

        if quote is None and command_line.startswith("->", i):
            commands.append("".join(current).strip())
            current = []
            i += 2
            continue

        current.append(char)
        i += 1

    commands.append("".join(current).strip())

    return commands


# Convert a command into a list of arguments
def parse_command(command):
    return shlex.split(command)


# Execute an external Linux command
def execute_command(args):
    try:
        result = subprocess.run(args, check=False)
        return result.returncode

    except FileNotFoundError:
        print(f"opsh: command not found: {args[0]}")
        return 127

    except PermissionError:
        print(f"opsh: permission denied: {args[0]}")
        return 126

    except OSError as error:
        print(f"opsh: execution error: {error}")
        return 1


# Main shell loop
def main():

    print("Welcome to OPSH - Mini Shell")
    print("Type 'quit' to exit.")

    while True:

        try:
            # Display the shell prompt
            command_line = input("opsh> ")

            # Ignore empty commands
            if not command_line.strip():
                continue

            # Split the command using ->
            commands = split_pipeline(command_line)

            # Check for empty commands
            if any(command == "" for command in commands):
                print("opsh: invalid empty command")
                continue

            # Parse all command segments
            try:
                parsed_commands = [
                    parse_command(command)
                    for command in commands
                ]

            except ValueError as error:
                print(f"opsh: syntax error: {error}")
                continue

            # Ignore commands containing only spaces
            if not parsed_commands[0]:
                continue

            # Exit the shell
            if len(parsed_commands) == 1:
                args = parsed_commands[0]

                if args[0] in ("quit", "exit"):
                    if len(args) > 1:
                        print("Usage: quit")
                        continue

                    break

            # Pipes are implemented in Part 3
            if len(parsed_commands) > 1:
                print("opsh: pipes will be implemented in Part 3")
                continue

            # Execute the command
            execute_command(parsed_commands[0])

        except KeyboardInterrupt:
            print()
            continue

        except EOFError:
            print()
            break

    print("Goodbye! Exiting OPSH.")


# Program entry point
if __name__ == "__main__" :
      main()
