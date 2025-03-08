import os
import asyncio
import logging
import logging.config
from datetime import datetime
from pytz import timezone
from aiohttp import web
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from plugins.web_support import web_server  # Your web server file
import pyromod

# Configure logging
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="SnowEncoderBot",
            in_memory=True,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={'root': 'plugins'}
        )

    async def keep_alive(self):
        """Sends a message every 30 minutes to keep the bot active."""
        while True:
            await asyncio.sleep(1800)  # 30 minutes
            try:
                await self.send_message(Config.ADMIN, "✅ Bot is still running!")
                logging.info("✅ Sent keep-alive message to admin.")
            except Exception as e:
                logging.error(f"⚠️ Keep-alive message failed: {e}")

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        # Start the web server
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()

        logging.info(f"✅ {me.first_name} started on {Config.KOYEB_URL}")

        await self.send_message(
            Config.ADMIN,
            f"✅ **Bot Started Successfully!**\n"
            f"🌍 **URL:** {Config.KOYEB_URL}"
        )

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"**{me.mention} restarted!**\n"
                    f"📅 **Date:** `{date}`\n"
                    f"⏰ **Time:** `{time}`\n"
                    f"🌐 **Timezone:** `Asia/Kolkata`\n"
                    f"🉐 **Version:** `v{__version__} (Layer {layer})`"
                )
            except Exception as e:
                logging.warning("⚠️ Make sure bot is admin in LOG_CHANNEL: " + str(e))

        # Start keep-alive task
        asyncio.create_task(self.keep_alive())

    async def stop(self, *args):
        await super().stop()
        logging.info("⛔ Bot Stopped.")

bot = Bot()
bot.run()
