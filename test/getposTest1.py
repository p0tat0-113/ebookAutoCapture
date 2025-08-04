import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()
        print(f"마우스 포인터의 위치: ({x}, {y})")
        time.sleep(0.1)  # 0.1초마다 위치를 업데이트
except KeyboardInterrupt:
    print("프로그램이 종료되었습니다.")
