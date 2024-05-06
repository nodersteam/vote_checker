import json
import os

import requests


def test_api_connection():
    if not os.path.isfile('projectsinfo.txt'):
        print("Файл 'projectsinfo.txt' не существует.")
        return

    with open('projectsinfo.txt', 'r') as file:
        projects = json.load(file)

    broken_apis = []

    for project in projects:
        project_api = project['project_api']
        test_url = f'{project_api}/cosmos/auth/v1beta1/params'
        try:
            response = requests.get(test_url)
            if response.status_code == 200:
                params = response.json().get('params')
                if params and all(key in params for key in ["max_memo_characters", "tx_sig_limit", "tx_size_cost_per_byte", "sig_verify_cost_ed25519", "sig_verify_cost_secp256k1"]):
                    print(f"API {project_api} работает корректно.")
                else:
                    print(f"API {project_api} не работает как ожидается. Не найдены необходимые параметры.")
                    broken_apis.append(project)
            else:
                print(f"API {project_api} недоступен, статус код: {response.status_code}")
                broken_apis.append(project)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при подключении к API {project_api}: {str(e)}")
            broken_apis.append(project)

    if broken_apis:
        print("\nСледующие API не работают корректно:")
        for broken_api in broken_apis:
            print(f"Название проекта: {broken_api['project_name']}, API: {broken_api['project_api']}")
            new_api = input(f"Введите новый API для проекта {broken_api['project_name']} или оставьте пустым для пропуска: ")
            if new_api:
                broken_api['project_api'] = new_api

    # Обновление файла с информацией о проектах
    with open('projectsinfo.txt', 'w') as file:
        json.dump(projects, file, ensure_ascii=False, indent=4)

    print("Проверка API завершена.")
