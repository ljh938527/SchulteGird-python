'''
    Program : Shulte-gird
    Author : ljh938527
    Project-Url : https://github.com/ljh938527/SchulteGird-python
'''
import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import winsound
from game import Game
from window import menu
from utils import format_time

version = ["1", "0", "0"]
versions = '.'.join(version)

class GUI(Game):
    def __init__(self):
        super(GUI, self).__init__()
        self.root = tk.Tk()
        self.root.title('舒尔特方格 - v' + versions)
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        self.grid_frame = tk.Frame(self.root)  # 按钮容器
        self.grid_frame.place(relx=0.5, rely=0.5, anchor="center")  # 居中显示
        self.buttons = []
        
        self.interface()
    
    def setup_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="新游戏", command=self.gameRestart)
        game_menu.add_command(label="设置尺寸", command=self.change_grid_size)
        game_menu.add_separator()
        game_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="游戏", menu=game_menu)
        self.root.config(menu=menubar)
    
    def handle_button_on_click(self, btn, num):
        """处理按钮点击事件"""
        if not self.timer_running:
            self.start_timer()
        #print(f"点击了: {int(num)}")
        if int(num) != self.current_number:
            winsound.Beep(1000,200)
        else:
            self.current_number += 1
            btn.config(bg="GREY")
            if self.current_number > self.grid_size**2:
                self.stop_timer()
                messagebox.showinfo("恭喜", f"已完成！总用时：{format_time(self.passed_time())}")
                self.current_number = 1
                for btn in self.buttons:
                    btn.config(bg="GREEN")

    def gameRestart(self):
        """重开按钮，更新界面"""
        self.stop_timer()
        self.generate_grid()
        self.current_number = 1
        self.start_time = None
        self.time_label.config(text="用时：00:00.00")
        self.size_var.set(str(self.grid_size))
        self.reput_buttons()
    
    def change_grid_size(self):
        """修改网格尺寸"""
        new_size = simpledialog.askinteger(
            "设置尺寸",
            f"当前尺寸：{self.grid_size}\n请输入新尺寸（3-6）：",
            parent=self.root,
            minvalue=3,
            maxvalue=6
        )
        
        if new_size and new_size != self.grid_size:
            self.grid_size = new_size
            self.gameRestart()
    
    def on_size_change(self):
        """Spinbox尺寸修改事件"""
        try:
            new_size = int(self.size_var.get())
            if 3 <= new_size <= 6:
                self.grid_size = new_size
                self.restart_game()
            else:
                raise ValueError
        except ValueError:
            self.size_var.set(str(self.grid_size))
            messagebox.showerror("错误", "请输入3-6之间的整数")
    
    def update_time_display(self):
        """更新界面时间显示"""
        if self.timer_running:
            self.time_label.config(text=f"用时：{format_time(self.passed_time())}")
            self.root.after(10, self.update_time_display)  # 每10ms更新一次
    
    def create_buttons(self):
        """创建按钮"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                text_value = self.grid[i][j]
                Btn = tk.Button(self.grid_frame, text=text_value, font=("Arial", 12, 'bold'), fg="WHITE", bg="GREEN", width=3, height=2)
                Btn.config(command=lambda btn=Btn, num=text_value: self.handle_button_on_click(btn, num))  # 使用lambda传递参数
                Btn.grid(row=j, column=i, padx=2, pady=2)
                self.buttons.append(Btn)
    
    def reput_buttons(self):
        """重放按钮"""
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()
        self.create_buttons()
    
    def interface(self):
        """窗口布局显示"""
        self.setup_menu()
        self.size_var = tk.StringVar(value=str(self.grid_size))
        time_frame = tk.Frame(self.root)
        time_frame.pack(pady=15)
        self.time_label = tk.Label(
            time_frame,
            text="用时：00:00.00",
            font=("Arial", 12))
        self.time_label.pack()
        
        self.generate_grid()
        self.create_buttons()

        Button1 = tk.Button(self.root, text="打乱", font=("Arial", 10, 'bold'), command=self.gameRestart)
        #Button1.place(x=10, y=10)
        
        
    

if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()
    
    