import random
import os
from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button, Select, Header, Footer, ProgressBar
from textual.binding import Binding
from service import words_loader

class TypeMyWord(App):
    CSS_PATH = None
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+b", "click_start", show=False),
        Binding("ctrl+e", "toggle_explanation", "Show/Hide Explanation", priority=True),
        Binding("ctrl+k", "skip_word", "Skip Word", priority=True),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.words = []
        self.current = None
        self.show_explanation = False
        self.word_idx = 0
        self.csv_files = []
        self.selected_csv = None

    def compose(self) -> ComposeResult:
        yield Header()
        self.select = Select(options=[], prompt="Select a word list:")
        yield self.select
        self.start_btn = Button("Start", id="start_btn")
        yield self.start_btn
        self.progress = ProgressBar(total=1, id="progress", show_eta=False)
        yield self.progress
        self.word_display = Static("", id="word")
        yield self.word_display
        self.explanation_display = Static("", id="explanation")
        yield self.explanation_display
        self.input = Input(id="input")
        yield self.input
        self.status = Static("", id="status")
        yield self.status
        yield Footer()

    async def on_mount(self) -> None:
        # Scan for CSV files
        words_dir = os.path.join(os.path.dirname(__file__), '../words')
        self.csv_files = [f for f in os.listdir(words_dir) if f.endswith('.csv')]
        if not self.csv_files:
            self.status.update("No CSV files found in words/ directory.")
            return
        self.select.set_options([(f, f) for f in self.csv_files])
        self.select.value = self.csv_files[0]
        self.input.visible = False
        self.word_display.visible = False
        self.explanation_display.visible = False
        self.progress.visible = False

    async def on_button_pressed(self, event):
        if event.button.id == "start_btn":
            self.selected_csv = self.select.value
            self.progress.visible = True
            await self.start()

    async def start(self):
        self.words = words_loader.load_words(selected_csv=self.selected_csv)
        random.shuffle(self.words)
        self.word_idx = 0
        self.show_explanation = False
        self.input.value = ""
        self.input.visible = True
        self.word_display.visible = True
        self.explanation_display.visible = False
        self.status.update("")
        self.select.visible = False
        self.start_btn.visible = False
        self.progress.update(total=len(self.words), progress=0)
        await self.show_word()

    async def show_word(self):
        if self.word_idx >= len(self.words):
            self.progress.update(progress=len(self.words))
            self.word_display.update("Finished!")
            self.explanation_display.update("")
            self.input.visible = False
            return
        self.current = self.words[self.word_idx]
        self.progress.update(progress=self.word_idx+1)
        self.word_display.update(f"Word: {self.current.word}")
        self.explanation_display.update(f"Explanation: {self.current.explanation}")
        self.explanation_display.visible = self.show_explanation
        self.input.value = ""
        self.input.focus()

    async def on_input_submitted(self, event):
        if not self.current:
            return
        value = event.value.strip()
        if value == self.current.word:
            self.word_idx += 1
            self.status.update("")
            await self.show_word()
        else:
            self.status.update("")
            self.input.value = ""
            self.input.focus()

    async def action_toggle_explanation(self):
        self.show_explanation = not self.show_explanation
        await self.show_word()

    async def action_click_start(self):
        self.start_btn.press()

    async def action_skip_word(self):
        """Skip the current word and move to the next one."""
        if self.word_idx < len(self.words):
            self.word_idx += 1
            await self.show_word()