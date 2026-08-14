import sys

def handle_exit():
    """Ctrl+C / Ctrl+D 입력 시 비정상 종료를 방지하고 안전하게 확인합니다."""
    try:
        check = input("\n\n작업을 중단하고 이전 메뉴로 돌아가시겠습니까? (y/n): ").strip().lower()
        if check in ['y', 'yes', 'ㅛ']:
            return True
        else:
            print("이전 작업으로 돌아갑니다.\n")
            return False
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
        sys.exit(0)

def get_int_input(prompt, min_val=None, max_val=None):
    """숫자 입력을 검증합니다. (공백, 범위, 문자 예외 처리)"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("아무것도 입력되지 않았습니다. 숫자를 입력해 주세요.\n")
                continue

            val = int(user_input)
            if min_val is not None and val < min_val:
                print(f"{min_val} 이상의 숫자를 입력해 주세요.\n")
                continue
            if max_val is not None and val > max_val:
                print(f"{max_val} 이하의 숫자를 입력해 주세요.\n")
                continue

            return val
        except ValueError:
            print("숫자만 입력해 주세요. (예: 1, 2, 3...)\n")
        except (KeyboardInterrupt, EOFError):
            if handle_exit():
                return None

def get_str_input(prompt):
    """문자열 입력을 검증합니다. (공백 처리)"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("내용이 비어 있습니다. 올바른 텍스트를 입력해 주세요.\n")
                continue
            return user_input
        except (KeyboardInterrupt, EOFError):
            if handle_exit():
                return None