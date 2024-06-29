import requests
from config import TOKEN, CHAT_ID_MAINNET, CHAT_ID_TESTNET

def send_telegram_message(message, network_type):
    # Определяем ID чата в зависимости от типа сети
    chat_id = CHAT_ID_MAINNET if network_type == 'mainnet' else CHAT_ID_TESTNET
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"Сообщение успешно отправлено в чат '{network_type}'")
    except Exception as e:
        print(f"Не удалось отправить сообщение в чат '{network_type}': {str(e)}")