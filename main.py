"""Сильвия — простой автономный агент для облачного запуска.

Этот файл сделан неблокирующим и не требует интерактивного ввода,
чтобы его можно было запускать в GitHub Actions или других CI.
"""
import re
import os
import requests
from core import analyze_and_decide, load_beliefs

# Конфигурация
TARGETS = [
    "http://example.com/admin",
    "http://example.com/config",
    "http://example.com/login",
]
MAX_PAGES = int(os.environ.get("SYLVIA_MAX_PAGES", "20"))
TIMEOUT = 5


def extract_links(html, base_url):
    # Простейшее извлечение абсолютных ссылок
    return re.findall(r'href=["\'](https?://[^"\']+)["\']', html)


def run_ai_agent(targets=None):
    if targets is None:
        targets = list(TARGETS)
    visited = set()
    pages_visited = 0

    print(f"[*] Сильвия стартует. Лимит страниц: {MAX_PAGES}")

    while targets and pages_visited < MAX_PAGES:
        target = targets.pop(0)
        if target in visited:
            continue

        try:
            print(f"\n[{pages_visited+1}/{MAX_PAGES}] Обработка: {target}")
            resp = requests.get(target, timeout=TIMEOUT)
            status = str(resp.status_code)

            decision = analyze_and_decide(target, status)
            print(f"[+] Решение ядра: {decision}")

            if status == "200":
                links = extract_links(resp.text, target)
                for link in links:
                    if link not in visited and len(targets) < MAX_PAGES:
                        targets.append(link)
                print(f"[+] Найдено {len(links)} ссылок на странице.")

            visited.add(target)
            pages_visited += 1

        except Exception as e:
            print(f"[!] Ошибка доступа к {target}: {e}")

    print("\n[!] Работа завершена. Обновления сохранены в beliefs.json (если были)")


if __name__ == "__main__":
    run_ai_agent()
    