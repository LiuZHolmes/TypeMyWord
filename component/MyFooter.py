from textual.widgets import Static, Input, Button, Select, Header, Footer, ProgressBar, Label


class MyFooter(Footer):
    def __init__(self):
        super().__init__()
        self.status = Label("FOO")
        self.show_command_palette = False
        self.status.styles.dock = "right"
        self.styles.grid_size_columns = 5

    def compose(self):
        yield from super().compose()
        return self.status
