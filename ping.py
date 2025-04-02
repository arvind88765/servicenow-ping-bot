import os
import requests
from requests.auth import HTTPBasicAuth
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# Get the sensitive information from environment variables (set in Glitch secrets)
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN'] # Set in Glitch secrets
SN_URL = "https://dev192981.service-now.com/sp"  # Replace with your instance URL
SN_USERNAME = os.environ['SN_USERNAME']  # Set in Glitch secrets
SN_PASSWORD = os.environ['SN_PASSWORD']  # Set in Glitch secrets

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
def wake_up(update, context):
    ping_servicenow()
    update.message.reply_text("✅ Wake-up call sent to your PDI!")

# Set up the Telegram bot
updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add the /wake_up command to the bot
dispatcher.add_handler(CommandHandler('wake_up', wake_up))

# Schedule a background job to ping ServiceNow every 12 hours
scheduler = BackgroundScheduler()
scheduler.add_job(ping_servicenow, 'interval', hours=12)
scheduler.start()

# Start the bot
updater.start_polling()
print("🤖 Bot is running...")
