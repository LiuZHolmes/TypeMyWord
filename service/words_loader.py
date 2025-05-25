import datetime
import os
import csv
from typing import Optional
from fsrs_rs_python import DEFAULT_PARAMETERS, FSRS, MemoryState

fsrs = FSRS(parameters=DEFAULT_PARAMETERS)

class Word:
    def __init__(self, id, word, explanation, 
                 due: Optional[datetime.datetime] = None, 
                 memory_state: Optional[MemoryState] = None,
                 scheduled_days: int = 0,
                 last_review: Optional[datetime.date] = None):
        self.id = id
        self.word = word
        self.explanation = explanation
        if due is None:
            self.due = datetime.datetime.now(datetime.timezone.utc)
            self.memory_state: Optional[MemoryState] = None
            self.scheduled_days = 0
            self.last_review: Optional[datetime.date] = None

def load_words_from_csv(selected_csv: str) -> list[Word]:
    words_dir = os.path.join(os.path.dirname(__file__), '../words')
    csv_path = os.path.join(words_dir, selected_csv)
    words = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for _idx, row in enumerate(reader):
            words.append(Word(row[0], row[1], row[2]))
    return words

def load_words(selected_csv: str) -> list[Word]:
    words = load_words_from_csv(selected_csv)
    now = datetime.datetime.now(datetime.timezone.utc)
    words = [word for word in words if word.due is None or word.due <= now]
    return words

def save_words_to_csv(selected_csv: str, words: list[Word]):
    words_dir = os.path.join(os.path.dirname(__file__), '../words')
    csv_path = os.path.join(words_dir, selected_csv)
    # 读取原始csv所有行
    with open(csv_path, encoding='utf-8') as f:
        reader = list(csv.reader(f))
    header = reader[0]
    rows = reader[1:]
    # 构建id到Word的映射
    word_map = {str(w.id): w for w in words}
    # 检查header，自动扩展字段
    field_names = header.copy()
    for extra in ["due", "memory_state", "scheduled_days", "last_review"]:
        if extra not in field_names:
            field_names.append(extra)
    # 更新行
    new_rows = []
    for row in rows:
        word_id = str(row[0])
        if word_id in word_map:
            w = word_map[word_id]
            # 保留原有字段，更新指定字段
            row_dict = dict(zip(header, row))
            row_dict["due"] = w.due.isoformat() if hasattr(w, "due") and w.due else ""
            row_dict["memory_state"] = str(w.memory_state) if hasattr(w, "memory_state") and w.memory_state else ""
            row_dict["scheduled_days"] = str(w.scheduled_days) if hasattr(w, "scheduled_days") else ""
            row_dict["last_review"] = w.last_review.isoformat() if hasattr(w, "last_review") and w.last_review else ""
            # 按field_names顺序输出
            new_row = [row_dict.get(col, "") for col in field_names]
            new_rows.append(new_row)
        else:
            # 旧行补全新字段
            row_dict = dict(zip(header, row))
            for extra in ["due", "memory_state", "scheduled_days", "last_review"]:
                if extra not in row_dict:
                    row_dict[extra] = ""
            new_row = [row_dict.get(col, "") for col in field_names]
            new_rows.append(new_row)
    # 写回csv
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(field_names)
        writer.writerows(new_rows)
