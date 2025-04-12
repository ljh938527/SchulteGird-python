'''
    Program : Shulte-gird
    Author : ljh938527
    Project-Url : https://github.com/ljh938527/SchulteGird-python
'''
import tkinter as tk
from tkinter import simpledialog, messagebox
import pygame
from PIL import Image, ImageTk
from threading import Thread
from game import Game
from utils import format_time

version = ["1", "2", "1"]
versions = '.'.join(version)

pygame.mixer.init()

class GUI(Game):
    def __init__(self):
        super(GUI, self).__init__()
        self.root = tk.Tk()
        self.root.title('舒尔特方格 - v' + versions)
        self.root.geometry("500x500")
        self.root.minsize(500, 500)
        self.root.resizable(True, True)
        self.grid_frame = tk.Frame(self.root)  # 按钮容器
        self.grid_frame.place(relx=0.5, rely=0.5, anchor="center")  # 居中显示
        self.tip_frame = tk.Frame(self.root)  # 提示框
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # 窗口内属性
        self.buttons = []
        self.size_var = tk.StringVar(value=str(self.grid_size))
        self.enable_gray = tk.BooleanVar(value=False)
        self.enable_play_sound = tk.BooleanVar(value=True)
        self.dark_mode = False
        #窗口主题
        self.theme_colors = {
            'light': {
                'bg': '#FFFFFF',
                'fg': '#000000',
                'button_bg': '#4CAF50',
                'button_fg': 'white',
                'hover_bg': '#45a049'
            },
            'dark': {
                'bg': '#2D2D2D',
                'fg': '#FFFFFF',
                'button_bg': '#2E7D32',
                'button_fg': 'white',
                'hover_bg': '#1B5E20'
            }
        }
        # 窗口布局
        self.interface()
        self.apply_theme()
    
    def setup_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        # 游戏菜单
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="新游戏(N)", command=self.gameRestart, underline=4, accelerator='F2')
        game_menu.add_separator()
        game_menu.add_command(label="设置尺寸(C)", command=self.change_grid_size, underline=5)
        game_menu.add_checkbutton(label="切换主题(E)", command=self.toggle_theme, underline=5)
        game_menu.add_separator()
        game_menu.add_checkbutton(label="按钮变灰(Y)", variable=self.enable_gray, underline=5)
        game_menu.add_checkbutton(label="音效(S)", variable=self.enable_play_sound, underline=3)
        game_menu.add_separator()
        game_menu.add_command(label="统计信息(T)", command=self.show_statistics, underline=5)
        game_menu.add_separator()
        game_menu.add_command(label="退出(X)", command=self.root.quit, underline=3)
        menubar.add_cascade(label="游戏(G)", menu=game_menu, underline=3)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="查看帮助(H)", command=self.help, underline=5)
        help_menu.add_separator()
        help_menu.add_command(label="关于(A)", command=self.about, underline=3)
        menubar.add_cascade(label="帮助(H)", menu=help_menu, underline=3)
        self.root.config(menu=menubar)
    
    def apply_theme(self):
        """应用主题"""
        theme = 'dark' if self.dark_mode else 'light'
        colors = self.theme_colors[theme]
        self.root.configure(bg=colors['bg'])
        self.grid_frame.configure(bg=colors['bg'])
        self.tip_frame.configure(bg=colors['bg'])
        self.time_label.configure(bg=colors['bg'], fg=colors['fg'])
        self.today_games_label.configure(bg=colors['bg'], fg=colors['fg'])
    
    def toggle_theme(self):
        """切换主题"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
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
    
    def play_success_sound(self):
        """播放完成音效"""
        self.play_sound('assets/success1.mp3')
    
    def on_closing(self):
        """窗口关闭事件处理"""
        pygame.mixer.quit()
        pygame.quit()
        self.root.destroy()
    
    def help(self):
        """帮助信息窗口"""
        help_window = tk.Toplevel()
        help_window.title('帮助信息')
        help_window.geometry("400x400")
        # 帮助文本
        help_text = tk.Label(
            help_window,
            text="这是舒尔特方格游戏的帮助信息。\n\n"
                 "1. 点击数字按顺序完成游戏。\n"
                 "2. 可以通过菜单切换主题、调整网格尺寸等。\n"
                 "3. 查看统计信息了解历史记录。\n",
            justify=tk.LEFT,
            wraplength=350
        )
        help_text.pack(pady=10)
        # 显示图片
        try:
            image = Image.open("assets/image.png")
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            img_label = tk.Label(help_window, image=photo)
            img_label.image = photo  # 防止图片被垃圾回收
            img_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(help_window, text=f"无法加载图片: {e}", fg="red")
            error_label.pack(pady=10)
        # 关闭按钮
        close_button = tk.Button(help_window, text="关闭", command=help_window.destroy)
        close_button.pack(pady=10)
    
    def about(self):
        """关于窗口"""
        about_window = tk.Toplevel()
        about_window.title('关于')
        program_text = tk.Label(about_window, text="舒尔特方格", font=("Arial", 10))
        program_text.pack(pady=10)
        author_text = tk.Label(about_window, text='作者: ljh938527', font=("Arial", 9))
        author_text.pack(pady=5)
        version_text = tk.Label(about_window, text=f'版本: {versions}', font=("Arial", 9))
        version_text.pack(pady=5)
        close_button = tk.Button(about_window, text="关闭", command=about_window.destroy)
        close_button.pack(pady=10)

    def handle_button_on_click(self, btn, num):
        """处理按钮点击事件"""
        if not self.timer_running:
            self.start_timer()
        #print(f"点击了: {int(num)}")
        if int(num) != self.current_number:
            self.count_click_wrong()
            if self.enable_play_sound.get():
                self.play_error_sound()  # 播放错误音效
        else:
            self.next_number()
            if self.enable_gray.get():
                btn.config(bg="GREY")
            if self.is_completed():
                self.stop_timer()
                elapsed = self.passed_time()
                self.stats.add_record(self.grid_size, elapsed)  # 保存记录
                self.play_success_sound()  #播放完成音效
                self.update_today_games_count()
                messagebox.showinfo("恭喜", f"已完成！总用时：{format_time(elapsed)}，错误次数：{self.wrong_count}")
                self.current_number = 1
                for btn in self.buttons:
                    btn.config(bg="GREEN")
    
    def update_today_games_count(self):
        """更新今日游戏次数"""
        self.stats.update_games_count() # 今日游戏次数加一
        self.today_games_label.config(
            text=f"今天游戏次数：{self.stats.get_today_games_count()}"
        ) #更新界面显示
    
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
            width=42,
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
        header = f"{'日期':<20}{'尺寸':<10}{'用时':<10}\n"
        self.history_text.insert(tk.END, header)
        self.history_text.insert(tk.END, "-"*38 + "\n")
        
        # 记录按时间倒序排列
        for record in reversed(self.stats.history):
            line = f"{record['date']:<21}"\
                   f"{record['grid_size']}x{record['grid_size']:<9}" \
                   f"{record['formatted_time']:<10}\n"
            self.history_text.insert(tk.END, line)
        
        self.history_text.config(state=tk.DISABLED)
    
    def export_stats(self):
        """导出统计数据到文件"""
        export_file_path = "export/game_stats.txt"
        self.stats.check_folder('export/')
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
            f"当前尺寸：{self.grid_size}\n请输入新尺寸(3-6)：",
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
                if self.grid_size >= 6:
                    self.root.geometry('700x700')
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
                Btn = tk.Button(self.grid_frame, text=text_value, font=("Arial", 12, 'bold'), fg="WHITE", bg="GREEN", width=4, height=2)
                Btn.config(command=lambda btn=Btn, num=text_value: self.handle_button_on_click(btn, num))  # 使用lambda传递参数
                Btn.grid(row=j, column=i, padx=1, pady=1)
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
        
        # 显示用时
        self.tip_frame.pack(pady=15)
        self.time_label = tk.Label(
            self.tip_frame,
            text="用时：00:00.00",
            font=("Arial", 12))
        self.time_label.pack()
        
        # 显示今天游戏次数
        self.today_games_label = tk.Label(
            self.tip_frame,
            text=f"今天游戏次数：{self.stats.get_today_games_count()}",
            font=("Arial", 12))
        self.today_games_label.pack()
        
        self.generate_grid()
        self.create_buttons()
    

if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()
