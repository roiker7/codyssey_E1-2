import json
import os
from quiz import Quiz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(BASE_DIR, "state.json")

DEFAULT_QUIZZES = [
    {
        "question": "도커 이미지를 실제로 실행시켜서 살아있는 프로세스로 만드는 명령어는?",
        "choices": ["run", "stats", "images", "attach"],
        "answer": 1,
        "hint": "r로 시작하는 단어입니다."
    },
    {
        "question": "Dockerfile에서 FROM 명령어의 역할은?",
        "choices": ["파일을 복사한다", "프로그램을 실행한다", "베이스가 될 이미지를 지정한다", "라이브러리를 설치한다"],
        "answer": 3,
        "hint": "컨테이너의 가장 기초 뼈대를 가져오는 작업입니다."
    }
]

def load_data():
    #state.json 파일에서 데이터를 불러옵니다. 없거나 손상 시 기본값으로 복구
    if not os.path.exists(STATE_FILE):
        print("저장된 데이터 파일이 없어 기본 데이터로 초기화합니다.")
        return _reset_to_default()

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
        best_score = data.get("best_score", 0)
        history = data.get("history", []) # 히스토리 배열 로드

        if not quizzes:
            quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]

        return quizzes, best_score, history

    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"\n[알림] 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
        return _reset_to_default()

def save_data(quizzes, best_score, history):
    """퀴즈 목록, 최고 점수, 히스토리를 state.json에 UTF-8로 저장합니다."""
    data = {
        "best_score": best_score,
        "history": history,
        "quizzes": [q.to_dict() for q in quizzes]
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")
        return False

def _reset_to_default():
    quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
    best_score = 0
    history = []
    save_data(quizzes, best_score, history)
    return quizzes, best_score, history