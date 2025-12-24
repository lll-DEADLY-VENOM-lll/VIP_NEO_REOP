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

links = {}

@app.on_callback_query(filters.regex("unban_userbot"))
async def unban_assistant_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    userbot = await get_assistant(chat_id)

    try:
        await app.unban_chat_member(chat_id, userbot.id)
        await callback_query.answer(
            "Assistant unbanned successfully✅\nJoining group...⌛", show_alert=True
        )

        if callback_query.message.chat.username:
            invitelink = callback_query.message.chat.username
            try:
                await userbot.resolve_peer(invitelink)
                await asyncio.sleep(1)
                await userbot.join_chat(invitelink)
                await callback_query.message.reply_text(
                    "**Assistant has successfully joined the group. Now you can play songs✅**"
                )
            except Exception:
                await callback_query.message.reply_text(
                    f"**Failed to invite assistant. Please add @{userbot.username} manually.**"
                )
        else:
            try:
                invitelink = await client.export_chat_invite_link(chat_id)
                await asyncio.sleep(1)
                await userbot.join_chat(invitelink)
            except Exception:
                await callback_query.message.reply_text(
                    f"**Make bot admin to invite assistant @{userbot.username}**"
                )
    except Exception as e:
        await callback_query.answer(f"Error: {e}", show_alert=True)


def PlayWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        if message.sender_chat:
            upl = InlineKeyboardMarkup([[InlineKeyboardButton(text="ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]])
            return await message.reply_text(_["general_4"], reply_markup=upl)

        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.",
                    disable_web_page_preview=True,
                )

        if PRIVATE_BOT_MODE == str(True):
            if not await is_served_private_chat(message.chat.id):
                await message.reply_text("**ᴘʀɪᴠᴀᴛᴇ ᴍᴜsɪᴄ ʙᴏᴛ**\n\nOnly for authorized chats.")
                return await app.leave_chat(message.chat.id)

        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass

        audio_telegram = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
        video_telegram = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
        url = await YouTube.url(message)

        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                buttons = botplaylist_markup(_)
                return await message.reply_photo(photo=PLAYLIST_IMG_URL, caption=_["playlist_1"], reply_markup=InlineKeyboardMarkup(buttons))

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

        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins or message.from_user.id not in admins:
                    return await message.reply_text(_["play_4"])

        # --- AUDIO/VIDEO LOGIC FIX ---
        cmd = message.command[0].lower()
        if cmd.startswith("v") or "-v" in message.text:
            video = True    # Video Mode for vplay
        else:
            video = False   # Strict Audio Mode for play
        
        fplay = True if cmd.endswith("e") else None
        # -----------------------------

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(message.chat.id)

            # --- PEER_ID_INVALID CRASH FIX ---
            try:
                common_chats = await userbot.get_common_chats(app.id)
                if chat_id in [chat.id for chat in common_chats]:
                    return await command(client, message, _, chat_id, video, channel, playmode, url, fplay)
            except Exception:
                common_chats = []
            # ---------------------------------

            try:
                get = await app.get_chat_member(chat_id, userbot.id)
            except UserNotParticipant:
                try:
                    if message.chat.username:
                        await userbot.join_chat(message.chat.username)
                    else:
                        invitelink = await client.export_chat_invite_link(chat_id)
                        await userbot.join_chat(invitelink)
                except Exception:
                    return await message.reply_text(f"**Assistant @{userbot.username} join nahi kar paa raha. Use manually add karein aur admin banayein.**")
            except Exception:
                pass

        return await command(client, message, _, chat_id, video, channel, playmode, url, fplay)

    return wrapper