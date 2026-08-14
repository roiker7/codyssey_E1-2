from game import QuizGame
from utils import get_int_input

def main():
    game = QuizGame()

    while True:
        print('''
    ========================================
                    도전 골든벨! 
    ========================================
    1. 퀴즈 풀기 (게임 시작)
    2. 퀴즈 추가 
    3. 퀴즈 목록
    4. 점수 확인
    5. 종료
    ========================================''')

        choice = get_int_input("원하는 메뉴를 선택해 주세요 (1-5): ", min_val=1, max_val=5)

        if choice is None:
            break

        if choice == 1:
            game.play_quiz()
        elif choice == 2:
            game.add_quiz()
        elif choice == 3:
            game.show_quizzes()
        elif choice == 4:
            game.show_best_score()
        elif choice == 5:
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break

if __name__ == "__main__":
    main()