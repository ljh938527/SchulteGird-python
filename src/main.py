'''
    Program : Shulte-gird
    Author : ljh938527
    Project-Url : https://github.com/ljh938527/SchulteGird-python
'''
import tkinter as tk
from tkinter import simpledialog, messagebox
import pygame
from threading import Thread
from game import Game
from utils import format_time

version = ["1", "1", "0"]
versions = '.'.join(version)

pygame.mixer.init()

class GUI(Game):
    def __init__(self):
        super(GUI, self).__init__()
        self.root = tk.Tk()
        self.root.title('舒尔特方格 - v' + versions)
        self.root.geometry("600x600")
        self.root.minsize(600, 600)
        self.root.resizable(True, True)
        self.grid_frame = tk.Frame(self.root)  # 按钮容器
        self.grid_frame.place(relx=0.5, rely=0.5, anchor="center")  # 居中显示
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # 窗口内属性
        self.buttons = []
        self.size_var = tk.StringVar(value=str(self.grid_size))
        self.enable_gray = tk.BooleanVar(value=True)
        self.enable_play_sound = tk.BooleanVar(value=True)
        
        self.interface()
    
    def setup_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        
        # 游戏菜单
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="新游戏", command=self.gameRestart)
        game_menu.add_separator()
        game_menu.add_command(label="统计信息", command=self.show_statistics)
        game_menu.add_separator()
        game_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="游戏", menu=game_menu)
        # 设置菜单
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="设置尺寸", command=self.change_grid_size)
        settings_menu.add_separator()
        settings_menu.add_checkbutton(label="按钮变灰", variable=self.enable_gray)
        settings_menu.add_checkbutton(label="音效", variable=self.enable_play_sound)
        menubar.add_cascade(label="设置", menu=settings_menu)
        self.root.config(menu=menubar)
    
    def play_sound(self, file_path):
        """播放音效"""
        def _play():
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
            except pygame.error as e:
                print(f'播放失败: {e}')
        # 多线程后台播放
        play = Thread(target=_play, daemon=True)
        play.start()
            
    def play_error_sound(self):
        """播放错误音效"""
        self.play_sound('assets/Error10.mp3')
    
    def on_closing(self):
        """窗口关闭事件处理"""
        pygame.mixer.quit()
        pygame.quit()
        self.root.destroy()
    
    def handle_button_on_click(self, btn, num):
        """处理按钮点击事件"""
        if not self.timer_running:
            self.start_timer()
        #print(f"点击了: {int(num)}")
        if int(num) != self.current_number:
            self.count_click_wrong()
            if self.enable_play_sound.get():
                self.play_error_sound()  # 播放音效
        else:
            self.next_number()
            if self.enable_gray.get():
                btn.config(bg="GREY")
            if self.is_completed():
                self.stop_timer()
                elapsed = self.passed_time()
                self.stats.add_record(self.grid_size, elapsed)  # 保存记录
                messagebox.showinfo("恭喜", f"已完成！总用时：{format_time(elapsed)}，错误次数：{self.wrong_count}")
                self.current_number = 1
                for btn in self.buttons:
                    btn.config(bg="GREEN")

    def gameRestart(self):
        """重开按钮"""
        self.resetGame()
        self.time_label.config(text="用时：00:00.00")
        self.generate_grid()
        self.size_var.set(str(self.grid_size))
        self.reput_buttons()
    
    def show_statistics(self):
        """显示分组统计信息"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("分组统计信息")
        # 主容器
        main_frame = tk.Frame(stats_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧历史记录
        history_frame = tk.LabelFrame(main_frame, text="历史记录")
        history_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 右侧统计摘要
        stats_frame = tk.LabelFrame(main_frame, text="统计摘要")
        stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        
        # 历史记录列表
        scrollbar = tk.Scrollbar(history_frame)
        self.history_text = tk.Text(
            history_frame,
            yscrollcommand=scrollbar.set,
            width=40,
            height=15,
            state=tk.DISABLED
        )
        scrollbar.config(command=self.history_text.yview)
        # 填充历史数据
        self.update_history_display()
        
        # 统计摘要布局
        grouped_stats = self.stats.get_grouped_stats()
        for size in sorted(grouped_stats.keys()):
            frame = tk.Frame(stats_frame)
            frame.pack(fill=tk.X, pady=5)
            
            title = tk.Label(frame, text=f"{size}x{size} 统计", font=('Arial', 10, 'bold'))
            title.pack(anchor='w')
            
            stats = grouped_stats[size]
            text = (
                f"游戏次数: {stats['count']}\n"
                f"平均用时: {format_time(stats['average_time'])}\n"
                f"最佳成绩: {format_time(stats['best_time'])}\n"
                f"最长用时: {format_time(stats['worst_time'])}"
            )
            self.stats.summary_labels[size] = tk.Label(frame, text=text, justify=tk.LEFT)
            self.stats.summary_labels[size].pack(anchor='w')
        
        # 布局
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 底部按钮
        btn_frame = tk.Frame(stats_window)
        btn_frame.pack(pady=5)
        tk.Button(
            btn_frame,
            text="导出数据",
            command=self.export_stats
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            btn_frame,
            text="关闭",
            command=stats_window.destroy
        ).pack(side=tk.LEFT)
    
    def update_history_display(self):
        """更新历史记录显示"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        # 表头
        header = f"{'日期':<20}{'尺寸':<8}{'用时':<10}\n"
        self.history_text.insert(tk.END, header)
        self.history_text.insert(tk.END, "-"*38 + "\n")
        
        # 记录按时间倒序排列
        for record in reversed(self.stats.history):
            line = f"{record['date']:<20}" \
                   f"{record['grid_size']}x{record['grid_size']:<8}" \
                   f"{record['formatted_time']:<10}\n"
            self.history_text.insert(tk.END, line)
        
        self.history_text.config(state=tk.DISABLED)
    
    def export_stats(self):
        """导出统计数据到文件"""
        export_file_path = "export/game_stats.txt"
        with open(export_file_path, "w") as f:
            f.write("游戏统计记录\n")
            f.write(f"{'日期':<20}{'尺寸':<10}{'用时':<10}\n")
            f.write("-"*40 + "\n")
            for record in self.stats.history:
                f.write(f"{record['date']:<20}"
                        f"{record['grid_size']}x{record['grid_size']:<10}"
                        f"{record['formatted_time']:<10}\n")
        messagebox.showinfo("导出成功", f"数据已保存到 {export_file_path}")
    
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
                self.gameRestart()
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
        
        time_frame = tk.Frame(self.root)
        time_frame.pack(pady=15)
        self.time_label = tk.Label(
            time_frame,
            text="用时：00:00.00",
            font=("Arial", 12))
        self.time_label.pack()
        
        self.generate_grid()
        self.create_buttons()
        

if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()
    