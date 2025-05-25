import os
import csv

# 读取单词和解释
def load_words(selected_csv):
    words_dir = os.path.join(os.path.dirname(__file__), '../words')
    csv_path = os.path.join(words_dir, selected_csv)
    words = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            if len(row) >= 2:
                words.append({'word': row[0], 'explanation': row[1]})
    return words