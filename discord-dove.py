import discord
import logging
from discord.ext import commands
from discord.ext import tasks
from telegram import Bot
from telegram.error import Unauthorized
from telegram.ext import Updater
from itertools import cycle

# Discord 봇 설정
discord_bot_token = "Discord Bot Token"
intents = discord.Intents.default()
intents.message_content = True
discord_bot = commands.Bot(command_prefix="!", intents=intents)

status = cycle(["상태 메시지1", "상태 메시지2"])

# Telegram 봇 설정
telegram_bot_token = 'Telegram Bot Token'
telegram_bot = Bot(token=telegram_bot_token)
telegram_chat_id = 'Telegram Chat ID'

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('my_logger')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

for handler in logging.root.handlers:
    handler.setFormatter(formatter)

@discord_bot.event
async def on_ready():
    logger.info(f"Discord 봇 {discord_bot.user.name} 로그인 성공!")
    change_status.start()

@discord_bot.event
async def on_message(message):
    if message.author.id == "Discord User ID":
        try:
            if message.content:
                telegram_bot.send_message(chat_id=telegram_chat_id, text=message.content)
                logger.info(f"텔레그램 메시지 전송 성공: {message.content}")
            for attachment in message.attachments:
                if attachment.content_type.startswith('image'):
                    telegram_bot.send_photo(chat_id=telegram_chat_id, photo=attachment.url)
                    logger.info("텔레그램 이미지 전송 성공")
        except Unauthorized:
            logger.info("Telegram 봇이 채팅에 메시지를 보낼 권한이 없습니다.")
    await discord_bot.process_commands(message)

@tasks.loop(seconds=10)
async def change_status():
    await discord_bot.change_presence(activity=discord.Game(next(status)))

discord_bot.run(discord_bot_token)
updater = Updater(token=telegram_bot_token, use_context=True)
updater.start_polling()
updater.idle()