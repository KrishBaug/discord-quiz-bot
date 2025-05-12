import json 
import os
from datetime import datetime


def load_data() -> dict:
    with open('questions.json', 'r') as f:
        data = json.load(f)
        return data


def return_no_of_questions() -> int:
    data = load_data()
    return len(data)


def required_set_of_questions(question_index: list) -> dict:
    question_set = {"quiz_questions": []}
    data = load_data()
    for question_no in question_index:
        question_set['quiz_questions'].append(data[question_no])
    return question_set


def update_or_create_json_file(questions: dict, unique_key: str) -> None:
    with open(f'DATA_FILES/quiz{unique_key}.json', 'w') as f:
        json.dump(questions, f, indent=2)


def remove_file(unique_code: str) -> None:
    try:
        os.remove(f'DATA_FILES/quiz{unique_code}.json')
    except FileNotFoundError:
        print(f'File quiz{unique_code}.json not found')


def creat_tracking_file(author_id: int, author_name: str,
                        author_guild: int, unique_code: str, all_questions: list) -> None:
    track_file = {
        "quiz_data": {
            "user_name": author_name,
            "user_id": author_id,
            "user_guild": author_guild,
            "cmd_channel": unique_code,
            "question_list": all_questions,
            "Total_questions": len(all_questions),
            "time": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "running_status": True,
            "current_question_no": 0,
            "score_of_players": []
        }
    }
    with open(f'TRACKING_FILES/quiz_track{unique_code}.json', 'w') as f:
        json.dump(track_file, f, indent=2)


def get_options(unique_code: str) -> list:
    with open(f'TRACKING_FILES/quiz_track{unique_code}.json') as f:
        w = json.load(f)


    current_question_no = w['quiz_data']['current_question_no']
    with open(f'DATA_FILES/quiz{unique_code}.json') as f:
        w = json.load(f)
        opt_a = w["quiz_questions"][current_question_no]["A"]
        opt_b = w["quiz_questions"][current_question_no]["B"]
        opt_c = w["quiz_questions"][current_question_no]["C"]
        opt_d = w["quiz_questions"][current_question_no]["D"]
        ans_key = w["quiz_questions"][current_question_no]["answer"]
        ans = w["quiz_questions"][current_question_no][ans_key]
        return [opt_a, opt_b, opt_c, opt_d, ans]


def get_question(unique_code: str) -> tuple:
    with open(f'TRACKING_FILES/quiz_track{unique_code}.json') as f:
        w = json.load(f)
        current_question_no = w['quiz_data']['current_question_no']
        total_question = w['quiz_data']['Total_questions']

    with open(f'DATA_FILES/quiz{unique_code}.json') as f:
        w = json.load(f)
        question = w["quiz_questions"][current_question_no]['question']

    return question, current_question_no + 1, total_question




def update_question_no(unique_code: str) -> None:
    with open(f'TRACKING_FILES/quiz_track{unique_code}.json', 'r+') as f:
        w = json.load(f)
        w['quiz_data']['current_question_no'] += 1
        f.seek(0)
        json.dump(w, f, indent=2)
        f.truncate()



def check_if_user_there(unique_code: str, user_id: str) -> bool:
    with open(f'TRACKING_FILES/quiz_track{unique_code}.json', "r") as f:
        data = json.load(f)

    user_data = data['quiz_data']['score_of_players']
    for player in user_data:
        if str(player["user_id"]) == user_id:
            return True

    return False



def add_user_score(unique_code: str, user_id: str, user_name: str):
    player_info = {
        "user_name": user_name,
        "user_id": user_id,
        "score": 0,
        "answered_question": False
    }
    with open(f'TRACKING_FILES/quiz_track{unique_code}.json', "r+") as f:
        data = json.load(f)
        data['quiz_data']['score_of_players'].append(player_info)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()




def if_question_answered(user_id: str, unique_code: str) -> bool:
    with open(f'TRACKING_FILES/quiz_track{unique_code}.json', "r") as f:
        data = json.load(f)
        user_data = data['quiz_data']['score_of_players']

    for player in user_data:
        if player['user_id'] == user_id:
            return player['answered_question']

    return False


def update_score(unique_code: str, user_id: str, answer_state: bool):
    with open(f'TRACKING_FILES/quiz_track{unique_code}.json', "r+") as f:
        data = json.load(f)
        user_data = data['quiz_data']['score_of_players']
        
        score = 10 if answer_state else 0

        for player in user_data:
            if str(player["user_id"]) == user_id:
                player["score"] += score
                player['answered_question'] = True

        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()



def handle_button_click(unique_code: str, user_id: str, user_name: str, answer_state: bool):
    if not check_if_user_there(unique_code, user_id):
        add_user_score(unique_code, user_id, user_name)

    if if_question_answered(user_id=user_id, unique_code=unique_code):
        return True
    else:
        update_score(unique_code=unique_code, user_id=user_id, answer_state=answer_state)
        return False

#start from here

def reset_ans_state(unique_code: str):
     with open(f'TRACKING_FILES/quiz_track{unique_code}.json', "r+") as f:
        data = json.load(f)
        user_data = data['quiz_data']['score_of_players']

        for player in user_data:
            player['answered_question']=False

        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

def get_all_data(unique_code: str):
    with open(f'DATA_FILES/quiz{unique_code}.json', 'r') as f:
        data = json.load(f)

    return data


def create_gpt_convo(convo, unique_code, id, user_name):
    conversation_format = {
            f"{user_name}": convo,
            "You (doubt solving ai)": ""
            }
    conversation ={
            "convo" : {}
            }
    with open(f'AI_CONVERSATIONS/{unique_code}', 'r+') as f:
        data.dump
        
