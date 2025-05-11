Quantum Chess 

Welcome to Quantum Chess, a student-developed Python game that blends classical chess mechanics with elements of quantum mechanics — including superposition, entanglement, and probabilistic collapse.

This project is built using pygame for the GUI and includes custom SVG-based assets and unique gameplay mechanics.

🎮 Features

Classic Chess Base: Full implementation of standard chess board and pieces.
Quantum Mechanics Integration**:
Superposition: Pieces can exist in two locations simultaneously with a 50% probability.
Entanglement: Pieces can be entangled across positions, affecting each other’s behavior.
Measurement Collapse: Pieces in superposition will collapse to a single state during gameplay.
Animated UI: Smooth welcome screen, player choice animations, and stylized board.
Side Selection: Choose to be the White Heroic Knight or the Dark Night.
AI Opponent: Basic computer player with quantum move chances and collapse logic.
Move Log Panel: Displays the last 4 moves for reference during play.

📁 Directory Structure

project/
│
├── test2.py                  Main game file with UI and game loop
├── board.py                Logic for board initialization and movement (if separate)
├── Assets/
│   ├── p1/
│   │   ├── king-w\.svg
│   │   ├── bishop-b.svg
│   │   └── ... (other piece images)
│   └── boards/
│       └── rect-8x8.svg    # SVG board image


## 🛠️ Requirements

Python 3.8 or above
Required libraries:
  - pygame
  - cairosvg

Install dependencies using:

bash
pip install pygame cairosvg cairocffi

https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/tag/2022-01-04
download the .exe file and install it and after that go on windows enviourment and edit the enviourment add new and place the bin directory 


🚀 Getting Started

1. Clone or download the repository.
2. Make sure all assets (SVGs and background images) are correctly located in the Assets folder as per the paths used in the code.
3. Run the game:

bash
python test2.py


4. Use W or B to choose your side and enjoy the game!

⚙️ Controls & Gameplay

| Action                   | Key                   |
| ------------------------ | --------------------- |
| Toggle Quantum Mode      | Q                     |
| Select/Move Pieces       | Mouse Click           |
| Choose Side (Start Menu) | W (White) / B (Black) |
| Exit Game                | Close Window or ESC   |

* Quantum Mode allows for 50/50 splitting of pieces.
* Collapse occurs randomly for AI or by logic during movement or conflict.
* Entangled pieces show a yellow dot indicator.


📦 Features in Progress

* Checkmate and stalemate logic in quantum mode
* Enhanced AI using probability trees
* Networked multiplayer
* Save/Load quantum states

🧠 Inspiration

This project was inspired by real-world research in quantum computation and games like [Quantum Chess by Chris Cantwell](https://quantumchess.net/), aiming to explore quantum concepts through interactive play.

📜 License

This project is for educational and research purposes. Feel free to modify and expand for personal or academic use.

🤝 Contributing

If you'd like to contribute or report bugs, feel free to fork this repository or open an issue.



👨‍💻 Developed By

Ayan Mohammad Zakriya K224728 
Hamza Yousuf          K224748 
Sami-ur-Rehman        K224673

BSCYS Students, FAST NUCES Karachi Campus



