import datetime
import os
import csv
import json
import re
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
        if memory_state is None:
            self.due = datetime.datetime.now(datetime.timezone.utc)
            self.memory_state: Optional[MemoryState] = None
            self.scheduled_days = 0
            self.last_review: Optional[datetime.date] = None
        else:
            self.due = due
            self.memory_state = memory_state
            self.scheduled_days = scheduled_days
            self.last_review = last_review
            

def load_words_from_csv(selected_csv: str) -> list[Word]:
    words_dir = os.path.join(os.path.dirname(__file__), '../words')
    csv_path = os.path.join(words_dir, selected_csv)
    words = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 读取表头
        col_idx = {k: i for i, k in enumerate(header)}
        for row in reader:
            id = row[col_idx.get('id', 0)]
            word = row[col_idx.get('word', 1)]
            explanation = row[col_idx.get('explanation', 2)]
            due = None
            memory_state = None
            scheduled_days = 0
            last_review = None
            if 'due' in col_idx and row[col_idx['due']]:
                try:
                    due = datetime.datetime.fromisoformat(row[col_idx['due']])
                except Exception:
                    due = None
            # memory_state反序列化json
            if 'memory_state' in col_idx and row[col_idx['memory_state']]:
                try:
                    ms = json.loads(row[col_idx['memory_state']])
                    memory_state = MemoryState(ms["stability"], ms["difficulty"])
                except Exception:
                    memory_state = None
            if 'scheduled_days' in col_idx and row[col_idx['scheduled_days']]:
                try:
                    scheduled_days = int(row[col_idx['scheduled_days']])
                except Exception:
                    scheduled_days = 0
            if 'last_review' in col_idx and row[col_idx['last_review']]:
                try:
                    last_review = datetime.datetime.fromisoformat(row[col_idx['last_review']])
                except Exception:
                    last_review = None
            words.append(Word(id, word, explanation, due, memory_state, scheduled_days, last_review))
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
            # memory_state序列化为json
            if hasattr(w, "memory_state") and w.memory_state:
                s = str(w.memory_state)
                # 用正则提取值
                match = re.search(r"stability: ([\d.]+), difficulty: ([\d.]+)", s)
                if match:
                    stability = float(match.group(1))
                    difficulty = float(match.group(2))
                    row_dict["memory_state"] = json.dumps({
                        "stability": stability,
                        "difficulty": difficulty
                    })

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
