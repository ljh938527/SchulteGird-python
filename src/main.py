'''
    Program : Shulte-gird
    Author : ljh938527
    Project-Url : https://github.com/ljh938527/SchulteGird-python
'''
import tkinter as tk
from tkinter import messagebox
#from pygame import mixer
import random
import time

version = "0.1.0"

class GUI():
    def __init__(self):
        super(GUI, self).__init__()
        self.root = tk.Tk()
        self.root.title('舒尔特方格 - v' + version)
        self.root.geometry("400x400")
        self.root.resizable(True, True)
        self.button_frame = tk.Frame(self.root)  # 按钮容器
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")  # 居中显示
        
        self.textList = ["1", "2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]
        self.numList = []
        self.current_number = 1
        self.buttons = []
        self.start_time = None  # 开始时间
        self.time_label = None
        self.timer_running = False  # 计时器状态

        self.interface()

    def make_table(self, list, a) -> list:
        """将列表转为a*a的二维数组"""
        return [list[i:i+a] for i in range(0, a*a, a)]

    def shuffleList(self, list):
        """打乱列表"""
        random.shuffle(list)

    def start_timer(self):
        """启动计时器"""
        self.start_time = time.time()
        self.timer_running = True
        self.update_time_display()

    def stop_timer(self):
        """停止计时器"""
        self.timer_running = False
    
    def get_elapsed_time(self):
        """获取格式化时间字符串"""
        if self.start_time is None:
            return "00:00.00"
        elapsed = time.time() - self.start_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        millis = int((elapsed - int(elapsed)) * 100)
        return f"{mins:02}:{secs:02}.{millis:02}"

    def update_time_display(self):
        """更新界面时间显示"""
        if self.timer_running:
            self.time_label.config(text=f"用时：{self.get_elapsed_time()}")
            self.root.after(10, self.update_time_display)  # 每10ms更新一次

    def handle_button_on_click(self, btn, num):
        """处理按钮点击事件"""
        if not self.timer_running:
            self.start_timer()
        #print(f"点击了: {int(num)}")
        self.numList.append(num)
        if int(num) != self.current_number:
            print("错误音效")
            
        else:
            self.current_number += 1
            #btn.config(bg="GREY")
            print("没问题")
            if self.current_number > 16:
                self.stop_timer()
                messagebox.showinfo("恭喜", f"已完成！总用时：{self.get_elapsed_time()}")
                self.current_number = 1

    def gameRestart(self):
        """重开按钮，更新界面"""
        self.stop_timer()
        self.shuffleList(self.textList)
        self.table = self.make_table(self.textList, 4)
        self.current_number = 1
        self.start_time = None
        self.time_label.config(text="用时：00:00.00")
        self.update()

    def update(self):
        """更新按钮"""
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()
        for i in range(4):
            for j in range(4):
                text_value = self.table[j][i]
                Button1 = tk.Button(self.button_frame, text=text_value, font=("Arial", 12, 'bold'), fg="WHITE", bg="GREEN", width=3, height=2)
                Button1.config(command=lambda btn=Button1, num=text_value: self.handle_button_on_click(btn, num))  # 使用lambda传递参数
                Button1.grid(row=j, column=i, padx=2, pady=2)
                self.buttons.append(Button1)

    def interface(self):
        """窗口布局显示"""
        time_frame = tk.Frame(self.root)
        time_frame.pack(pady=15)
        
        self.time_label = tk.Label(
            time_frame,
            text="用时：00:00.00",
            font=("Arial", 12))
        self.time_label.pack()
        
        self.shuffleList(self.textList)
        self.table = self.make_table(self.textList, 4)
        self.update()

        Button2= tk.Button(self.root, text="重开", font=("Arial", 10, 'bold'), command=self.gameRestart)
        Button2.place(x=10, y=10)
        

if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()