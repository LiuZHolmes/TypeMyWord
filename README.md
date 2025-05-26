# TypeMyWord

TypeMyWord is a command-line tool for practicing word spelling. It reads a CSV file containing words and their explanations, then quizzes you by asking you to type each word correctly. You can reveal the explanation for each word if needed.

TypeMyWord uses the [FSRS](https://github.com/open-spaced-repetition/fsrs) (Free Spaced Repetition Scheduler) algorithm for intelligent scheduling and memory tracking. This allows for more scientific and personalized word review intervals, similar to Anki's advanced scheduling.

## Features
- Scan the `words/` directory for available word lists (CSV files)
- Randomly quiz you on the words in the selected file
- Show explanations on demand (press `Ctrl+E`)
- Start quiz (press `Ctrl+B`)
- Skip word (press `Ctrl+S`)
- Quit the app (press `Ctrl+K`)
- Simple command-line interface

## Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd TypeMyWord
```

### 2. Set up a virtual environment (recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare your word lists
- Place your CSV files in the `words/` directory.
- Each CSV should have at least three columns: `id,word,explanation` (header required).
  - For best experience, you can also include: `due,memory_state,scheduled_days,last_review` (these will be auto-managed by the program).

Example:
```
id,word,explanation
a1,apple,An edible fruit
a2,python,A popular programming language
```

### 5. Run the program
```bash
python main.py
```

## Usage
- At startup, select a word list using the dropdown (or use the default selection).
- Type the correct word and press Enter to check your answer.
- If correct, rate your memory of the word by pressing 1/2/3/4 (corresponding to again, hard, good, easy; press Enter for default 3=good). The system will intelligently schedule the next review based on the FSRS algorithm.
- Press `Ctrl+E` to show/hide the explanation.
- Press `Ctrl+B` to start the quiz.
- Press `Ctrl+S` to skip the current word.
- Press `Ctrl+K` to quit and save progress.

## TODO
- [ ] fix bug when rating with Input Method
- [x] skip then rate
- [x] refactor to separate ui and core logic
- [x] Update words from app and textbook daily
- [x] supply more explanations

## License
MIT
