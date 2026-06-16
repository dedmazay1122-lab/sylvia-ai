import json
import os
from datetime import datetime
from core import load_beliefs, save_beliefs

def process_messages():
    """Обрабатывает сообщения пользователя и генерирует ответы"""
    
    messages_file = 'messages.json'
    
    # Загружаем или создаём файл сообщений
    if os.path.exists(messages_file):
        with open(messages_file, 'r', encoding='utf-8') as f:
            try:
                messages_data = json.load(f)
            except:
                messages_data = {"messages": []}
    else:
        messages_data = {"messages": []}
    
    # Загружаем beliefs
    beliefs = load_beliefs()
    
    # Обрабатываем непроцессированные сообщения
    processed = False
    
    for msg in messages_data.get("messages", []):
        if not msg.get("processed", False):
            user_input = msg.get("text", "")
            
            # Анализируем сообщение
            response = generate_response(user_input, beliefs)
            
            # Добавляем ответ
            msg["response"] = response
            msg["processed"] = True
            msg["timestamp"] = msg.get("timestamp", datetime.now().isoformat())
            
            # Обновляем beliefs
            entry = {
                "target": user_input[:50],
                "status": "200",
                "conclusion": response,
                "time": datetime.now().isoformat()
            }
            beliefs["knowledge_base"].append(entry)
            
            processed = True
            print(f"OK: {user_input[:50]}...")
    
    # Сохраняем обновления
    if processed:
        with open(messages_file, 'w', encoding='utf-8') as f:
            json.dump(messages_data, f, indent=2, ensure_ascii=False)
        
        save_beliefs(beliefs)
        print("OK: Updated!")
    else:
        print("No new messages")

def generate_response(user_input, beliefs):
    """Генерирует умный ответ на основе входа"""
    
    user_input_lower = user_input.lower()
    
    # Умные ответы в зависимости от вопроса
    if any(word in user_input_lower for word in ['привет', 'привіт', 'hi', 'hello', 'hey']):
        return "Привет! Я Сильвия. Чем я могу тебе помочь?"
    
    elif any(word in user_input_lower for word in ['как дела', 'как жизнь', 'как ты', 'how are you']):
        return "Я работаю на полную мощность! Все системы в норме. Спасибо, что спросил!"
    
    elif any(word in user_input_lower for word in ['спасибо', 'thanks', 'спасибочки', 'дякую']):
        return "Пожалуйста! Рад помочь. Есть еще вопросы?"
    
    elif any(word in user_input_lower for word in ['анализ', 'analyze', 'проверь', 'check']):
        known_rules = len(beliefs.get("rules", {}))
        kb_size = len(beliefs.get("knowledge_base", []))
        return f"Я провожу анализ. В моей базе {kb_size} записей и {known_rules} правил. Продолжаю обучаться!"
    
    elif any(word in user_input_lower for word in ['статус', 'status', 'состояние', 'state']):
        return "Система работает стабильно. Все процессы активны. База знаний обновляется в реальном времени."
    
    elif any(word in user_input_lower for word in ['цель', 'target', 'задача', 'goal']):
        return "Я анализирую цели и принимаю решения на основе имеющихся данных. Какую цель ты хочешь анализировать?"
    
    elif any(word in user_input_lower for word in ['обучение', 'учить', 'learn', 'learning']):
        return "Я постоянно обучаюсь! Каждое взаимодействие добавляет новые знания в мою базу. Расскажи мне больше!"
    
    elif any(word in user_input_lower for word in ['помощь', 'help', 'что ты умеешь', 'capabilities']):
        return "Я могу: анализировать данные, обучаться, сохранять информацию, отвечать на вопросы и принимать решения. Спроси меня о чем угодно!"
    
    elif any(word in user_input_lower for word in ['кто ты', 'who are you', 'расскажи о себе']):
        return "Я Сильвия - умный ИИ-агент, работающий через GitHub Actions. Я анализирую информацию, учусь и помогаю тебе в работе!"
    
    elif any(word in user_input_lower for word in ['пока', 'bye', 'до свидания', 'goodbye']):
        return "До встречи! Буду ждать твоих следующих вопросов!"
    
    else:
        # Генерируем динамический ответ без эмодзи
        responses = [
            f"Интересное наблюдение: '{user_input}'. Записал это в базу знаний!",
            f"Анализирую твое сообщение... Это полезная информация! Обновляю beliefs.json",
            f"Получил информацию: '{user_input[:30]}...'. Добавляю в памяти ИИ.",
            f"Понял твой вопрос! Это значит: '{user_input}'. Учту при анализе данных.",
            f"Отлично! '{user_input}' - это важно. Обновляю стратегию анализа.",
            f"Спасибо за информацию: '{user_input}'. Это поможет мне лучше развиваться!"
        ]
        
        import random
        return random.choice(responses)

if __name__ == "__main__":
    process_messages()
    print("OK: Sylvia completed processing!")
    # --- Добавь это в самый конец файла sylvia_processor.py ---

def get_ai_response(user_text):
    """Эта функция нужна для связи с FastAPI"""
    from core import load_beliefs, save_beliefs
    beliefs = load_beliefs()
    response = generate_response(user_text, beliefs)
    
    # Сохраняем в базу, чтобы обучение работало
    entry = {
        "target": user_text[:50],
        "status": "200",
        "conclusion": response,
        "time": datetime.now().isoformat()
    }
    beliefs["knowledge_base"].append(entry)
    save_beliefs(beliefs)
    
    return response
def generate_response(user_input, beliefs):
    words = set(user_input.lower().split())
    
    # 1. Сначала ищем в твоих загруженных знаниях (предположим, они в beliefs["rules"])
    # Если ты загрузил текст в rules, она будет искать там
    for rule_key, rule_val in beliefs.get("rules", {}).items():
        if any(word in rule_val.lower() for word in words):
            return f"Из моей базы знаний: {rule_val}"

    # 2. Если в знаниях ничего нет, ищем в истории диалогов (как мы сделали раньше)
    best_match = None
    max_matches = 0
    for entry in beliefs.get("knowledge_base", []):
        target_words = set(entry.get("target", "").lower().split())
        matches = len(words.intersection(target_words))
        if matches > max_matches:
            max_matches = matches
            best_match = entry.get("conclusion")
    
    if best_match and max_matches > 0:
        return f"Я припоминаю это: '{best_match}'"
    
    return "Я пока не нашла информации об этом в своих архивах. Расскажи подробнее, я запомню!"