import requests
from config import TOKEN, CHAT_ID_MAINNET, CHAT_ID_TESTNET

def send_telegram_message(message, voted, network_type):
    # Определяем ID чата в зависимости от типа сети
    chat_id = CHAT_ID_MAINNET if network_type == 'mainnet' else CHAT_ID_TESTNET
    # Выбираем эмодзи в зависимости от статуса голосования
    vote_emoji = "🟢" if voted == "Yes" else "🔴"
    # Добавляем эмодзи к сообщению
    full_message = f"{vote_emoji} {message}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': full_message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Сообщение успешно отправлено")
    except Exception as e:
        print(f"Не удалось отправить сообщение: {str(e)}")
