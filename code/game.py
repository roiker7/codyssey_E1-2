import random
from datetime import datetime
from quiz import Quiz
from utils import get_int_input, get_str_input
from storage import load_data, save_data

class QuizGame:
    def __init__(self):
        self.quizzes, self.best_score, self.history = load_data()

    def save_state(self):
        save_data(self.quizzes, self.best_score, self.history)

    def play_quiz(self):
        #퀴즈 풀기 기능 (랜덤 출제, 문항 수 선택, 힌트)
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다! 먼저 퀴즈를 추가해 주세요.")
            return

        print("\n========================================")
        print("           퀴즈 게임을 시작합니다!          ")
        print("========================================")

        # 1. 문제 수 선택
        max_q = len(self.quizzes)
        num_q = get_int_input(f"몇 문제를 푸시겠습니까? (1-{max_q}): ", min_val=1, max_val=max_q)
        if num_q is None: return

        # 2. 랜덤 출제 설정 (random 모듈 활용)
        selected_quizzes = random.sample(self.quizzes, num_q)
        score = 0

        for i, quiz in enumerate(selected_quizzes, 1):
            hint_used = False
            while True:
                quiz.display_quiz(i)
                if hint_used:
                    print(f"\n💡 현재 힌트: {quiz.hint}")

                user_ans = get_int_input("\n정답 번호를 입력하세요 (0: 힌트, 1-4): ", min_val=0, max_val=4)
                if user_ans is None:
                    print("퀴즈 풀기가 중단되었습니다.")
                    return

                # 힌트 사용 처리
                if user_ans == 0:
                    if not hint_used:
                        hint_used = True
                        print("\n[!] 힌트를 확인했습니다. 맞추더라도 점수가 일부 차감(10점 -> 7점)됩니다.")
                    else:
                        print("\n[!] 이미 힌트를 사용하셨습니다.")
                    continue  # 다시 문제 출력 및 입력 대기로 돌아감

                # 정답 검증
                if quiz.check_answer(user_ans):
                    print("⭕ 정답입니다!")
                    score += 7 if hint_used else 10
                else:
                    print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
                break  # 해당 문제 종료, 다음 문제로 이동

        # 게임 결과 출력 및 히스토리 저장
        print("\n========================================")
        print(f"게임 종료! 당신의 최종 점수: {score}점")
        print("========================================")

        if score > self.best_score:
            print(f"🎉 최고 점수를 경신했습니다! (기존: {self.best_score}점 ➔ 신규: {score}점)")
            self.best_score = score
        
        # 게임 기록 히스토리 추가
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "date": now,
            "questions_played": num_q,
            "score": score
        })
        self.save_state()

    def add_quiz(self):
        """퀴즈 추가 기능 (힌트 포함)"""
        print("\n========================================")
        print("           새로운 퀴즈 추가하기           ")
        print("========================================")

        question = get_str_input("등록할 문제를 입력하세요: ")
        if question is None: return

        choices = []
        print("\n보기를 4개 입력해 주세요.")
        for i in range(1, 5):
            choice_text = get_str_input(f"보기 {i}: ")
            if choice_text is None: return
            choices.append(choice_text)

        answer = get_int_input("\n정답 번호를 입력하세요 (1-4): ", min_val=1, max_val=4)
        if answer is None: return

        hint = get_str_input("\n문제의 힌트를 입력하세요: ")
        if hint is None: return

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n성공적으로 새 퀴즈가 저장되었습니다!")

    def delete_quiz(self):
        """퀴즈 삭제 기능"""
        print("\n========================================")
        print("              퀴즈 삭제하기             ")
        print("========================================")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        # 퀴즈 목록 출력
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")

        delete_idx = get_int_input(f"\n삭제할 퀴즈 번호를 입력하세요 (1-{len(self.quizzes)}, 0: 뒤로가기): ", min_val=0, max_val=len(self.quizzes))
        
        if delete_idx is None or delete_idx == 0:
            print("삭제를 취소하고 이전 메뉴로 돌아갑니다.")
            return
        
        # 선택한 퀴즈 삭제 (인덱스는 0부터 시작하므로 -1)
        deleted_quiz = self.quizzes.pop(delete_idx - 1)
        self.save_state()
        print(f"\n'{deleted_quiz.question}' 문제가 완전히 삭제되었습니다.")

    def show_quizzes(self):
        """퀴즈 목록 확인 기능"""
        print("\n========================================")
        print("              퀴즈 목록 보기             ")
        print("========================================")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes, 1):
            quiz.display_quiz(i)
            print(f"   [정답: {quiz.answer}번]")
            print("-" * 40)

    def show_records(self):
        """점수 및 게임 기록 히스토리 확인 기능"""
        print("\n========================================")
        print("             점수 및 게임 기록           ")
        print("========================================")
        print(f"🏆 현재 최고 점수: {self.best_score}점\n")
        
        print("[최근 게임 기록 (최대 10개)]")
        if not self.history:
            print("아직 게임 기록이 없습니다.")
        else:
            # 최근 기록 10개만 리스트의 끝에서부터 가져와서 출력
            for i, record in enumerate(self.history[-10:], 1):
                print(f" {i}. {record['date']} | 푼 문제 수: {record['questions_played']}개 | 획득 점수: {record['score']}점")