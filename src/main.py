'''
    Program : Shulte-gird
    Author : ljh938527
    Project-Url : https://github.com/ljh938527/SchulteGird-python
'''
import tkinter as tk
import random

version = "0.1.0"

class GUI():
    def __init__(self):
        super(GUI, self).__init__()
        self.root = tk.Tk()
        self.root.title('舒尔特方格 - v' + version)
        self.root.geometry("400x400")
        
        self.textList = ["1", "2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]
        self.numList = []
        self.current_number = 1
        self.buttons = []

        self.interface()
    
    def make_table(self, list, a):  # 列表转二维数组，生成矩阵
        return [list[i:i+a] for i in range(0, a*a, a)]
    
    def shuffleList(self, list):  # 打乱列表
        random.shuffle(list)

    def handle_button_on_click(self, num):
        '''
        * Function : 处理按钮事件
        * Description : 若点击数字与当前数字相同则继续，不相同则播放错误音效
        '''
        #print(f"点击了: {int(num)}")
        self.numList.append(num)
        if int(num) != self.current_number:
            print("错误音效")
        else:
            self.current_number += 1
            print("没问题")
        #print(f"当前数字: {self.current_number} \n")
        

    def shuffleTable(self):  # 乱序按钮
        self.shuffleList(self.textList)
        self.table = self.make_table(self.textList, 4)
        self.update()
        self.current_number = 1

    def update(self):
        '''
        * Function : 用于更新按钮
        * Description : 每次更新先销毁旧按钮，再生成新按钮
        '''
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()
        for i in range(1, 5):
            for j in range(1, 5):
                text_value = self.table[j-1][i-1]
                Button1 = tk.Button(
                    self.root, 
                    text=text_value, 
                    font=("Arial", 12, 'bold'), 
                    fg="WHITE",
                    bg="GREEN", 
                    command=lambda num=text_value: self.handle_button_on_click(num),  # 使用lambda传递参数
                    width=3, 
                    height=2
                )
                Button1.place(x=100*i, y=100*j)
                self.buttons.append(Button1)

    def interface(self):  # 窗口布局
        self.shuffleList(self.textList)
        self.table = self.make_table(self.textList, 4)
        self.update()

        Button2= tk.Button(self.root, text="乱序", font=("Arial", 10, 'bold'), command=self.shuffleTable)
        Button2.place(x=50, y=10)
        

if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()