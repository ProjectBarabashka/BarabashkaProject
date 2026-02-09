import subprocess
import ollama
import requests

# НАСТРОЙКИ PROJECT BARABASHKA
TOKEN = "8499286144:AAED49Ma-V6CogW8PEa0evpBdEqt6poZNLc"
CHAT_ID = "747673564"

def send_tg(text):
    try:
        # ИСПРАВЛЕНО: Добавлен /bot перед токеном
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": text}
        # ИСПРАВЛЕНО: Добавлен реальный запрос к серверу
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

# 1. Получаем реальные данные с видеокарты
try:
    gpu_raw = subprocess.getoutput('nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,memory.used --format=csv,noheader,nounits')
except Exception as e:
    gpu_raw = "Ошибка получения данных GPU"

# 2. Опрашиваем Llama 3
prompt = f"""
Ты — мониторинг-система ProjectBarabashka. 
Твоя задача — анализировать состояние видеокарты, которую мы сдаем в аренду на Clore.ai.
Данные (Температура, Нагрузка %, Память MB): {gpu_raw}

Если температура > 80 или Нагрузка 100% долго, напиши краткий отчет с предупреждением.
Если всё в норме, просто напиши "Статус: Стабильно" и кратко цифры.
Отвечай на русском языке.
"""

try:
    response = ollama.generate(model='llama3', prompt=prompt)
    analysis = response['response'].strip()
    
    # 3. Отправка отчета в Telegram
    send_tg(f"📊 [ProjectBarabashka Clore Report]\n\n{analysis}")
    print(f"Отчет успешно отправлен: {analysis}")
except Exception as e:
    print(f"Ошибка Ollama: {e}")
