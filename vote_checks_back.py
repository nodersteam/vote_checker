import datetime
import json
import os
from dateutil.parser import isoparse
import requests
import schedule
import time
from config import CHAT_ID_MAINNET, CHAT_ID_TESTNET
from telegram_utils import send_telegram_message
from api_test import test_api_connection

next_check_time = None
interval = None

def check_active_votes():
    global next_check_time, interval
    if interval:
        next_check_time = datetime.datetime.now() + interval

    if not os.path.isfile('projectsinfo.txt'):
        print("Файл 'projectsinfo.txt' не существует.")
        return

    with open('projectsinfo.txt', 'r') as file:
        projects = json.load(file)

    for project_info in projects:
        project_api = project_info['project_api']
        project_wallet = project_info['wallet_address']
        network_type = project_info['network_type']

        project_votes_found = False
        for api_version in ['v1beta1', 'v1']:
            url = f'{project_api}/cosmos/gov/{api_version}/proposals?pagination.limit=600'
            response = requests.get(url)
            if response.status_code == 200:
                proposals = response.json().get('proposals', [])
                if proposals:
                    active_proposals = [p for p in proposals if p.get('status') == "PROPOSAL_STATUS_VOTING_PERIOD"]
                    if not active_proposals:
                        continue
                    print(f"\nАктивные голоса для {project_info['project_name']}:\n")
                    project_votes_found = True
                    for proposal in active_proposals:
                        proposal_id = proposal.get('id', proposal.get('proposal_id', 'No ID available'))
                        title = proposal.get('title', 'No title available') if api_version == 'v1' else proposal['content'].get('title', 'No title available')

                        vote_url = f'{project_api}/cosmos/gov/{api_version}/proposals/{proposal_id}/votes/{project_wallet}'
                        vote_response = requests.get(vote_url)
                        voted = "Yes" if vote_response.status_code == 200 else "No"

                        start_time = isoparse(proposal.get('voting_start_time')).strftime('%d %B %Y, %H:%M') if proposal.get('voting_start_time') else 'No start time'
                        end_time = isoparse(proposal.get('voting_end_time')).strftime('%d %B %Y, %H:%M') if proposal.get('voting_end_time') else 'No end time'
                        message = (
                            f"\nПроект: {project_info['project_name']}\n"
                            f"Network Type: {network_type}\n"
                            f"Proposal ID: {proposal_id}\n"
                            f"Title: {title}\n"
                            f"Voting Start Time: {start_time}\n"
                            f"Voting End Time: {end_time}\n"
                            f"Voted: {voted}\n"
                        )
                        send_telegram_message(message, voted, network_type)
                if not project_votes_found:
                    print(f"{project_info['project_name']}: Новые голоса не найдены.")


def schedule_checks():
    global interval
    while True:
        print("""
Пожалуйста, выберите один из следующих вариантов для расписания:
1. Каждый час
2. Каждый день
3. Каждую неделю
        """)

        option = input("Введите номер выбранного вами варианта: ")

        if option == '1':
            interval = datetime.timedelta(hours=1)
            print("Расписание установлено на проверку каждый час.")
            break
        elif option == '2':
            interval = datetime.timedelta(days=1)
            print("Расписание установлено на проверку каждый день.")
            break
        elif option == '3':
            interval = datetime.timedelta(weeks=1)
            print("Расписание установлено на проверку каждую неделю.")
            break
        else:
            print("Введен неверный вариант. Пожалуйста, попробуйте еще раз.")


def start_auto_check_votes():
    global next_check_time
    if not interval:
        print("Расписание не установлено. Пожалуйста, установите расписание.")
        return

    print("Начало автоматической проверки голосов...")
    print("Теперь вы можете безопасно закрыть вашу сессию экрана.")
    print("Чтобы отсоединиться от сессии экрана, нажмите Ctrl + A, затем D.")
    print("Чтобы повторно подключиться к сессии экрана, введите 'screen -r' в терминале.")
    
    # Инициализация первого времени проверки
    next_check_time = datetime.datetime.now() + interval

    while True:
        current_time = datetime.datetime.now()
        if current_time >= next_check_time:
            print(f"\nНачало проверки голосов... Следующая проверка через: {interval}")
            check_active_votes()
            next_check_time = current_time + interval
        time.sleep(120)  # Сон на 120 секунд для снижения нагрузки
