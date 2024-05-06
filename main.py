from project_info import add_project_info, view_project_info, edit_project_info, delete_project_info
from vote_checks import check_active_votes, schedule_checks, start_auto_check_votes
from api_test import test_api_connection  # Импортируем новую функцию

def menu():
    while True:
        print("""
Добро пожаловать в нашу систему!

---- Управление проектами ----
1. Добавить информацию о проекте для проверки активных голосований
2. Посмотреть информацию о проекте
3. Изменить информацию о проекте
4. Удалить информацию о проекте

---- Проверка голосования ----
5. Проверить активные голоса
6. Настроить автоматическую проверку голосов
7. Начать автоматическую проверку голосов

---- Тестирование ----
8. Проверка работоспособности API

10. Выход
        """)

        option = input("Введите номер выбранного вами варианта: ")

        if option == '1':
            add_project_info()
        elif option == '2':
            view_project_info()
        elif option == '3':
            edit_project_info()
        elif option == '4':
            delete_project_info()
        elif option == '5':
            check_active_votes()
        elif option == '6':
            schedule_checks()
        elif option == '7':
            start_auto_check_votes()
        elif option == '8':
            test_api_connection()
        elif option == '10':
            print("Выход из программы...")
            break
        else:
            print("Введен неверный вариант. Пожалуйста, попробуйте еще раз.")

if __name__ == "__main__":
    menu()
