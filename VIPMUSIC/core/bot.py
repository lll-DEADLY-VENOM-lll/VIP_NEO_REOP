import asyncio
import pyrogram
import pyromod.listen  # noqa
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
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

        # --- LOG GROUP CHECK ---
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

        # --- SETTING CLEAN COMMANDS ---
        if config.SET_CMDS:
            try:
                # Sirf Basic Commands (Private Chat ke liye)
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "Start the bot"),
                        BotCommand("help", "Get help menu"),
                        BotCommand("ping", "Check bot status"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )

                # Sirf Music Commands (Group Admins ke liye)
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "Play requested song"),
                        BotCommand("vplay", "Play video song"),
                        BotCommand("pause", "Pause music"),
                        BotCommand("resume", "Resume music"),
                        BotCommand("skip", "Skip track"),
                        BotCommand("stop", "Stop music"),
                        BotCommand("queue", "Check song queue"),
                        BotCommand("settings", "Bot settings"),
                        BotCommand("reload", "Reload admin list"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set bot commands: {e}")

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")

    async def stop(self):
        await super().stop()
