from pywinauto.keyboard import send_keys
import time

# 잠시 대기하여 사용자가 수동으로 창을 포커스할 시간을 줍니다
print("창을 포커스한 후 5초 내에 입력이 시작됩니다...")
time.sleep(5)  # 5초 대기

# 방향키 입력을 시작합니다
send_keys('{UP}')    # 위쪽 방향키
time.sleep(0.1)      # 잠시 대기
send_keys('{DOWN}')  # 아래쪽 방향키
time.sleep(0.1)
send_keys('{LEFT}')  # 왼쪽 방향키
time.sleep(0.1)
send_keys('{RIGHT}') # 오른쪽 방향키
