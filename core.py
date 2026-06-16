def analyze_and_decide(target, status):
    memory = load_beliefs()
    
    # Получаем правило, если статус есть, иначе возвращаем "неизвестный статус"
    rule = memory["rules"].get(str(status), "неизвестный статус")
    
    # Делаем подробный вывод
    conclusion = f"Статус {status} -> {rule}"
    
    # Добавляем запись в базу
    entry = {"target": target, "status": status, "conclusion": rule}
    memory["knowledge_base"].append(entry)
    
    save_beliefs(memory)
    return conclusion
def learn_new_rule(status, definition):
    """Агент учится новому правилу"""
    memory = load_beliefs()
    if status not in memory["rules"]:
        memory["rules"][str(status)] = definition
        save_beliefs(memory)
        print(f"[!] ИИ обучился: статус {status} теперь значит '{definition}'")
import json
import os

MEMORY_FILE = 'beliefs.json'

def load_beliefs():
    if not os.path.exists(MEMORY_FILE):
        return {"rules": {}, "knowledge_base": []}
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_beliefs(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def learn_new_rule(status, definition):
    memory = load_beliefs()
    memory["rules"][str(status)] = definition
    save_beliefs(memory)

def analyze_and_decide(target, status):
    memory = load_beliefs()
    rule = memory["rules"].get(str(status), "неизвестный статус")
    
    # Записываем в базу опыта
    entry = {"target": target, "status": status, "conclusion": rule}
    memory["knowledge_base"].append(entry)
    save_beliefs(memory)
    
    return f"Статус {status} -> {rule}"
