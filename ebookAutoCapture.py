#from pywinauto.keyboard import send_keys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pyautogui
import mss
import mss.tools
import time
from datetime import datetime


class ebookToPDF:

    def __init__(self, root):

        #좌측 상단, 우측 하단 좌표를 저장하는 변수들
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        #좌표를 UI에 표시해주는 변수들
        self.posDisplay1 = StringVar()
        self.posDisplay2 = StringVar()
        self.posDisplay1.set("[0,0]")
        self.posDisplay2.set("[0,0]")

        self.pages = IntVar()#캡쳐 페이지 수

        self.name = StringVar()#파일 이름

        self.dirPath = StringVar()#파일 저장 경로

        self.captureSpeed = IntVar()#캡쳐 간격
        self.captureSpeed.set(200)

        self.moveToNextPageOption = IntVar()#다음 페이지 이동 옵션(0: 키보드 오른쪽 방향키, 1: 마우스 좌클릭)

        self.progress = DoubleVar()#진행율 
        self.progress.set(0.0)

        root.title("eBookAutoCapture")
        root.geometry("")#이렇게 해야 내부 위젯들 사이즈에 맞게 창의 크기가 자동으로 조절됨. https://stackoverflow.com/questions/50955987/auto-resize-tkinter-window-to-fit-all-widgets
        root.resizable(width=False, height=False)      

        contents = ttk.Frame(root, padding="3 3 3 3")
        contents.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(contents, text="madeBy p0tat0-113", ).grid(column=1, row=1, columnspan=3, sticky=W)
        ttk.Label(contents, text="설정 버튼을 누른 후 space키를 눌러야 좌표가 기입됨").grid(column=1, row=2, columnspan=3, sticky=W)

        ttk.Label(contents, text="좌측 상단 좌표", ).grid(column=1, row=3, sticky=W)
        ttk.Label(contents, text="우측 하단 좌표", ).grid(column=1, row=4, sticky=W)
        ttk.Label(contents, textvariable=self.posDisplay1, width=10).grid(column=2, row=3, sticky=(W, E))
        ttk.Label(contents, textvariable=self.posDisplay2, width=10).grid(column=2, row=4, sticky=(W, E))
        ttk.Button(contents, text="좌표 설정", command=self.callGetPointerPosLeft).grid(column=3, row=3, sticky=(W, E))
        ttk.Button(contents, text="좌표 설정", command=self.callGetPointerPosRight).grid(column=3, row=4, sticky=(W, E))

        ttk.Label(contents, text="총 페이지 수").grid(column=1, row=5, sticky=W)
        ttk.Label(contents, text="파일 이름").grid(column=1, row=6, sticky=W)
        ttk.Entry(contents, width=10, textvariable=self.pages).grid(column=3, row=5, sticky=(W, E))
        ttk.Entry(contents, width=10, textvariable=self.name).grid(column=3, row=6, sticky=(W, E))

        ttk.Label(contents, text="캡쳐 간격(ms)").grid(column=1, row=7, sticky=W)
        ttk.Label(contents, textvariable=self.captureSpeed,width=3).grid(column=2, row=7, sticky=(W, E))
        ttk.Scale(contents, orient=HORIZONTAL, length=100, from_=1, to=1000, variable=self.captureSpeed, command=self.floatToInt).grid(column=3, row=7, sticky=(W,E))

        ttk.Label(contents, text="다음 페이지 이동").grid(column=1, row=8, sticky=W)
        ttk.Radiobutton(contents, text="키보드 방향키", variable=self.moveToNextPageOption, value=0).grid(column=2, row=8, sticky=W)
        ttk.Radiobutton(contents, text="마우스 클릭", variable=self.moveToNextPageOption, value=1).grid(column=3, row=8, sticky=W)

        ttk.Progressbar(contents, orient=HORIZONTAL,length=30, mode='determinate', maximum = 10000, variable=self.progress).grid(column=1, row=9, columnspan=3, sticky=(W,E))

        ttk.Button(contents, text="작업 시작", command=self.captureCall).grid(column=1, row=10,columnspan=3, sticky=(W,E))
        ttk.Button(contents, text="저장 경로 설정", command=self.getDirPath).grid(column=1, row=11,columnspan=3, sticky=(W,E))
        ttk.Label(contents, text="경로", textvariable=self.dirPath, width=51).grid(column=1, row=12,columnspan=3, sticky=W)

        for child in contents.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
    
    def floatToInt(self, *args):#Scale바를 통해서 입력되는 값의 소숫점을 제거함.
        self.captureSpeed.set(round(self.captureSpeed.get(),0))

    def callGetPointerPosLeft(self,*args): #Tkinter를 통해서 호출되는 메서드는 매개변수로 반드시 *args를 가지고 있어야 함.
        print("callGetPointerPosLeft")
        root.bind("<Key-space>", lambda event: self.getPointerPos(event,1))#바인드된 함수에 인자를 넘기려면 이렇게 lambda로 우회적으로 넘겨야 함.
        root.focus_set()  # root로 포커스 강제 이동, 스페이스바를 눌렀을 때 버튼이 계속 눌리던 문제를 해결

    def callGetPointerPosRight(self,*args):
        print("callGetPointerPosRight")
        root.bind("<Key-space>", lambda event: self.getPointerPos(event,2))
        root.focus_set()  # root로 포커스 강제 이동

    def getPointerPos(self,event,position):
        posx,posy = pyautogui.position()
        if(position == 1):
            self.x1 = posx
            self.y1 = posy
            self.posDisplay1.set(str([posx,posy]))
        if(position == 2):
            self.x2 = posx
            self.y2 = posy
            self.posDisplay2.set(str([posx,posy]))
        #root.unbind("<Key-space>") 스페이스바를 여러번 눌러서 좌표를 수정할 수 있게함.

    def getDirPath(self, *args):
        self.dirPath.set(filedialog.askdirectory())
        print(self.dirPath.get())

    def captureCall(self, *args):
        capture = Capture()
        capture\
            .setRoot(root)\
            .setRegion(self.x1,self.y1,self.x2,self.y2)\
            .setPages(self.pages.get())\
            .setName(self.name.get())\
            .setDirpath(self.dirPath.get())\
            .setCaptureSpeed(self.captureSpeed.get())\
            .setProgres(self.progress)\
            .setMoveToNextPage(self.moveToNextPageOption.get())

        root.after(2000, capture.process)

