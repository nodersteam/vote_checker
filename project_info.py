import os
import json

def add_project_info():
    project_name = input("Введите название проекта: ")
    project_api = input("Введите API проекта: ")
    wallet_address = input("Введите адрес кошелька для этого проекта: ")
    network_type = input("Это mainnet или testnet? (mainnet/testnet): ")

    project_info = {
        'project_name': project_name,
        'project_api': project_api,
        'wallet_address': wallet_address,
        'network_type': network_type
    }

    projects = []
    if os.path.isfile('projectsinfo.txt'):
        with open('projectsinfo.txt', 'r') as file:
            projects = json.load(file)

    projects.append(project_info)

    with open('projectsinfo.txt', 'w') as file:
        json.dump(projects, file, ensure_ascii=False, indent=4)

    print("Информация о проекте успешно добавлена.")

def view_project_info():
    if not os.path.isfile('projectsinfo.txt'):
        print("Файл 'projectsinfo.txt' не существует.")
        return

    with open('projectsinfo.txt', 'r') as file:
        projects = json.load(file)

    if not projects:
        print("Информация о проектах отсутствует.")
        return

    print("Информация о проектах:\n")
    for idx, project_info in enumerate(projects, 1):
        print(f"{idx}.")
        print(f"Название проекта: {project_info['project_name']}")
        print(f"API проекта: {project_info['project_api']}")
        print(f"Адрес кошелька: {project_info['wallet_address']}\n")

def edit_project_info():
    if not os.path.isfile('projectsinfo.txt'):
        print("Файл 'projectsinfo.txt' не существует.")
        return

    with open('projectsinfo.txt', 'r') as file:
        projects = json.load(file)

    if not projects:
        print("Информация о проектах отсутствует.")
        return

    view_project_info()

    while True:
        project_idx = input("Введите номер проекта, который вы хотите редактировать: ")
        if not project_idx.isdigit() or int(project_idx) < 1 or int(project_idx) > len(projects):
            print("Введен недопустимый вариант. Пожалуйста, попробуйте еще раз.")
            continue

        project_idx = int(project_idx) - 1
        project_name = input(f"Введите новое название проекта (текущее: {projects[project_idx]['project_name']}): ")
        project_api = input(f"Введите новый API проекта (текущий: {projects[project_idx]['project_api']}): ")
        wallet_address = input(f"Введите новый адрес кошелька (текущий: {projects[project_idx]['wallet_address']}): ")

        projects[project_idx] = {
            'project_name': project_name,
            'project_api': project_api,
            'wallet_address': wallet_address,
        }

        with open('projectsinfo.txt', 'w') as file:
            json.dump(projects, file, ensure_ascii=False, indent=4)

        print("Информация о проекте успешно обновлена.")
        break

def delete_project_info():
    if not os.path.isfile('projectsinfo.txt'):
        print("Файл 'projectsinfo.txt' не существует.")
        return

    with open('projectsinfo.txt', 'r') as file:
        projects = json.load(file)

    if not projects:
        print("Информация о проектах отсутствует.")
        return

    view_project_info()

    while True:
        project_idx = input("Введите номер проекта, который вы хотите удалить: ")
        if not project_idx.isdigit() or int(project_idx) < 1 or int(project_idx) > len(projects):
            print("Введен недопустимый вариант. Пожалуйста, попробуйте еще раз.")
            continue

        project_idx = int(project_idx) - 1
        del projects[project_idx]

        with open('projectsinfo.txt', 'w') as file:
            json.dump(projects, file, ensure_ascii=False, indent=4)

        print("Информация о проекте успешно удалена.")
        break
