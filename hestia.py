import os
import sys
import importlib
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def speak(text):
    print(f"Hestia: {text}")
    
def run_command(command):
    parts = command.split(" ")
    command_name = parts[0]
    
    try:
        module = importlib.import_module(f"commands.{command_name}")
        if hasattr(module, 'execute'):
            module.execute(parts[1:])
        else:
            speak(f"Command {command_name} does not have an execute function")
    except ModuleNotFoundError:
        speak(f"Command {command_name} not found")
        
def run_assistant():
    run_command("hello")
    
    while True:
        command = input("You: ").lower()
        if command == "exit":
            speak("Goodbye")
            break
        run_command(command)
        
if __name__ == "__main__":
    run_assistant()