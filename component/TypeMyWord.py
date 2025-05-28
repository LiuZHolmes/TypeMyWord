import random
import os
from fsrs_rs_python import DEFAULT_PARAMETERS, FSRS
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input, Footer
from textual.binding import Binding
from service import words_loader
from service.scheduler import get_next_states, update_word_state

desired_retention = 0.9
fsrs = FSRS(parameters=DEFAULT_PARAMETERS)


class TypeMyWord(App):
    CSS_PATH = None
    BINDINGS = [
        Binding("ctrl+k", "quit", "Quit", priority=True),
        Binding("ctrl+e", "toggle_explanation",
                "Show/Hide Explanation", priority=True),
        Binding("ctrl+s", "skip_word", "Skip Word", priority=True),
    ]

    def __init__(self, selected_csv=None, **kwargs):
        super().__init__(**kwargs)
        self.words = []
        self.current = None
        self.show_explanation = False
        self.word_idx = 0
        self.selected_csv = selected_csv  # Pass the selected CSV file directly

    def compose(self) -> ComposeResult:
        self.input = Input(id="input", compact=True)
        yield self.input

    async def on_mount(self) -> None:
        # Load words from the selected CSV file
        if not self.selected_csv:
            self.exit("No CSV file provided.")
            return
        self.words = words_loader.load_words(selected_csv=self.selected_csv)
        if not self.words:
            self.exit(f"No words found in {self.selected_csv}.")
            return
        random.shuffle(self.words)
        self.word_idx = 0
        self.input.value = ""
        self.input.visible = True
        await self.show_word()

    async def show_word(self):
        if self.word_idx >= len(self.words):
            self.input.placeholder = "Done"
            self.input.disabled = True
            return
        self.current = self.words[self.word_idx]
        word_text = self.current.word
        explanation_text = f": {self.current.explanation}" if self.show_explanation else ""
        self.input.placeholder = (f"{word_text}{explanation_text}")
        self.input.value = ""
        self.input.focus()

    async def on_input_submitted(self, event):
        if not self.current:
            return
        value = event.value.strip()
        if value == self.current.word:
            await self.pass_word()
            return
        # 评价分支
        if hasattr(self, 'input_submitted_for_rating') and self.input_submitted_for_rating:
            next_states = get_next_states(self.current)
            update_word_state(self.current, next_states, value)
            self.word_idx += 1
            self.input_submitted_for_rating = False
            await self.show_word()
            return
        else:
            self.input.placeholder = ""
            self.input.value = ""
            self.input.focus()

    async def action_toggle_explanation(self):
        self.show_explanation = not self.show_explanation
        await self.show_word()

    async def action_skip_word(self):
        await self.pass_word()

    async def action_quit(self):
        # 退出时保存数据
        if self.selected_csv and self.words:
            words_loader.save_words_to_csv(self.selected_csv, self.words)
        self.exit()

    async def pass_word(self):
        self.input.placeholder = "✔ Rate with 1:again 2:hard 3:good(default) 4:easy"
        self.input.value = ""
        self.input.focus()
        self.input_submitted_for_rating = True
