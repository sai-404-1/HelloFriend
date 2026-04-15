from pathlib import Path
from ollama import chat
from os.path import isdir
from os import mkdir, listdir
from time import strftime
import json

MODEL_NAME="name"
global message_from_chat
message_from_chat=[{'role': 'user', 'content': 'Чат начинается'}]

def add_to_end(message:dict={'role': 'user/assistant', 'content': 'something'}):
    return message_from_chat.append(message)

def stream_message(messages):
    stream = chat(
        model=MODEL_NAME,
        messages=messages,
        stream=True
    )
    message = ""
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        message+=chunk['message']['content']
    print('\n')
    return message

if not isdir('./chats'):
    mkdir("./chats")

while True:
    try:
        user_input = input(">>> ")
        add_to_end({'role': 'user', 'content': user_input})
        assistant_output = stream_message(message_from_chat)
        add_to_end({'role': 'assistant', 'content': assistant_output})
    except KeyboardInterrupt:
        file_name = f"{strftime('%d%m%y_%H%M%S')}_{len(listdir('./chats'))}"
        with open(f"./chats/{file_name}.jsonl", "w") as file:
            for message in message_from_chat:
                file.write(json.dumps(message, ensure_ascii=False)+'\n')
            file.close()
        break