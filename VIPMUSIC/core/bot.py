# Copyright (C) 2024 by VISHAL-PANDEY@Github, < https://github.com/vishalpandeynkp1 >.

import asyncio

# --- EVENT LOOP FIX ---
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import pyrogram
import pyromod.listen  # noqa
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config
from ..logging import LOGGER

class VIPBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "VIPMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        button = InlineKeyboardMarkup([[InlineKeyboardButton(text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏", url=f"https://t.me/{self.username}?startgroup=true")]])

        # Safe Log Group Check
        if config.LOG_GROUP_ID:
            try:
                await self.send_photo(
                    config.LOG_GROUP_ID,
                    photo=config.START_IMG_URL,
                    caption=f"╔════❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱════❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭ᴇᴅ 𝐁𝐚𝐛𝐲🎉\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨ʀ 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
            except Exception:
                LOGGER(__name__).error("Log Group access failed. Bot starting without logs.")

        # --- SETTING EXTRA COMMANDS ---
        if config.SET_CMDS:
            try:
                # Commands for Private Chats
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "Start the bot"),
                        BotCommand("help", "Get help menu"),
                        BotCommand("ping", "Check bot status"),
                        BotCommand("id", "Get your user ID"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )

                # Commands for Group Admins (FULL LIST)
                await self.set_bot_commands(
                    commands=[
                        # Music Commands
                        BotCommand("play", "Play requested song"),
                        BotCommand("vplay", "Play video song"),
                        BotCommand("pause", "Pause music"),
                        BotCommand("resume", "Resume music"),
                        BotCommand("skip", "Skip current track"),
                        BotCommand("stop", "Stop music & clear queue"),
                        BotCommand("queue", "Check song queue"),
                        BotCommand("lyrics", "Get song lyrics"),
                        BotCommand("song", "Download audio song"),
                        BotCommand("video", "Download video song"),
                        
                        # Management & Utility
                        BotCommand("settings", "Bot settings"),
                        BotCommand("reload", "Reload bot database"),
                        BotCommand("vctag", "Tag all for Voice Chat"),
                        BotCommand("stopvctag", "Stop VC tagging"),
                        BotCommand("tagall", "Mention all members"),
                        BotCommand("cancel", "Cancel ongoing tag"),
                        BotCommand("gstats", "Check global stats"),
                        BotCommand("repo", "Get bot repository"),
                        BotCommand("update", "Update the bot"),
                        
                        # Fun Commands
                        BotCommand("gali", "Fun reply"),
                        BotCommand("shayari", "Get a shayari"),
                        BotCommand("love", "Love status/shayari"),
                        BotCommand("joke", "Get a random joke"),
                        
                        # Sudo/Owner Only (Visible to Admins)
                        BotCommand("sudolist", "Check sudo users list"),
                        BotCommand("owner", "Check bot owner"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set bot commands: {e}")

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")
