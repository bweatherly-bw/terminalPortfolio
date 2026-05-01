from __future__ import annotations
from typing import Iterable

from textual.app import App, ComposeResult, on
from textual.binding import Binding
from textual.containers import VerticalScroll, Center, Middle
from textual.screen import Screen
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    Label,
    ListView,
    ListItem,
    Markdown,
)


class HomeScreen(Screen):
    """Welcome / landing screen"""

    def compose(self) -> ComposeResult:
        yield Static(
            """
[bold #0f0]Welcome to Brandon's Portfolio[/]

Austin, TX • Terminal enthusiast • Builder of cool stuff in Python and JS. 

Press [b]P[/b] to see projects
     [b]A[/b] for about
     [b]Q[/b] or Ctrl+C to quit
""",
            id="welcome",
            markup=True,
        )

        with Center():
            with Middle():
                yield Button("View Projects", id="to-projects", variant="primary")


class ProjectDetail(Screen):
    """Shows one project"""

    def __init__(self, title: str, description: str, url: str | None = None):
        super().__init__()
        self.project_title = title
        self.description = description
        self.url = url

    def compose(self) -> ComposeResult:
        yield Label(f"[bold]{self.project_title}[/]", id="project-title")
        yield Markdown(self.description)

        if self.url:
            yield Button.open_link(
                self.url,
                label=f"Visit → {self.url.split('//')[-1]}",
                id="visit-url",
                variant="success",
            )

        yield Button("Back", id="back", variant="error")

    @on(Button.Pressed, "#back")
    def go_back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#visit-url")
    def open_link(self):
        # Textual will try to open in browser (works in many terminals)
        # Falls back gracefully if not supported
        pass  # Button.open_link already handles it


class ProjectsScreen(Screen):
    """List of your projects"""

    def compose(self) -> ComposeResult:
        yield Label("[bold]Selected Projects[/]", classes="section-title")

        with ListView():
            yield ListItem(
                Label("terminal-cv • 2025"),
                classes="project-item",
                data={
                    "title": "terminal-cv",
                    "desc": """
A self-updating terminal resume / portfolio.
Built with **Textual** + GitHub Actions.
Shows real-time commit activity, tech stack, and ASCII art flair.
                    """,
                    "url": "https://github.com/yourusername/terminal-cv",
                },
            )

            yield ListItem(
                Label("ssh-roguelike • 2026"),
                classes="project-item",
                data={
                    "title": "SSH Roguelike",
                    "desc": """
Multi-user dungeon crawler over SSH.
Persistent world, turn-based combat, ASCII procedurally generated maps.
                    """,
                    "url": None,
                },
            )

            # Add more ListItems here...

        yield Button("Back to Home", id="back-home")

    @on(ListView.Selected)
    def show_detail(self, event: ListView.Selected):
        item = event.item
        data = item.data
        if data:
            self.app.push_screen(
                ProjectDetail(
                    title=data["title"],
                    description=data["desc"],
                    url=data.get("url"),
                )
            )

    @on(Button.Pressed, "#back-home")
    def go_home(self):
        self.app.pop_screen()


class AboutScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Markdown(
            """
# About Brandon

- Based in **Austin, Texas**
- I enjoy: Cyber Security, Software Development, Game Development, Open Source, and Terminal Tools
- Currently exploring: terminal-based tools, SSH experiences, minimalism in UX
- Find my full work → https://brandon.example.com
- GitHub: @bw-bweatherly

Built this terminal experience with **Textual** — because why not make a portfolio you ssh into?
            """
        )
        yield Button("Back", id="back")

    @on(Button.Pressed, "#back")
    def go_back(self):
        self.app.pop_screen()


class PortfolioApp(App):
    """Brandon's Terminal Portfolio"""

    CSS = """
    Screen {
        background: $surface;
    }

    #welcome {
        height: auto;
        margin: 2;
        padding: 1 2;
        border: tall #0f0;
        background: $panel;
        text-align: center;
    }

    .section-title {
        margin: 1 0;
        text-align: center;
        text-style: bold;
        color: $accent;
    }

    .project-item {
        height: auto;
        padding: 1;
        margin: 1 0;
        border: tall $primary;
        background: $boost;
    }

    ListView > ListItem:focus {
        background: $secondary;
    }

    Button {
        margin: 1 2;
    }
    """

    BINDINGS = [
        Binding("p", "push_screen('projects')", "Projects", show=True),
        Binding("a", "push_screen('about')", "About", show=True),
        Binding("d", "toggle_dark", "Toggle Dark", show=True),
        Binding("q", "app.quit", "Quit", show=True),
    ]

    SCREENS = {
        "home": HomeScreen,
        "projects": ProjectsScreen,
        "about": AboutScreen,
    }

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen("home")
        self.dark = True  # Start in dark mode (looks cooler in terminal)

    def action_push_screen(self, screen: str) -> None:
        self.push_screen(screen)


if __name__ == "__main__":
    app = PortfolioApp()
    app.run()