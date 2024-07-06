import datetime
import json
import os
from dateutil.parser import isoparse
import requests
import time
from config import CHAT_ID_MAINNET, CHAT_ID_TESTNET
from telegram_utils import send_telegram_message

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

    mainnet_messages = []
    testnet_messages = []
    seen_proposals = set()

    for project_info in projects:
        project_api = project_info.get('project_api')
        project_wallet = project_info.get('wallet_address')
        network_type = project_info.get('network_type')

        for api_version in ['v1beta1', 'v1']:
            url = f'{project_api}/cosmos/gov/{api_version}/proposals?pagination.limit=600'
            try:
                response = requests.get(url, timeout=3)
                response.raise_for_status()

                print(f"Status Code: {response.status_code}")
                print(f"Response Text: {response.text[:1000]}")  # Печатает первые 1000 символов ответа

                if response.status_code == 200:
                    try:
                        data = response.json()
                        proposals = data.get('proposals', [])
                    except requests.exceptions.JSONDecodeError:
                        print(f"Failed to decode JSON for {project_info['project_name']}. Response text: {response.text[:1000]}")
                        continue

                    if proposals:
                        active_proposals = [p for p in proposals if p.get('status') == "PROPOSAL_STATUS_VOTING_PERIOD"]
                        if active_proposals:
                            print(f"\nАктивные голоса для {project_info['project_name']}:\n")
                            for proposal in active_proposals:
                                proposal_id = proposal.get('id', proposal.get('proposal_id', 'No ID available'))

                                if proposal_id in seen_proposals:
                                    continue
                                seen_proposals.add(proposal_id)

                                title = proposal['content'].get('title', '') if api_version == 'v1beta1' else proposal.get('title', '')

                                # Проверка наличия заголовка
                                if not title:
                                    print(f"Предложение {proposal_id} не содержит заголовка. Пропуск.")
                                    continue

                                try:
                                    start_time = isoparse(proposal.get('voting_start_time')).strftime('%d %B %Y, %H:%M') if proposal.get('voting_start_time') else 'No start time'
                                    end_time = isoparse(proposal.get('voting_end_time')).strftime('%d %B %Y, %H:%M') if proposal.get('voting_end_time') else 'No end time'
                                except Exception as e:
                                    print(f"Ошибка при парсинге дат: {e}")
                                    start_time = 'Ошибка даты'
                                    end_time = 'Ошибка даты'

                                vote_url = f'{project_api}/cosmos/gov/{api_version}/proposals/{proposal_id}/votes/{project_wallet}'
                                vote_response = requests.get(vote_url)
                                if vote_response.status_code == 200:
                                    vote_data = vote_response.json()
                                    option = vote_data['vote']['options'][0]['option']
                                    voted = {
                                        "VOTE_OPTION_YES": "Yes",
                                        "VOTE_OPTION_ABSTAIN": "Abstain",
                                        "VOTE_OPTION_NO": "No",
                                        "VOTE_OPTION_NO_WITH_VETO": "No with veto"
                                    }.get(option, "Not yet")
                                else:
                                    voted = "Not yet"

                                # Логика изменения цвета кружка
                                vote_emoji = "🟢" if voted != "Not yet" else "🔴"

                                message = (
                                    f"{vote_emoji} 🌐 {project_info['project_name']}\n"
                                    f"⚖️ Network: {network_type}\n"
                                    f"📜 Proposal ID: {proposal_id}\n"
                                    f"📃 Title: {title}\n"
                                    f"⏰ Voting Start: {start_time}\n"
                                    f"⏳ Voting End: {end_time}\n"
                                    f"🗳️ Voted option: {voted}"
                                )

                                if network_type == 'mainnet':
                                    mainnet_messages.append(message)
                                elif network_type == 'testnet':
                                    testnet_messages.append(message)

                        else:
                            print(f"{project_info['project_name']}: Нет активных голосов.")
                    else:
                        print(f"{project_info['project_name']}: Нет предложений.")
            except requests.exceptions.Timeout:
                print(f"Превышено время ожидания для {project_info['project_name']}. Переход к следующему проекту.")
                break
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса API для {project_info['project_name']}: {str(e)}")
                continue

    if mainnet_messages:
        combined_mainnet_message = "\n\n".join(mainnet_messages)
        send_telegram_message(combined_mainnet_message, 'mainnet')

    if testnet_messages:
        combined_testnet_message = "\n\n".join(testnet_messages)
        send_telegram_message(combined_testnet_message, 'testnet')


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

    next_check_time = datetime.datetime.now() + interval

    while True:
        current_time = datetime.datetime.now()
        if current_time >= next_check_time:
            print(f"\nНачало проверки голосов... Следующая проверка через: {interval}")
            check_active_votes()
            next_check_time = current_time + interval
        time.sleep(120)  # Сон на 120 секунд для снижения нагрузки
