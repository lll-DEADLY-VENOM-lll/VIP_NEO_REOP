import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import InviteRequestSent, UserAlreadyParticipant
from VIPMUSIC import app
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC.utils.database import get_assistant
from VIPMUSIC.utils.vip_ban import admin_filter

@app.on_message(
    filters.group & filters.command(["userbotjoin", "ujoin"]) & ~filters.private
)
async def join_group(client, message):
    chat_id = message.chat.id
    userbot = await get_assistant(chat_id)
    userbot_id = userbot.id
    
    done = await message.reply("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ... ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ**")
    
    # Check bot's status
    try:
        chat_member = await app.get_chat_member(chat_id, app.id)
    except Exception:
        return await done.edit("**ᴍᴜᴊʜᴇ ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴛᴀᴀᴋɪ ᴍᴀɪɴ ᴄʜᴇᴄᴋ ᴋᴀʀ sᴀᴋᴜɴ!**")

    # If Group has username (Public)
    if message.chat.username:
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**")
        except UserAlreadyParticipant:
            await done.edit_text("**✅ ᴀssɪsᴛᴀɴᴛ ᴘᴇʜʟᴇ sᴇ ʜɪ ɢʀᴏᴜᴘ ᴍᴇɪɴ ʜᴀɪ.**")
        except InviteRequestSent:
            await app.approve_chat_join_request(chat_id, userbot_id)
            await done.edit_text("**✅ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴇᴅ!**")
        except Exception:
            # Try unbanning if join fails
            if chat_member.status == ChatMemberStatus.ADMINISTRATOR:
                try:
                    await app.unban_chat_member(chat_id, userbot_id)
                    await userbot.join_chat(message.chat.username)
                    await done.edit_text("**ᴀssɪsᴛᴀɴᴛ ᴡᴀs ʙᴀɴɴᴇᴅ, ɴᴏᴡ ᴜɴʙᴀɴɴᴇᴅ ᴀɴᴅ ᴊᴏɪɴᴇᴅ!**")
                except Exception as e:
                    await done.edit_text(f"**Error:** `{e}`")
            else:
                await done.edit_text("**ᴍᴜᴊʜᴇ ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ (ʙᴀɴ ᴘᴏᴡᴇʀ ᴋᴇ sᴀᴀᴛʜ) ᴛᴀᴀᴋɪ ᴍᴀɪɴ ᴀssɪsᴛᴀɴᴛ ᴋᴏ ʟᴀᴀ sᴀᴋᴜɴ.**")

    # If Group is Private
    else:
        if chat_member.status != ChatMemberStatus.ADMINISTRATOR:
            return await done.edit_text("**ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘ ᴍᴇɪɴ ᴀssɪsᴛᴀɴᴛ ᴋᴏ ʙᴜʟᴀɴᴇ ᴋᴇ ʟɪʏᴇ ᴍᴜᴊʜᴇ ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ!**")
        
        try:
            invite_link = await app.export_chat_invite_link(chat_id)
            await userbot.join_chat(invite_link)
            await done.edit_text("**✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴠɪᴀ ʟɪɴᴋ.**")
        except UserAlreadyParticipant:
            await done.edit_text("**✅ ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ʜᴇʀᴇ.**")
        except Exception as e:
            await done.edit_text(f"**ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ:** `{e}`")

@app.on_message(filters.command("userbotleave") & filters.group & admin_filter)
async def leave_one(client, message):
    userbot = await get_assistant(message.chat.id)
    try:
        await userbot.leave_chat(message.chat.id)
        await message.reply_text("**✅ ᴀssɪsᴛᴀɴᴛ ʟᴇғᴛ ᴛʜɪs ᴄʜᴀᴛ.**")
    except Exception as e:
        await message.reply_text(f"**Error:** `{e}`")

@app.on_message(filters.command(["leaveall"]) & SUDOERS)
async def leave_all(client, message):
    left = 0
    failed = 0
    lol = await message.reply("🔄 **ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠɪɴɢ ᴀʟʟ ᴄʜᴀᴛs...**")
    userbot = await get_assistant(message.chat.id)
    
    async for dialog in userbot.get_dialogs():
        try:
            await userbot.leave_chat(dialog.chat.id)
            left += 1
            await asyncio.sleep(1)
        except Exception:
            failed += 1
            
    await lol.edit(f"**✅ ʟᴇғᴛ:** `{left}`\n**❌ ғᴀɪʟᴇᴅ:** `{failed}`")
