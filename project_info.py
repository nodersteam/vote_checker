import os
import json
from tabulate import tabulate


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

    headers = ["№", "Название проекта", "API", "Адрес кошелька", "Тип сети"]
    table = []

    for idx, project_info in enumerate(projects, 1):
        table.append([idx, project_info['project_name'], project_info['project_api'], project_info['wallet_address'],
                      project_info['network_type']])

    print(tabulate(table, headers, tablefmt="grid"))


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
        network_type = input(f"Введите тип сети (текущий: {projects[project_idx]['network_type']}): ")

        projects[project_idx] = {
            'project_name': project_name,
            'project_api': project_api,
            'wallet_address': wallet_address,
            'network_type': network_type
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
        project_idx = input("Введите номер проекта, который вы хотите удалить (или 'q' для выхода): ")

        if project_idx.lower() == 'q':
            break

        if not project_idx.isdigit() or int(project_idx) < 1 or int(project_idx) > len(projects):
            print("Введен недопустимый вариант. Пожалуйста, попробуйте еще раз.")
            continue

        project_idx = int(project_idx) - 1
        del_project = projects.pop(project_idx)

        with open('projectsinfo.txt', 'w') as file:
            json.dump(projects, file, ensure_ascii=False, indent=4)

        project_name = del_project.get('project_name', 'Неизвестное название')
        print(f"Проект '{project_name}' успешно удален.")
        break


# Пример использования функций
if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("1. Добавить информацию о проекте")
        print("2. Просмотреть информацию о проектах")
        print("3. Редактировать информацию о проекте")
        print("4. Удалить информацию о проекте")
        print("5. Выйти")

        choice = input("Выберите действие: ")

        if choice == '1':
            add_project_info()
        elif choice == '2':
            view_project_info()
        elif choice == '3':
            edit_project_info()
        elif choice == '4':
            delete_project_info()
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
