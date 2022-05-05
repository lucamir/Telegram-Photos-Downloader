from os import mkdir, path, remove
from time import sleep

import telethon.sync
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos

api_id = 34423  # REPLACE THE EXAMPLE NUMBER WITH YOUR API ID CODE
api_hash = ""  # PUT_YOUR_API_HASH_CODE_HERE
session_name = "download_media"  # YOU CAN REPLACE THIS STRING WITH A CUSTOM SESSION NAME
download_folder_path = "./downloaded-media"  # YOU CAN REPLACE THIS STRING WITH A CUSTOM FOLDER PATH


def find_chat(chats, chat_name):
    for chat in chats:
        if chat.name == chat_name:
            return chat


def input_chat_name(chats):
    print("\nWrite the chat name from which you want to downlaod the media or exit for close the program")
    while True:
        chat_name = input("What's the chat name? @> ")
        if chat_name == "exit":
            quit()
        else:
            finded = False
            for chat in chats:
                if chat.name == chat_name:
                    finded = True
                    print(chat_name)
                    break
            if not finded:
                print("I can't find a chat with that name, try again with another chat")
            else:
                return chat_name


def main():

    # creation of a client and start the session with your personal API ID AND HASH CODE
    with TelegramClient(session_name, api_id, api_hash) as client:

        client.start()  # start the client

        chats = client.get_dialogs()  # get all the conversations

        # name of the conversation from which you want to download the photos
        chat_name = input_chat_name(chats)

        chat = find_chat(chats, chat_name)  # find the selected chat

        if not path.exists(download_folder_path):
            mkdir(download_folder_path)

        downlaod_counter = 0

        # loop for get from all the messages of the selected conversation just the message that contains photos
        for message in client.iter_messages(chat, filter=InputMessagesFilterPhotos):
            if message.media:
                downlaod_counter += 1
                print(f"Downloaded media: {downlaod_counter}", end="\r")
                client.download_media(message, download_folder_path)
                sleep(0.25)
        print(f"Downloaded media: {downlaod_counter}")

    # removing the session info from the local folder
    session_path = f"./{session_name}.session"
    if path.exists(session_path):
        remove(session_path)


if __name__ == "__main__":
    main()
