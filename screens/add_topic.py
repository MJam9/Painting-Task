from kivy.uix.screenmanager import Screen
from kivy.app import App
from utils import save_json, get_file_path


class AddTopicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "add"
        self.bind(on_enter=self.on_screen_enter)

    def on_screen_enter(self, *args):
        """Wird aufgerufen, wenn der Screen angezeigt wird"""
        app = App.get_running_app()
        app.refresh_categories()
        
        # Aktualisiere die Spinner-Werte
        self.ids.category_spinner.values = app.categories + ["Neue Kategorie"]
        self.ids.category_spinner.text = "Wähle eine Kategorie"
        
        # Leere die Input-Felder
        self.ids.topic_input.text = ""
        self.ids.new_category_input.text = ""
        self.ids.new_category_input.height = 0
        self.ids.new_category_input.opacity = 0
        self.ids.new_category_input.disabled = True

    def on_category_choice(self, spinner, text):
        if text == "Neue Kategorie":
            self.ids.new_category_input.height = 40
            self.ids.new_category_input.opacity = 1
            self.ids.new_category_input.disabled = False
        else:
            self.ids.new_category_input.height = 0
            self.ids.new_category_input.opacity = 0
            self.ids.new_category_input.disabled = True
            self.ids.new_category_input.text = ""

    def add_topic(self):
        app = App.get_running_app()
        new_topic = self.ids.topic_input.text.strip()
        
        if not new_topic:
            app.show_popup("Fehler", "Bitte gib ein Thema ein.")
            return

        selected_category = self.ids.category_spinner.text
        if selected_category == "Wähle eine Kategorie":
            app.show_popup("Fehler", "Bitte wähle eine Kategorie.")
            return

        if selected_category == "Neue Kategorie":
            new_category = self.ids.new_category_input.text.strip()
            if not new_category or new_category in app.categories:
                app.show_popup("Fehler", "Ungültige oder bereits existierende Kategorie.")
                return
            app.categories.append(new_category)
            selected_category = new_category

        app.data.append(
            {"topic": new_topic, "category": [selected_category]}
        )
        save_json(get_file_path(), app.data)
        app.refresh_categories()
        app.show_popup("Erfolg", f"'{new_topic}' wurde zu '{selected_category}' hinzugefügt.")
        app.switch_screen("main")
