from os import mkdir, path, remove
from time import sleep

import telethon.sync
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos

SESSION_NAME = "download_media"  # YOU CAN REPLACE THIS STRING WITH A CUSTOM SESSION NAME
OUTPUT_FOLDER = "./downloaded-media"  # YOU CAN REPLACE THIS STRING WITH A CUSTOM FOLDER PATH


def find_chat(chats, chat_name):
    for chat in chats:
        if chat.name == chat_name:
            return chat


def input_chat_name(chats):
    print("\nWrite the chat name from which you want to downlaod the media or exit for close the program\n")
    while True:
        chat_name = input("Please enter the chat name: ")
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
    print("\nI need some info for create the connection...\n")

    try:
        API_ID = int(input("Please enter your API ID: "))
        API_HASH = input("Please enter your API HASH: ")
        # creation of a client and start the session with your personal API ID AND HASH CODE
        with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
            client.start()  # start the client
            chats = client.get_dialogs()  # get all the conversations

            # name of the conversation from which you want to download the photos
            chat_name = input_chat_name(chats)

            chat = find_chat(chats, chat_name)  # find the selected chat

            if not path.exists(OUTPUT_FOLDER):
                mkdir(OUTPUT_FOLDER)

            downlaod_counter = 0

            # loop for get from all the messages of the selected conversation just the message that contains photos
            for message in client.iter_messages(chat, filter=InputMessagesFilterPhotos):
                if message.media:
                    downlaod_counter += 1
                    print(f"Downloaded media: {downlaod_counter}", end="\r")
                    client.download_media(message, OUTPUT_FOLDER)
                    sleep(0.25)
            print(f"Downloaded media: {downlaod_counter}")

        # removing the session info from the local folder
        session_path = f"./{SESSION_NAME}.session"
        if path.exists(session_path):
            remove(session_path)

    except Exception as e:
        print(f"[Error]: {e}")


if __name__ == "__main__":
    main()
