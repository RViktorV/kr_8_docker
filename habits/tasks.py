import requests

def send_telegram_message(chat_id, message):
    token = 'YOUR_TELEGRAM_BOT_TOKEN'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Можно использовать HTML или Markdown для форматирования текста
    }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return f"Сообщение отправлено: {message}"
    else:
        return f"Ошибка отправки сообщения: {response.text}"