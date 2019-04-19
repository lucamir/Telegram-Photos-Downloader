from telethon import TelegramClient
import telethon.sync
from telethon.tl.types import InputMessagesFilterPhotos
import asyncio
import socks

api_id = 3789173321 #REPLACE THE EXAMPLE NUMBER WITH YOUR API ID CODE 
api_hash = '#PUT_YOUR_API_HASH_CODE_HERE'
session_name = 'my_session' #YOU CAN REPLACE THIS STRING WITH A CUSTOM SESSION NAME

def main():
    # download counter
    downlaod_counter = 0

    # name of the conversation from which you want to download the photos
    conversation_name = '#PUT_YOUR_CONVERSATION_NAME_HERE'
    
    # creation of a client and start the session with your personal API ID AND HASH CODE
    client = TelegramClient(session_name, api_id, api_hash)

    # start the client
    client.start()

    # get all the conversations
    dialogs = client.get_dialogs()

    # variable that will contain the conversation
    chat = None

    # loop for get from all the conversation the selected one
    for dialog in dialogs:
        if dialog.name == conversation_name:
            chat = dialog
            break

    # loop for get from all the messages of the selected conversation just the message that contains photos
    for message in client.iter_messages(chat,filter=InputMessagesFilterPhotos):
        downlaod_counter+=1
        if message.media:
            print ("Downloading media: ",downlaod_counter)
            client.download_media(message)

if __name__ == '__main__':
    main()
