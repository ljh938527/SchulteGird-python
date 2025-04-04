# 舒尔特方格训练工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

基于Python的认知训练工具，用于提升周边视觉和专注力

## ✨ 功能特点

- **可调网格尺寸**: 支持3x3到6x6的网格
- **双主题模式**: 亮色/暗黑主题切换
- **数据统计系统**:
  - 毫秒级精确计时
  - 历史记录存储
  - 分尺寸成绩分析
- **声音反馈**: 错误提示音效
- **数据导出**: 支持统计信息导出

## 🚀 安装与运行

### 环境要求
- Python 3.9+

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Schulte-grid.git
cd Schulte-grid
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python src/main.py
```

*Windows用户可双击运行`setup.bat`进行自动配置*

## 🎮 使用说明

1. **游戏操作**：
   - 按升序点击数字
   - 正确点击推进进度
   - 错误触发提示音

2. **菜单功能**：
   - `新游戏`：开启当前尺寸新游戏
   - `统计信息`：查看历史成绩
   - `网格尺寸`：通过输入框或菜单调整

## 📁 项目结构

```
Schulte-grid/
├── src/
│   ├── assets/          # 资源文件
│   ├── game.py          # 核心游戏逻辑
│   ├── main.py          # 图形界面入口
│   ├── statistics.py    # 数据处理模块
│   └── utils.py         # 工具函数
├── requirements.txt     # 依赖列表
└── setup.bat            # Windows安装脚本
```

## 📜 开源许可

MIT 许可证 - 详情请见 [LICENSE](LICENSE)