from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.app import App
from utils import save_json, get_file_path


class CategoryAssignmentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "assign"
        self.current_topic = None
        self.bind(on_pre_enter=self.refresh_screen)

    def refresh_screen(self, *args):
        """Wird aufgerufen, wenn der Screen angezeigt wird"""
        app = App.get_running_app()
        app.refresh_categories()
        
        # Spinner mit allen Topic-Namen füllen
        topic_names = [item["topic"] for item in app.data]
        self.ids.topic_spinner.values = topic_names
        self.ids.topic_spinner.text = "Wähle ein Thema"
        
        # Container leeren
        self.ids.category_container.clear_widgets()
        self.current_topic = None
        # Hide delete button until a topic is selected
        if 'delete_button' in self.ids:
            self.ids.delete_button.disabled = True
            self.ids.delete_button.opacity = 0

    def on_topic_selected(self, topic_name):
        """Wird aufgerufen, wenn ein Thema aus dem Spinner ausgewählt wird"""
        if topic_name == "Wähle ein Thema":
            self.ids.category_container.clear_widgets()
            self.current_topic = None
            return
        
        app = App.get_running_app()
        
        # Finde das ausgewählte Thema
        self.current_topic = next((item for item in app.data if item["topic"] == topic_name), None)
        
        if not self.current_topic:
            # Ensure delete button hidden
            if 'delete_button' in self.ids:
                self.ids.delete_button.disabled = True
                self.ids.delete_button.opacity = 0
            return
        
        # Kategorien anzeigen
        self.ids.category_container.clear_widgets()
        
        for category in app.categories:
            line = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(45))
            checkbox = CheckBox(
                active=category in self.current_topic["category"],
                size_hint=(None, 1),
                width=dp(40),
            )
            checkbox.bind(active=self.make_checkbox_callback(category))
            line.add_widget(checkbox)
            line.add_widget(Label(text=category, halign="left", valign="middle", size_hint_x=0.85))
            self.ids.category_container.add_widget(line)
        # Show delete button when a topic is selected
        if 'delete_button' in self.ids:
            self.ids.delete_button.disabled = False
            self.ids.delete_button.opacity = 1

    def delete_current_topic(self):
        if not self.current_topic:
            return

        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Soll '{self.current_topic['topic']}' wirklich gelöscht werden?"))

        btn_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        confirm = Button(text='Löschen', background_color=(0.8,0.2,0.2,1), color=(1,1,1,1))
        cancel = Button(text='Abbrechen')
        btn_layout.add_widget(cancel)
        btn_layout.add_widget(confirm)
        content.add_widget(btn_layout)

        popup = Popup(title='Eintrag löschen', content=content, size_hint=(0.8, 0.4))

        def do_delete(instance):
            app = App.get_running_app()
            try:
                app.data.remove(self.current_topic)
            except ValueError:
                pass
            save_json(get_file_path(), app.data)
            popup.dismiss()
            # Refresh spinner and container
            self.refresh_screen()

        confirm.bind(on_release=do_delete)
        cancel.bind(on_release=popup.dismiss)
        popup.open()

    def make_checkbox_callback(self, category):
        def callback(checkbox, value):
            if not self.current_topic:
                return
            
            if value and category not in self.current_topic["category"]:
                self.current_topic["category"].append(category)
            elif not value and category in self.current_topic["category"]:
                self.current_topic["category"].remove(category)
            
            save_json(get_file_path(), App.get_running_app().data)

        return callback
