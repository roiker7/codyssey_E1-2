from quiz import Quiz
from utils import get_int_input, get_str_input
from storage import load_data, save_data

class QuizGame:
    def __init__(self):
        self.quizzes, self.best_score = load_data()

    def save_state(self):
        save_data(self.quizzes, self.best_score)

    def play_quiz(self):
        """퀴즈 풀기 기능"""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다! 먼저 퀴즈를 추가해 주세요.")
            return

        print("\n========================================")
        print("           퀴즈 게임을 시작합니다!          ")
        print("========================================")

        score = 0
        for i, quiz in enumerate(self.quizzes, 1):
            quiz.display_quiz(i)
            user_ans = get_int_input("\n정답 번호를 입력하세요 (1-4): ", min_val=1, max_val=4)

            if user_ans is None:
                print("퀴즈 풀기가 중단되었습니다.")
                return

            if quiz.check_answer(user_ans):
                print("정답입니다!")
                score += 10
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print("\n========================================")
        print(f"게임 종료! 당신의 최종 점수: {score}점")
        print("========================================")

        if score > self.best_score:
            print(f"🎉 최고 점수를 경신했습니다! (기존: {self.best_score}점 ➔ 신규: {score}점)")
            self.best_score = score
            self.save_state()

    def add_quiz(self):
        """퀴즈 추가 기능"""
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

        answer = get_int_input("\n정답 번호를 입력하세요: ", min_val=1, max_val=4)
        if answer is None: return

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n성공적으로 새 퀴즈가 저장되었습니다!")

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

    def show_best_score(self):
        """최고 점수 확인 기능"""
        print("\n========================================")
        print("               최고 점수 확인            ")
        print("========================================")
        if self.best_score == 0:
            print("아직 게임을 진행하지 않았거나 최고 점수가 0점입니다.")
        else:
            print(f"🏆 현재 최고 점수: {self.best_score}점")