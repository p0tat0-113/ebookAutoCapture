from tkinter import * #tkinter라이브러리 임포트
from tkinter import ttk #테마 위젯을 제공하는 하위 모듈

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        print(meters.get())
    except ValueError:
        print("에러")
        pass

root = Tk()#메인 애플리케이션창 설정
root.title("Feet to Meters")#창의 제목 설정
#root의 메서드들을 호출해서 애플리케이션의 창 설정을 만짐.

#콘텐츠 프레임을 생성하고, 그 안에 사용자 인터페이스의 내용을 보관할 프레임 위젯을 만듦.
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)#columnconfigure/rowconfigure bits tell Tk that the frame should expand to fill any extra space if the window is resized.
root.rowconfigure(0, weight=1)
#프레임을 없이도 메인 창에 위젯들을 넣을 수 있지만, 그러면 배경색이 맞지 않아서 프레임을 만들어서 넣어준다는 것 같음.

#피트를 입력할 entry widget생성
feet = StringVar()#StringVar는 Tkinter에서 제공하는 변수 클래스다. StringVar는 문자열 값을 저장하기 위한 클래스. 얘 말고 intvar doubleVar도 있음. .set() .get()으로 값을 넣고 뺌.

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
#mainframe: 위젯이 들어갈 부모를 지정, width=7 textvariable=feet 은 configuration options임. 7개의 문자가 보이도록 길이를 지정함. textvariable로 입력한 값이 feet에 입력되게 함.

feet_entry.grid(column=2, row=1, sticky=(W, E))#위젯을 어디에 넣을지 행과 열을 지정함. sticky는 정렬 옵션임. 지금 왼쪽 오른쪽을 다 선택해서 중앙으로 정렬됨.

#나머지 위젯들도 생성하고, 어떤 그리드를 지정함.
meters = StringVar()#Tkinter에서 제공하는 변수 클래스. .set() .get()으로 값을 넣고 뺌.

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))#textvariable로 meters를 넣어줌. 위의 calculate함수의 결과가 meters로 들어간다.

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=2, row=3, sticky=(W,E))#command로 버튼을 눌렀을 때 실행될 함수의 참조값을 넘겨줌. 

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)


#인터페이스를 다듬어줌.

#서로 엉키지 않도록 모든 자식 요소들에 패딩을 추가해줌.
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()#tells Tk to put the focus on our entry widget. That way, the cursor will start in that field, so users don't have to click on it before starting to type.
root.bind("<Return>", calculate)#사용자가 엔터키를 누르면 calculate가 작동되도록 바인딩해줌.

root.mainloop()#이벤트 루프 시작