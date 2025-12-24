# Copyright (C) 2024 by VISHAL-PANDEY@Github, < https://github.com/vishalpandeynkp1 >.
#
# This file is part of < https://github.com/vishalpandeynkp1/VIPNOBITAMUSIC_REPO > project,
# and is released under the "GNU v3.0 License Agreement".

import uvloop
uvloop.install()

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
        LOGGER(__name__).info(f"Starting Bot...")
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
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        self.mention = get_me.mention

        # --- Log Group ID ko safely Integer mein convert karna ---
        if config.LOG_GROUP_ID:
            try:
                LOGGER_ID = int(config.LOG_GROUP_ID)
            except ValueError:
                LOGGER(__name__).error("LOG_GROUP_ID invalid hai! Yeh sirf numbers mein hona chahiye (e.g. -100xxx).")
                LOGGER_ID = None
        else:
            LOGGER_ID = None

        # Create the button
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        # Start Message sending logic
        if LOGGER_ID:
            try:
                await self.send_photo(
                    LOGGER_ID,
                    photo=config.START_IMG_URL,
                    caption=f"╔════❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱════❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲🎉\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
            except Exception as e:
                LOGGER(__name__).error(f"Log group mein photo nahi bhej paya: {e}")
                try:
                    await self.send_message(
                        LOGGER_ID,
                        f"╔═══❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱═══❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲🎉\n║\n║◈ {self.name}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚══════════════❍⊱❁",
                        reply_markup=button,
                    )
                except Exception as ex:
                    LOGGER(__name__).error(f"Log group mein message bhi nahi gaya: {ex}")

        # Setting commands
        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "Start the bot"),
                        BotCommand("help", "Get the help menu"),
                        BotCommand("ping", "Check if the bot is alive"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "Start playing requested song"),
                        BotCommand("stop", "Stop the current song"),
                        BotCommand("pause", "Pause the current song"),
                        BotCommand("resume", "Resume the paused song"),
                        BotCommand("queue", "Check the queue"),
                        BotCommand("skip", "Skip the current song"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "❥ Start the bot"),
                        BotCommand("ping", "❥ Check the ping"),
                        BotCommand("help", "❥ Get help"),
                        BotCommand("vctag", "❥ Tag all for voice chat"),
                        BotCommand("stopvctag", "❥ Stop tagging for VC"),
                        BotCommand("tagall", "❥ Tag all members"),
                        BotCommand("settings", "❥ Get the settings"),
                        BotCommand("reload", "❥ Reload the bot"),
                        BotCommand("play", "❥ Play song"),
                        BotCommand("vplay", "❥ Play video"),
                        BotCommand("end", "❥ Empty the queue"),
                        BotCommand("stop", "❥ Stop the song"),
                        BotCommand("song", "❥ Download song"),
                        BotCommand("video", "❥ Download video"),
                        BotCommand("sudolist", "❥ Check the sudo list"),
                        BotCommand("gstats", "❥ Bot stats"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Commands set karne mein error: {e}")

        # Check Admin Status in Log Group
        if LOGGER_ID:
            try:
                chat_member_info = await self.get_chat_member(LOGGER_ID, self.id)
                if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).warning("Bot Logger Group mein Admin nahi hai! Kirpya admin banayein.")
            except Exception:
                LOGGER(__name__).error("Bot Logger Group ka member nahi hai ya ID galat hai.")

        LOGGER(__name__).info(f"MusicBot Started as {self.username}")

    async def stop(self):
        await super().stop()
        LOGGER(__name__).info("Bot Stopped.")
