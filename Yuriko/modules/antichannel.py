import html

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.filters import Filters

from Yuriko.modules.helper_funcs.anonymous import AdminPerms, user_admin
from Yuriko.modules.helper_funcs.decorators import emikocmd, emikomsg
from Yuriko.modules.sql.antichannel_sql import (
    antichannel_status,
    disable_antichannel,
    enable_antichannel,
)


@emikocmd(command="antichannel", group=100)
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html(
                "Enabled antichannel in {}".format(html.escape(chat.title))
            )
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html(
                "Disabled antichannel in {}".format(html.escape(chat.title))
            )
        else:
            message.reply_text("Unrecognized arguments {}".format(s))
        return
    message.reply_html(
        "Antichannel setting is currently {} in {}".format(
            antichannel_status(chat.id), html.escape(chat.title)
        )
    )


@emikomsg(Filters.chat_type.groups, group=110)
def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if (
        message.sender_chat
        and message.sender_chat.type == "channel"
        and not message.is_automatic_forward
    ):
        message.delete()
        sender_chat = message.sender_chat
        bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)

__mod_name__ = "Aɴᴛɪ-Cʜᴀɴɴᴇʟ"

__help__ = """
Commands

✗ /antichannel on - `to on antichannel.`

✗ /antichannel off - `to of antichannel`

*✗ Pᴏᴡᴇʀᴇᴅ 💕 Bʏ: BᴏᴛDᴜɴɪʏᴀ!*
"""
