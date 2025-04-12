import json
import os
from datetime import datetime
import utils

class Statistics():
    def __init__(self):
        self.stats_file = "data/game_stats.json"
        self.history = []
        self.load_stats()
        self.summary_labels = {}
        self.check_folder()
        self.count_file = "data/count.json"
        self.data = self.load_games_count_data()
    
    def check_folder(self):
        dirs = ['data/', 'export/']
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
                print(f'创建文件夹 {d}')

    def load_stats(self):
        """加载历史数据"""
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                try:
                    self.history = json.load(f)
                except json.JSONDecodeError:
                    self.history = []

    def save_stats(self):
        """保存数据到文件"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_record(self, grid_size, time_taken):
        """添加新记录"""
        record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'grid_size': grid_size,
            'time': time_taken,
            'formatted_time': utils.format_time(time_taken)
        }
        self.history.append(record)
        self.save_stats()

    def get_grouped_stats(self):
        """按网格尺寸分组的统计信息"""
        stats = {}
        for record in self.history:
            size = record['grid_size']
            if size not in stats:
                stats[size] = {
                    'count': 0,
                    'times': [],
                    'best_time': float('inf'),
                    'worst_time': 0
                }
            
            stats[size]['count'] += 1
            stats[size]['times'].append(record['time'])
            if record['time'] < stats[size]['best_time']:
                stats[size]['best_time'] = record['time']
            if record['time'] > stats[size]['worst_time']:
                stats[size]['worst_time'] = record['time']
        
        # 计算平均值
        for size in stats:
            stats[size]['average_time'] = sum(stats[size]['times']) / stats[size]['count']
        
        return stats
    
    def load_games_count_data(self):
        """加载游戏次数文件"""
        try:
            with open(self.count_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 文件不存在或解析错误时创建文件初始化数据
            with open(self.count_file, "w") as f:
                json.dump({}, f)
            return {}
    
    def update_games_count(self):
        """更新今日游戏次数"""
        today_date = datetime.now().strftime("%Y-%m-%d")
        today_count = self.data.get(today_date, 0)
        self.data[today_date] = today_count + 1
    
    def get_today_games_count(self):
        """获取今日游戏次数"""
        today_date = datetime.now().strftime("%Y-%m-%d")
        with open(self.count_file, "w") as f:
            json.dump(self.data, f)
        try:
            return self.data[today_date]
        except KeyError:
            self.data[today_date] = 0
            with open(self.count_file, "w") as f:
                json.dump(self.data, f)
            return self.data[today_date]

if __name__ == '__main__':
    statis = Statistics()
    hist = statis.history
    summary = statis.get_grouped_stats()
    
    #print(hist)
    #print(summary)
    
    print(statis.get_today_games_count())
    