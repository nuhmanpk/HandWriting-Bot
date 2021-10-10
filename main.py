
# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message
import os
import requests

bughunter0 = Client(
    "Handwriting",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
)


@bughunter0.on_message(filters.text)
async def text(bot, message):
    text = str(message.text)
    chat_id = int(message.chat.id)
    file_name = f"{message.chat.id}.jpg"
    length = len(text)
    if length < 500:
        txt = await message.reply_text("Converting to handwriting...")
        rgb = [0, 0, 0] # Edit RGB values here to change the Ink color
        try:
            # Can directly use pywhatkit module for this
            data = requests.get(
                "https://pywhatkit.herokuapp.com/handwriting?text=%s&rgb=%s,%s,%s"
                % (text, rgb[0], rgb[1], rgb[2])
            ).content
        except Exception as error:
            await message.reply_text(f"{error}")
            return
        with open(file_name, "wb") as file:
            file.write(data)
            file.close()
        await txt.edit("Uploading...")
        await bot.send_photo(
            chat_id=chat_id,
            photo=file_name,
            caption="Join @BugHunterBots"
        )
        await txt.delete()
        os.remove(file_name)
    else:
        await message.reply_text("Please don't do It")


bughunter0.run()

