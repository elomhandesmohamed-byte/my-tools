from telethon import TelegramClient, events

api_id = 31959459
api_hash = "PUT_YOUR_API_HASH_HERE"

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # يرد بس في الخاص
    if not event.is_private:
        return

    sender = await event.get_sender()
    name = sender.first_name if sender.first_name else "صديقي"

    await event.reply(f"{name}، دراك غير متصل ❌\nاترك رسالتك وسيتم الرد في أقرب وقت ⏳")

print("Userbot is running...")

client.start()
client.run_until_disconnected()
