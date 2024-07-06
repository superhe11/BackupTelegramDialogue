from telethon import TelegramClient, events
from telethon.tl.types import InputPeerUser, InputPeerChannel
import asyncio
import time

# Функция для чтения конфиг-файла
def read_config(filename):
    config = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.strip().split(' = ')
            config[key] = value.strip("'\"")
    return config

config = read_config('config.txt')

api_id = config['api_id']
api_hash = config['api_hash']
phone_number = config['phone_number']
your_id = config['your_id']
friend_id = config['friend_id']
channel_id = config['channel_id']
your_prefix = config['your_prefix']
friend_prefix = config['friend_prefix']

client = TelegramClient('session', api_id, api_hash)

sent_messages = {}

@client.on(events.NewMessage(chats=[int(your_id), int(friend_id)]))
async def handler(event):
    global sent_messages
    
    sender = await event.get_sender()
    message_id = event.id

    if message_id in sent_messages:
        return

    if sender.id == int(your_id):
        prefix = your_prefix
    elif sender.id == int(friend_id):
        prefix = friend_prefix
    else:
        return  

    message = prefix + event.text
    
    channel = await client.get_entity(int(channel_id))
    await client.send_message(channel, message)
    sent_messages[message_id] = time.time()
    current_time = time.time()
    sent_messages = {k: v for k, v in sent_messages.items() if current_time - v < 300}
    if sender.id == int(friend_id):
        await client.send_read_acknowledge(sender, event.message)
        raise events.StopPropagation

async def main():
    await client.start(phone=phone_number)
    print("Клиент запущен")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())