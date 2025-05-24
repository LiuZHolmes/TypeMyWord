# TypeMyWord

TypeMyWord is a command-line tool for practicing word spelling. It reads a CSV file containing words and their explanations, then quizzes you by asking you to type each word correctly. You can reveal the explanation for each word if needed.

## Features
- Scan the `words/` directory for available word lists (CSV files)
- Randomly quiz you on the words in the selected file
- Show explanations on demand (press `?`)
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
- Each CSV should have two columns: `word,explanation` (no header required).

Example:
```
apple,An edible fruit
python,A popular programming language
```

### 5. Run the program
```bash
python main.py
```

## Usage
- At startup, select a word list by number (or press Enter to use the first one).
- Type the correct word to continue.
- Type `?` to show the explanation for the current word.
- Type `exit` to quit the program.

## License
MIT
