from random import shuffle
import time
from utils import make_table

class Game():
    def __init__(self):
        self.current_number = 1
        
        self.start_time = None
        self.time_label = None
        self.timer_running = False
        
        self.grid_size = 5
        self.grid = []
        
    
    def generate_grid(self):
        """生成数字网格"""
        numbers = [str(i) for i in range(1, self.grid_size**2 + 1)]
        shuffle(numbers)
        self.grid = make_table(numbers, self.grid_size)
    
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


if __name__ == "__main__":
    game = Game()
    
    game.generate_grid()
    print(game.grid)
    