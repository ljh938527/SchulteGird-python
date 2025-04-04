from random import shuffle
import time
from utils import make_table
from statistics import Statistics

class Game():
    def __init__(self):
        self.current_number = 1
        self.wrong_count = 0
        
        self.start_time = None
        self.time_label = None
        self.timer_running = False
        
        self.grid_size = 5
        self.grid = []
        self.stats = Statistics()
    
    def generate_grid(self):
        """生成数字网格"""
        numbers = [str(i) for i in range(1, self.grid_size**2 + 1)]
        shuffle(numbers)
        self.grid = make_table(numbers, self.grid_size)
    
    def next_number(self):
        """点击数自增"""
        self.current_number += 1
    
    def count_click_wrong(self):
        """错误数自增"""
        self.wrong_count += 1
    
    def is_completed(self) -> bool:
        """游戏胜利"""
        return self.current_number > self.grid_size**2
    
    def update_time_display(self):
        pass
    
    def start_timer(self):
        """启动计时器"""
        self.start_time = time.time()
        self.timer_running = True
        self.update_time_display()

    def stop_timer(self):
        """停止计时器"""
        self.timer_running = False
    
    def passed_time(self) -> float:
        """计算已过时间"""
        return time.time() - self.start_time
    
    def resetGame(self):
        """重置游戏"""
        self.stop_timer()
        self.current_number = 1
        self.wrong_count = 0
        self.start_time = None

if __name__ == "__main__":
    game = Game()
    
    game.generate_grid()
    print(game.grid)
    