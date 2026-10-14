from datetime import datetime, timezone, timedelta
import csv
import os

def get_current_local_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

def get_thread_id():
    print('step1')
    return get_current_local_datetime().replace("-", "_").replace(":", "")

def save_chat_history(app, config):
    messages = app.get_state(config).values['chat_history']
    thread_id = config['configurable']['thread_id']
    folder_path = os.path.join(os.getcwd(), 'history')
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f'{thread_id}.csv')

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(messages)

    return file_path


"""
机器学习 ｜ 深度学习
翻译系统、专家系统、情感分析、图像识别、自然语言生成 ...............
架构不同 cnn rnn bret ....

LLM
架构: Transformer

大模型应用开发 需要深入的了解机器学习和深度学习嘛？
L4阶段  了解机器学习和深度学习


y = kx + b










"""








