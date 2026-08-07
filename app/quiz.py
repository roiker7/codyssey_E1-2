class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices  # 보기 4개 리스트
        self.answer = answer    # 정답 번호 (1-4)

    def display_quiz(self, quiz_number):
        """퀴즈 문제와 보기를 출력합니다."""
        print(f"\n[문제 {quiz_number}] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_input):
        """사용자 입력을 정답과 비교합니다."""
        return user_input == self.answer

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 변환합니다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        """JSON 데이터(dict)로부터 Quiz 객체를 생성합니다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )