import asyncio
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
from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden

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
            plugins=dict(root="VIPMUSIC.plugins"),
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        self.mention = get_me.mention

        button = InlineKeyboardMarkup([[InlineKeyboardButton(text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏", url=f"https://t.me/{self.username}?startgroup=true")]])

        # --- LOG GROUP ---
        if config.LOG_GROUP_ID:
            try:
                log_group_id = int(config.LOG_GROUP_ID)
                await self.send_photo(
                    chat_id=log_group_id,
                    photo=config.START_IMG_URL,
                    caption=f"╔════❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱════❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭ᴇᴅ 𝐁𝐚𝐛𝐲🎉\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨ʀ 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
            except Exception as e:
                LOGGER(__name__).error(f"Log Group Error: {e}")

        # --- EXTRA COMMANDS LIST ---
        if config.SET_CMDS:
            try:
                # 1. Commands for Everyone in Private
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "Bot ko start karein"),
                        BotCommand("help", "Help menu dekhein"),
                        BotCommand("ping", "Bot ki speed check karein"),
                        BotCommand("id", "Apni ID jaaniye"),
                        BotCommand("repo", "Bot ka source code"),
                        BotCommand("stats", "Bot ke stats dekhein"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )

                # 2. Commands for Group Admins (The Big List)
                await self.set_bot_commands(
                    commands=[
                        # Music
                        BotCommand("play", "Gaana bajayein (Audio)"),
                        BotCommand("vplay", "Video gaana bajayein"),
                        BotCommand("pause", "Gaana rokein"),
                        BotCommand("resume", "Gaana wapas chalayein"),
                        BotCommand("skip", "Agla gaana bajayein"),
                        BotCommand("stop", "Music band karein"),
                        BotCommand("queue", "Gaanon ki list dekhein"),
                        BotCommand("playlist", "Apni playlist chalayein"),
                        
                        # Admin Tools
                        BotCommand("settings", "Bot settings manage karein"),
                        BotCommand("reload", "Admin list update karein"),
                        BotCommand("ban", "User ko ban karein"),
                        BotCommand("unban", "User ko unban karein"),
                        BotCommand("mute", "User ko mute karein"),
                        BotCommand("unmute", "User ko unmute karein"),
                        BotCommand("purge", "Messages delete karein"),
                        
                        # Tagging & Fun
                        BotCommand("tagall", "Sabko mention karein"),
                        BotCommand("vctag", "Voice Chat ke liye tag karein"),
                        BotCommand("stopvctag", "Tagging rokein"),
                        BotCommand("shayari", "Ek shayari sunein"),
                        BotCommand("joke", "Ek joke sunein"),
                        BotCommand("love", "Love percentage check karein"),
                        BotCommand("gali", "Fun reply (Masti)"),
                        
                        # Search
                        BotCommand("song", "Gaana download karein"),
                        BotCommand("video", "Video download karein"),
                        BotCommand("lyrics", "Gaanon ke lyrics"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set extra commands: {e}")

        LOGGER(__name__).info(f"VIP Music Bot Started: {self.name}")

    async def stop(self):
        await super().stop()
