
# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import requests

HWBot = Client(
    "Handwriting",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
)

HOME_TEXT = "<b>Hey  [{}](tg://user?id={}) 🙋‍♂️\n\nIam A Bot Built To Hand Write In Telegram.\nSend me a text to convert it Handwriting.</b>"
admin_filter=filters.create(is_admin) 

@HWBot.on_message(filters.command(['start', f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    buttons = [
        [
            InlineKeyboardButton('⚙️ Update Channel', url='https://t.me/SLBotsOfficial'),
            InlineKeyboardButton('🧩 Support Group', url='https://t.me/trtechguide')
        ],
        [
            InlineKeyboardButton('👨🏼‍🦯 Help', callback_data='help'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)

@HWBot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ Creator : <a href='https://t.me/TharukRenuja'>Tharuk Renuja</a>\n○ Source Code : <a href='https://github.com/TharukRenuja/HandWriting-Bot'>Click here</a>\n○ Channel : @SLBotsOfficial\n○ Support Group : @trtechguide</b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass


@HWBot.on_message(filters.text)
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
            caption="Join @SLBotsOfficial"
        )
        await txt.delete()
        os.remove(file_name)
    else:
        await message.reply_text("Please don't do It")


HWBot.run()

