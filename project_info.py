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

    max_idx_length = len(str(len(projects)))
    header_format = "{:<{width}} {:<20} {:<30} {:<15}"
    row_format = "{:<{width}} {:<20} {:<30} {:<15}"

    print("Список проектов:")
    print(header_format.format("№", "Название проекта", "API", "Адрес кошелька", width=max_idx_length))
    print("-" * (max_idx_length + 70))  # Линия для разделения заголовка и данных

    for idx, project in enumerate(projects, start=1):
        project_name = project.get('project_name', 'Неизвестное название')
        project_api = project.get('project_api', 'Нет данных')
        wallet_address = project.get('wallet_address', 'Нет данных')

        # Выводим каждый проект с заданными ширинами для каждого столбца
        print(row_format.format(idx, project_name, project_api, wallet_address, width=max_idx_length))

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