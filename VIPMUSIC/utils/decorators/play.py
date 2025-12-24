# Copyright (C) 2024 by VISHAL-PANDEY@Github, < https://github.com/vishalpandeynkp1 >.
#
# This file is part of < https://github.com/vishalpandeynkp1/VIPNOBITAMUSIC_REPO > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/vishalpandeynkp1/VIPNOBITAMUSIC_REPO/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import PLAYLIST_IMG_URL, PRIVATE_BOT_MODE
from config import SUPPORT_GROUP as SUPPORT_CHAT
from config import adminlist
from strings import get_string
from VIPMUSIC import YouTube, app
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_served_private_chat,
)
from VIPMUSIC.utils.inline import botplaylist_markup

def PlayWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        # Anonymous Admin Check
        if message.sender_chat:
            upl = InlineKeyboardMarkup([[InlineKeyboardButton(text="ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]])
            return await message.reply_text(_["general_4"], reply_markup=upl)

        # Maintenance Check
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.", disable_web_page_preview=True)

        # Private Mode Check
        if PRIVATE_BOT_MODE == str(True):
            if not await is_served_private_chat(message.chat.id):
                await message.reply_text("**ᴘʀɪᴠᴀᴛᴇ ᴍᴜsɪᴄ ʙᴏᴛ**\n\nOnly for authorized chats.")
                return await app.leave_chat(message.chat.id)

        # Command Delete Logic
        if await is_commanddelete_on(message.chat.id):
            try: await message.delete()
            except: pass

        # Input Check
        audio_telegram = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
        video_telegram = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
        url = await YouTube.url(message)

        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                buttons = botplaylist_markup(_)
                return await message.reply_photo(photo=PLAYLIST_IMG_URL, caption=_["playlist_1"], reply_markup=InlineKeyboardMarkup(buttons))

        # Channel Play Logic
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None: return await message.reply_text(_["setting_12"])
            try: chat = await app.get_chat(chat_id)
            except: return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)

        # Admin Auth Check
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins or message.from_user.id not in admins:
                    return await message.reply_text(_["play_4"])

        # --- AUDIO/VIDEO SEPARATION LOGIC ---
        # Agar command vplay hai ya -v likha hai toh Video, warna sirf Audio
        command_name = message.command[0].lower()
        if "vplay" in command_name or "-v" in message.text:
            video = True
        else:
            video = None # "None" means Audio-only in VIP core
        
        fplay = True if command_name.endswith("e") else None
        # ------------------------------------

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(message.chat.id)

            # PeerIdInvalid Fix
            try:
                common_chats = await userbot.get_common_chats(app.id)
                if chat_id in [chat.id for chat in common_chats]:
                    return await command(client, message, _, chat_id, video, channel, playmode, url, fplay)
            except:
                pass 

            # Join Logic
            try:
                await app.get_chat_member(chat_id, userbot.id)
            except UserNotParticipant:
                try:
                    if message.chat.username:
                        await userbot.join_chat(message.chat.username)
                    else:
                        invitelink = await client.export_chat_invite_link(chat_id)
                        await userbot.join_chat(invitelink)
                except:
                    return await message.reply_text(f"**Assistant @{userbot.username} cannot join. Add manually.**")
            except: pass

        return await command(client, message, _, chat_id, video, channel, playmode, url, fplay)

    return wrapper