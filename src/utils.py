
def make_table(lst, a) -> list:
    """将列表转为a*a的二维数组"""
    return [lst[i:i+a] for i in range(0, a*a, a)]

def format_time(seconds):
    """格式化时间字符串"""
    if seconds is None:
        return "00:00.00"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 100)
    return f"{mins:02}:{secs:02}.{millis:02}"

def centerWindow(window, weidth, height):
    """使窗口显示于屏幕中央"""
    sweidth = window.winfo_screenwidth()
    sheight = window.winfo_screenheight()
    window.geometry('%dx%d+%d+%d' % (weidth, height, (sweidth-weidth)/2, (sheight-height)/2))


if __name__ == "__main__":
    arr = [i for i in range(1,50)]
    print(make_table(arr, 3))
    print(make_table(arr, 4))
    print(make_table(arr, 5))
    
    time = 666.66
    print(format_time(time))