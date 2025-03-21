#!/usr/bin/env python3

import argparse
import importlib
import sys

def run_command(command):
    parts = command.split(" ")
    command_name = parts[0]

    try:
        module = importlib.import_module(f"commands.{command_name}")
        
        if hasattr(module, 'execute'):
            module.execute(parts[1:])
        else:
            print(f"Command '{command_name}' does not have an execute function.")
    except ModuleNotFoundError:
        print(f"Command '{command_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Hestia CLI Assistant")
    parser.add_argument("command", type=str, help="The command to run (e.g., 'hello')")
    args = parser.parse_args()
 
    run_command(args.command)

if __name__ == "__main__":
    main()
