# Schulte Grid Training Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based cognitive training tool to improve peripheral perception and focus.

## ✨ Features

- **Customizable Grid Size**: 3x3 to 10x10 grids
- **Dark/Light Themes**: Eye-friendly interface
- **Game Statistics**:
  - Time tracking with millisecond precision
  - Session history storage
  - Size-specific performance analysis
- **Audio Feedback**: Error sound indication
- **Data Export**: Save statistics to text file

## 🚀 Installation & Running

### Requirements
- Python 3.9+

1. Clone repository:
```bash
git clone https://github.com/yourusername/Schulte-grid.git
cd Schulte-grid
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

*Windows users can double-click `setup.bat` for automatic setup*

## 🎮 Usage

1. **Main Game**:
   - Click numbers in ascending order
   - Correct clicks advance progress
   - Errors trigger sound feedback

2. **Controls**:
   - `Restart`: New game with current size
   - `Statistics`: View performance history
   - `Grid Size`: Use spinbox or menu to change

## 📁 Project Structure

```
Schulte-grid/
├── src/
│   ├── assets/          # Resource files
│   ├── game.py          # Core game logic
│   ├── main.py          # GUI entry point
│   ├── statistics.py    # Data handling
│   └── utils.py         # Helper functions
├── requirements.txt     # Dependencies
└── setup.bat            # Windows setup script
```

## 📜 License

MIT License - See [LICENSE](LICENSE) for details