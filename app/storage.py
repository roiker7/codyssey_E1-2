import json
import os
from quiz import Quiz

STATE_FILE = "state.json"

# 파일이 없거나 손상되었을 때 기본으로 탑재되는 퀴즈 데이터 (5개 이상)
DEFAULT_QUIZZES = [
    {
        "question": "도커 이미지를 실제로 실행시켜서 살아있는 프로세스로 만드는 명령어는?",
        "choices": ["run", "stats", "images", "attach"],
        "answer": 1
    },
    {
        "question": "Dockerfile에서 FROM 명령어의 역할은?",
        "choices": ["파일을 복사한다", "프로그램을 실행한다", "베이스가 될 이미지를 지정한다", "라이브러리를 설치한다"],
        "answer": 3
    },
    {
        "question": "Dockerfile에서 컨테이너가 시작될 때 실행할 마지막 명령어를 지정하는 키워드는?",
        "choices": ["START", "RUN", "COPY", "CMD"],
        "answer": 4
    },
    {
        "question": "운영체제 정보를 확인하는 명령어는?",
        "choices": ["uname", "echo", "pwd", "version"],
        "answer": 1
    },
    {
        "question": "호스트의 80번 포트를 컨테이너의 8080번 포트로 연결하기 위한 옵션은?",
        "choices": ["-p 8080:80", "-p 80:8080", "-v 80:8080", "-net 80:8080"],
        "answer": 2
    }
]

def load_data():
    """state.json 파일에서 데이터를 불러옵니다. 없거나 손상 시 기본값으로 복구합니다."""
    if not os.path.exists(STATE_FILE):
        print("저장된 데이터 파일이 없어 기본 데이터로 초기화합니다.")
        return _reset_to_default()

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
        best_score = data.get("best_score", 0)

        if not quizzes:
            quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]

        return quizzes, best_score

    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"\n[알림] 데이터 파일(state.json)이 손상되었습니다. 기본 데이터로 복구합니다.")
        return _reset_to_default()

def save_data(quizzes, best_score):
    """퀴즈 목록과 최고 점수를 state.json 파일에 UTF-8 인코딩으로 저장합니다."""
    data = {
        "best_score": best_score,
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
    save_data(quizzes, best_score)
    return quizzes, best_score