class Capture:
    def __init__(self):
        self.root = None
        self.region = None
        self.pages = None
        self.name = None
        self.dirpath = None
        self.captureSpeed = None
        self.progress = None
        self.moveToNextPage = None
        self.count = 1

    def setRoot(self,root):
        self.root = root
        return self
    
    def setRegion(self,x1,y1,x2,y2):
        self.region = (x1,y1,x2-x1,y2-y1)
        return self
    
    def setPages(self,pages):
        self.pages = pages
        return self
    
    def setName(self,name):
        self.name = name
        return self
    
    def setDirpath(self,dirpath):
        self.dirpath = dirpath.replace("/","\\")
        return self
    
    def setCaptureSpeed(self,captureSpeed):
        self.captureSpeed = captureSpeed
        return self
    
    def setProgres(self,progress):
        '''ValueVar타입으로 받아야 함.'''
        self.progress = progress
        progress.set(0.0)
        return self
    
    def setMoveToNextPage(self,moveToNextPageOption):
        self.moveToNextPage = self.selectMoveToNextPageOption(moveToNextPageOption)
        return self

    def process(self):
        self.capture()

        self.progress.set(self.progress.get()+(10000/self.pages))
        self.moveToNextPage()
        self.count += 1

        if (self.count<=self.pages):
            root.after(self.captureSpeed,self.process)#Tkinter가 captureSpeed만큼의 ms가 지난 후 process()를 다시 호출함.
            #tkinter는 time.sleep을 쓰는게 좋지 않다고 함. 이렇게 해야 progressbar가 지속적으로 업데이트 됨.
            #https://stackoverflow.com/questions/51298758/tkinter-updating-progressbar-when-a-function-is-called

        print("작업 완료")

    def capture(self):
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        save_dir = str(f"{self.dirpath}\\{self.name}[{self.count}]{now}.png")
        print(save_dir)

        with mss.mss() as sct:
            monitor = {"top": self.region[1], "left": self.region[0], "width": self.region[2], "height": self.region[3]}
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_dir)
            
    def selectMoveToNextPageOption(self,num):
        if num == 0:
            return self.moveToNextPageWithKey
        elif num   == 1:
            return self.moveToNextPageWithClick
        
    #다음페이지로 넘겨주는 함수들
    def moveToNextPageWithKey(self):
        pyautogui.press("right")
        print("키보드 딸칵")

    def moveToNextPageWithClick(self):
        pyautogui.leftClick()
        print("마우스 딸칵")


root = Tk()
ebookToPDF(root)#FeetToMeters인스턴스를 생성하는 과정에서 생성자 함수가 호출되고, root에 모든 설정을 끝냄.
root.mainloop()