import random
import os
from fsrs_rs_python import DEFAULT_PARAMETERS, FSRS
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input, Button, Select, Header, Footer, ProgressBar, Label
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
        with Vertical(id="main_container", classes="container"):
            self.word_display = Static("", id="word")
            yield self.word_display
            self.explanation_display = Static("", id="explanation")
            yield self.explanation_display
            self.input = Input(id="input", compact=True,)
            yield self.input
            self.status = Static("", id="status")
            yield self.status
        with Footer():
            yield Label("TypeMyWord")

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
        self.word_display.visible = True
        self.explanation_display.visible = self.show_explanation
        await self.show_word()

    async def show_word(self):
        if self.word_idx >= len(self.words):
            self.word_display.update("Done")
            self.explanation_display.update("")
            self.input.visible = False
            return
        self.current = self.words[self.word_idx]
        self.word_display.update(f"Word: {self.current.word}")
        self.explanation_display.update(
            f"Explanation: {self.current.explanation}")
        self.explanation_display.visible = self.show_explanation
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
            self.status.update("")
            self.input_submitted_for_rating = False
            self.input.placeholder = ""
            self.explanation_display.visible = self.show_explanation
            await self.show_word()
            return
        else:
            self.status.update("")
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
        self.word_display.update(f"Word: {self.current.word} ✔")
        self.status.update(
            "Rate with 1:again 2:hard 3:good(default) 4:easy")
        self.input.value = ""
        self.input.focus()
        self.input_submitted_for_rating = True
        self.explanation_display.visible = True
