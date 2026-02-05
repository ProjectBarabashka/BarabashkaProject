import subprocess
import ollama

def get_gpu_status():
    # Берем данные о температуре и нагрузке видеокарты
    result = subprocess.check_output(['nvidia-smi', '--query-gpu=temperature.gpu,utilization.gpu', '--format=csv,noheader,nounits'])
    return result.decode('utf-8')

gpu_data = get_gpu_status()
prompt = f"Вот текущее состояние моей видеокарты на Clore.ai: {gpu_data}. Есть ли повод для беспокойства? Ответь кратко."

response = ollama.generate(model='llama3', prompt=prompt)
print("Анализ Ламы:", response['response'])
