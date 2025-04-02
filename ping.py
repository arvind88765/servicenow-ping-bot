import requests
from requests.auth import HTTPBasicAuth
from telegram import Update
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import os
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Hardcode the bot token and ServiceNow credentials directly
TELEGRAM_API_TOKEN = "7625747331:AAGR3LBP7PtCaomy7s30vCrTvGjjOYuhYTY"  # Your bot token
SN_USERNAME = "admin"  # Your ServiceNow username
SN_PASSWORD = "4n8b!jXCbEG@"  # Your ServiceNow password
SN_URL = "https://dev192981.service-now.com/sp"  # Your ServiceNow instance URL

# Function to ping ServiceNow PDI to keep it active
def ping_servicenow():
    try:
        response = requests.get(SN_URL, auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD))
        if response.status_code == 200:
            print("✅ PDI is active.")
        else:
            print(f"❌ Error pinging PDI: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")

# Command handler for /wake_up to trigger a manual wake-up
async def wake_up(update: Update, context):
    ping_servicenow()
    await update.message.reply_text("✅ Wake-up call sent to your PDI!")

# Set up the Telegram bot (updated for python-telegram-bot v20+)
async def main():
    # Create the application (bot) instance
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Add the /wake_up command to the bot
    application.add_handler(CommandHandler('wake_up', wake_up))

    # Schedule a background job to ping ServiceNow every 12 hours
    scheduler = BackgroundScheduler()
    scheduler.add_job(ping_servicenow, 'interval', hours=12)
    scheduler.start()

    # Start the bot (handles event loop internally)
    await application.run_polling()

# Run the bot using asyncio.run() (handled with nest_asyncio)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # This will run the bot with a patched event loop
