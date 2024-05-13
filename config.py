import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID_MAINNET = os.getenv("CHAT_ID_MAINNET")
CHAT_ID_TESTNET = os.getenv("CHAT_ID_TESTNET")
