
import datetime
from fsrs_rs_python import DEFAULT_PARAMETERS, FSRS, MemoryState, NextStates
from service.service import normalize_input
from service.words_loader import Word

desired_retention = 0.9
fsrs = FSRS(parameters=DEFAULT_PARAMETERS)


def get_next_states(word: Word) -> NextStates:
    elapsed_days = 0
    if word.last_review is not None:
        elapsed_days = (datetime.datetime.now(
            datetime.timezone.utc) - word.last_review).days
    next_states = fsrs.next_states(
        word.memory_state, desired_retention, elapsed_days)
    return next_states
    """根据当前单词的记忆状态获取下一个状态"""
    if word.memory_state is None:
        return fsrs.next_states(MemoryState(0, 0), desired_retention, 0)
    elapsed_days = 0
    if word.last_review is not None:
        elapsed_days = (datetime.datetime.now(
            datetime.timezone.utc) - word.last_review).days
    return fsrs.next_states(word.memory_state, desired_retention, elapsed_days)


def update_word_state(word: Word, next_states: NextStates, rating: str):
    rating_map = {"1": "again", "2": "hard", "3": "good", "4": "easy"}
    rating = normalize_input(rating)
    if rating not in rating_map:
        rating = "3"  # default good
    rating_key = rating_map[rating]
    next_state = getattr(next_states, rating_key)
    interval = int(max(1, round(next_state.interval)))
    word.memory_state = next_state.memory
    word.scheduled_days = interval
    word.last_review = datetime.datetime.now(
        datetime.timezone.utc)
    word.due = word.last_review + \
        datetime.timedelta(days=interval)
