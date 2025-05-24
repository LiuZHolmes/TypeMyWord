import csv
import random
import sys
import os

# 读取单词和解释
def load_words(csv_path):
    words = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            if len(row) >= 2:
                words.append({'word': row[0], 'explanation': row[1]})
    return words

def choose_csv_file():
    words_dir = os.path.join(os.path.dirname(__file__), 'words')
    if not os.path.exists(words_dir):
        print('No words/ directory found.')
        sys.exit(1)
    csv_files = [f for f in os.listdir(words_dir) if f.endswith('.csv')]
    if not csv_files:
        print('No CSV files found in words/.')
        sys.exit(1)
    print('Available word CSV files:')
    for idx, fname in enumerate(csv_files, 1):
        print(f'{idx}. {fname}')
    choice = input(f'Select a file by number (default 1): ').strip()
    if not choice:
        choice = '1'
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(csv_files):
            raise ValueError
    except ValueError:
        print('Invalid selection.')
        sys.exit(1)
    return os.path.join(words_dir, csv_files[idx])

def main():
    csv_path = choose_csv_file()
    words = load_words(csv_path)
    random.shuffle(words)
    print('TypeMyWord - Type the correct word to continue. Type ? to show explanation, type exit to quit.')
    show_explanation = False
    while words:
        entry = words.pop()
        while True:
            print(f"Word: {entry['word']}")
            if show_explanation:
                print(f"Explanation: {entry['explanation']}")
            user_input = input('Please type the word (type ? to always show/hide explanation, exit to quit): ').strip()
            if user_input == 'exit':
                print('Exited.')
                sys.exit(0)
            if user_input == '?':
                show_explanation = not show_explanation
                print(f"Always show explanation: {'ON' if show_explanation else 'OFF'}")
                continue
            if user_input == entry['word']:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Correct!\n')
                break
            else:
                print('Incorrect, please try again.')

if __name__ == '__main__':
    main()
