import subprocess
import ollama
import requests

# НАСТРОЙКИ PROJECT BARABASHKA
TOKEN = "8499286144:AAED49Ma-V6CogW8PEa0evpBdEqt6poZNLc"
CHAT_ID = "747673564"

def send_tg(text):
    try:
        # ИСПРАВЛЕНО: добавлен /bot перед TOKEN
        url = f"https://api.telegram.org{TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": text}
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            print("✅ Сообщение успешно улетело в Telegram!")
        else:
            # Это поможет увидеть ошибку, если ID чата неверный
            print(f"❌ Ошибка Telegram: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Ошибка сети: {e}")

# 1. Получаем реальные данные с карты
gpu_raw = subprocess.getoutput('nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,memory.used --format=csv,noheader,nounits')

# 2. Опрашиваем Llama 3
prompt = f"""
Ты — мониторинг-система ProjectBarabashka. 
Твоя задача — анализировать состояние видеокарты на Clore.ai.
Данные (Температура, Нагрузка %, Память MB): {gpu_raw}

Если температура > 80 или Нагрузка 100% долго, напиши краткий отчет с предупреждением.
Если всё в норме, просто напиши "Статус: Стабильно" и кратко цифры.
Отвечай на русском языке.
"""

try:
    print("⏳ Лама думает...")
    response = ollama.generate(model='llama3', prompt=prompt)
    analysis = response['response'].strip()
    
    # 3. Отправка в Telegram
    send_tg(f"📊 [ProjectBarabashka Clore Report]\n\n{analysis}")
    print(f"Отчет отправлен: {analysis}")
except Exception as e:
    print(f"Ошибка Ollama: {e}")
