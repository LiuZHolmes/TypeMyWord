# 用 prompt_toolkit 实现简洁命令行交互版 TypeMyWord
import os
import random
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import clear
from service import words_loader
from service.scheduler import get_next_states, update_word_state


def list_csv_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".csv")]


def select_csv(words_dir):
    csv_files = list_csv_files(words_dir)
    if not csv_files:
        print(f"No CSV files found in '{words_dir}'.")
        return None
    if len(csv_files) == 1:
        print(f"Selected: {csv_files[0]}")
        return os.path.join(words_dir, csv_files[0])
    print("CSV files:")
    for idx, file in enumerate(csv_files, start=1):
        print(f"{idx}. {file}")
    while True:
        choice = input("Choose file #: ")
        if choice.isdigit() and 1 <= int(choice) <= len(csv_files):
            return os.path.join(words_dir, csv_files[int(choice) - 1])
        print("Invalid. Try again.")


def main():
    words_dir = os.path.join(os.getcwd(), "words")
    if not os.path.exists(words_dir):
        print(f"Directory '{words_dir}' not found.")
        return
    selected_csv = select_csv(words_dir)
    if not selected_csv:
        return
    words = words_loader.load_words(selected_csv=selected_csv)
    if not words:
        print(f"No words in {selected_csv}.")
        return
    random.shuffle(words)
    word_idx = 0
    session = PromptSession()  # 使用 PromptSession 实现动态交互
    while word_idx < len(words):
        clear()
        current = words[word_idx]
        word_text = current.word
        explanation_text = f"{current.explanation}"
        rate_placeholder = "Rate: 1 (again), 2 (hard), 3 (good, default), 4 (easy)"

        # 使用 placeholder 显示当前单词
        user_input = session.prompt(
            "> ",
            default="",
            placeholder=word_text,  # 将单词作为 placeholder 显示
        ).strip()

        if user_input.lower() in ("quit", "q"):
            break
        if user_input.lower() == "skip":
            word_idx += 1
            continue
        if user_input == word_text:
            # 显示释义和评分说明
            rating = session.prompt(
                "> ",
                default="",
                # 显示释义和评分说明
                placeholder=f"{explanation_text}. {rate_placeholder}",
            ).strip()
            next_states = get_next_states(current)
            update_word_state(current, next_states, rating)
            word_idx += 1
        else:
            continue
    words_loader.save_words_to_csv(selected_csv, words)
    clear()


if __name__ == "__main__":
    main()
