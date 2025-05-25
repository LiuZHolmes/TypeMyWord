import os
import csv

class Word:
    def __init__(self, id, word, explanation):
        self.id = id
        self.word = word
        self.explanation = explanation

# 读取单词和解释
def load_words(selected_csv: str) -> list[Word]:
    words_dir = os.path.join(os.path.dirname(__file__), '../words')
    csv_path = os.path.join(words_dir, selected_csv)
    words = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for _idx, row in enumerate(reader):
            words.append(Word(row[0], row[1], row[2]))
    return words