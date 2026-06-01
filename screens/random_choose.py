from kivy.uix.screenmanager import Screen
from kivy.app import App
from utils import get_random_item_by_category


class RandomChooseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "random"
        self.current_item = None
        self.bind(on_enter=self.on_screen_enter)

    def on_screen_enter(self, *args):
        """Wird aufgerufen, wenn der Screen angezeigt wird"""
        app = App.get_running_app()
        app.refresh_categories()
        self.ids.random_spinner.values = app.categories + ["Zufällig"]
        self.ids.random_spinner.text = "Zufällig"
        self.ids.result_label.text = ""
        self.current_item = None

    def choose_random_topic(self):
        app = App.get_running_app()
        selected_category = self.ids.random_spinner.text
        self.current_item = get_random_item_by_category(app.data, selected_category)
        if self.current_item:
            category_text = ", ".join(self.current_item["category"])
            self.ids.result_label.text = (
                f"Kategorie: {category_text}\nThema: {self.current_item['topic']}"
            )
        else:
            self.ids.result_label.text = "Keine verfügbaren Themen."


