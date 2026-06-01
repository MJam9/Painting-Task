import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import platform as kivy_platform
from kivy.metrics import dp
from kivy.lang import Builder

from screens import (
    MainMenuScreen,
    AddTopicScreen,
    RandomChooseScreen,
    CategoryAssignmentScreen,
)
from utils import load_json, get_file_path, get_categories

# Lade die .kv Datei
kv_path = os.path.join(os.path.dirname(__file__), "main.kv")
Builder.load_file(kv_path)


class PaintingTaskApp(App):
    def build(self):
        # Fenster-Konfiguration: feste Desktop-Größe entfernt.
        # Auf Mobilgeräten nutzt Kivy automatisch die Displaygröße
        # und Layouts sollten sich über `size_hint` anpassen.
        # Wenn während der Entwicklung eine feste Fenstergröße gewünscht
        # ist, kann man eine Plattformabfrage verwenden und nur dann setzen.
        # Beispiel (auskommentiert):
        # if kivy_platform not in ("android", "ios"):
        #     Window.size = (400, 600)
        
        self.file_path = get_file_path()
        self.data = load_json(self.file_path)
        self.categories = get_categories(self.data)

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(MainMenuScreen())
        self.screen_manager.add_widget(AddTopicScreen())
        self.screen_manager.add_widget(RandomChooseScreen())
        self.screen_manager.add_widget(CategoryAssignmentScreen())

        return self.screen_manager

    def show_popup(self, title, message):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=message, halign="center", valign="middle"))
        close_button = Button(text="Schließen", size_hint_y=None, height=dp(40))
        content.add_widget(close_button)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name

    def refresh_categories(self):
        self.data = load_json(self.file_path)
        self.categories = get_categories(self.data)


if __name__ == "__main__":
    PaintingTaskApp().run()
