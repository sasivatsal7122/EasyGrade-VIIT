import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

def telesendmsg(message,user_name):
    api_id = '9996836'
    api_hash = '373e9aa46c20e103167c5016d46a29a2'
    token = '5263589450:AAHwqvfkwmuhQZzoxaUsNM6SdTwETYcIgDc'

    phone = '+91 6281314789'
    client = TelegramClient('session', api_id, api_hash)

    client.connect()
    client.is_user_authorized()

    if not client.is_user_authorized():
        client.send_code_request(phone)  
        client.sign_in(phone, input('Enter the code: '))
    try:
        receiver = client.get_input_entity(f'https://t.me/{user_name}')
        client.send_message(receiver, message, parse_mode='html')
    except Exception as e:	
        print(e)

    client.disconnect()
