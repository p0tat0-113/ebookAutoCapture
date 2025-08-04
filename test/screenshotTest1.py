import mss
import mss.tools
import datetime
import os

num = 0

def capture_screen(region=None, save_path=None):
    if save_path is None:
        raise ValueError("You must provide a save_path for the screenshot.")
    
    global num
    save_path = save_path + str(num) +".png"
    num = num+1

    # 디렉토리가 존재하지 않으면 생성
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        raise Exception("해당 경로가 발견되지 않음.")
    
    with mss.mss() as sct:
        if region:
            # 특정 영역 캡처
            monitor = {"top": region[1], "left": region[0], "width": region[2], "height": region[3]}
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)

        # else:
        #     # 모니터 전체 캡처
        #     screenshot = sct.shot(output=save_path)
        
        print(f'Screenshot saved as {save_path}')

if __name__ == "__main__":
    # # 저장할 절대 경로 설정
    # absolute_path = "C:\\Users\\barrett11357\\Downloads\\screenshotTest\\"
    
    # # 전체 화면 캡처
    # capture_screen(save_path=absolute_path)

    # 특정 영역 캡처 (예: 좌상단에서 가로 300, 세로 400)
    absolute_path = "C:\\Users\\barrett11357\\Downloads\\screenshotTest\\"
    capture_screen(region=(0, 0, 300, 400), save_path=absolute_path)

    for i in range(5):
        capture_screen(region=(0, 0, 300, 400), save_path=absolute_path)