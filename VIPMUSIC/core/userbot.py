# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.

from typing import Callable, Optional
import pyrogram
from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []
clients = []

class Userbot(Client):
    def __init__(self):
        self.one = Client("VIPString1", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING1))
        self.two = Client("VIPString2", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING2))
        self.three = Client("VIPString3", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING3))
        self.four = Client("VIPString4", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING4))
        self.five = Client("VIPString5", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING5))

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistant Clients")
        
        # --- ASSISTANT 1 ---
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("GOD_HYPER_O_P")
                await self.one.join_chat("ABOUT_VENOM_OP")
                await self.one.join_chat("NEO_BOT_SUPPORT")
                await self.one.join_chat("FEELING_SMILEY")
            except: pass
            
            assistants.append(1)
            clients.append(self.one)
            
            # LOG GROUP FIX: Message bhejne ki koshish karega, fail hua toh skip karega
            if config.LOG_GROUP_ID:
                try:
                    await self.one.send_message(config.LOG_GROUP_ID, "Assistant 1 Started")
                except Exception as e:
                    LOGGER(__name__).warning(f"Assistant 1 log failed (Skipped): {e}")

            get_me = await self.one.get_me()
            self.one.id, self.one.username, self.one.mention = get_me.id, get_me.username, get_me.mention
            self.one.name = f"{get_me.first_name} {get_me.last_name or ''}"
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")

        # --- ASSISTANT 2 ---
        if config.STRING2:
            await self.two.start()
            assistants.append(2)
            clients.append(self.two)
            if config.LOG_GROUP_ID:
                try: await self.two.send_message(config.LOG_GROUP_ID, "Assistant 2 Started")
                except: pass
            get_me = await self.two.get_me()
            self.two.id, self.two.username = get_me.id, get_me.username
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant Two Started as {get_me.first_name}")

        # --- ASSISTANT 3 ---
        if config.STRING3:
            await self.three.start()
            assistants.append(3)
            clients.append(self.three)
            if config.LOG_GROUP_ID:
                try: await self.three.send_message(config.LOG_GROUP_ID, "Assistant 3 Started")
                except: pass
            get_me = await self.three.get_me()
            self.three.id, self.three.username = get_me.id, get_me.username
            assistantids.append(get_me.id)

        # --- ASSISTANT 4 ---
        if config.STRING4:
            await self.four.start()
            assistants.append(4)
            clients.append(self.four)
            get_me = await self.four.get_me()
            self.four.id = get_me.id
            assistantids.append(get_me.id)

        # --- ASSISTANT 5 ---
        if config.STRING5:
            await self.five.start()
            assistants.append(5)
            clients.append(self.five)
            get_me = await self.five.get_me()
            self.five.id = get_me.id
            assistantids.append(get_me.id)

def on_cmd(filters: Optional[pyrogram.filters.Filter] = None, group: int = 0) -> Callable:
    def decorator(func: Callable) -> Callable:
        for client in clients:
            client.add_handler(pyrogram.handlers.MessageHandler(func, filters), group)
        return func
    return decorator
