from database_manager import UserData, ImageData, RecipeData, SessionManager
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image, Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
import os
import shutil


class RecipeDialog(ModalView):
    def __init__(self, session_manager, **kwargs):
        super().__init__(**kwargs)
        self.session_manager = session_manager
        self.image_path = None
        self.recipe_rating = None
        self.size_hint = (0.95, 0.95)
        self.box_layout = BoxLayout(orientation='vertical')
        self.recipe_name = TextInput(
            background_color=(0, 0, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            halign='center',
            hint_text='Name',
            multiline=False,
            pos_hint={'center_x': 0.5},
            size_hint=(1, 0.1)
        )
        self.box_layout.add_widget(self.recipe_name)
        self.box_layout.add_widget(
            Button(background_color='#145DA0', on_press=self.choose_recipe_picture, size_hint=(1, 0.09),
                   text='Upload Recipe Picture'))
        self.image_label = AsyncImage(source='', size_hint=(1, 0.6))
        self.box_layout.add_widget(self.image_label)
        self.image_description = TextInput(
            hint_text='Description',
            multiline=True,
            pos_hint={'center_x': 0.5},
            size_hint=(1, 0.1)
        )
        self.box_layout.add_widget(self.image_description)
        self.recipe_instructions = TextInput(
            hint_text='Instructions',
            multiline=True,
            pos_hint={'center_x': 0.5},
            size_hint=(1, 0.5)
        )
        self.box_layout.add_widget(self.recipe_instructions)
        rating_layout = BoxLayout(pos_hint={'center_x': 0.5}, size_hint=(0.35, 0.14), spacing=10)
        for i in range(1, 6):
            rating_button = ToggleButton(
                bold=True,
                background_down='images/star/gg-star.png',
                background_normal='images/star/gg-star-down.png',
                color='white',
                group='rating',
                on_press=self.set_rating,
                text=str(i)
            )
            rating_layout.add_widget(rating_button)
        self.box_layout.add_widget(rating_layout)
        bottom_buttons_layout = BoxLayout(size_hint=(1, 0.05))
        bottom_buttons_layout.add_widget(
            Button(background_color='#145DA0', on_press=self.submit_data,
                   size_hint=(0.5, 1.15), text='Submit'))
        bottom_buttons_layout.add_widget(
            Button(background_color='#145DA0', on_press=self.dismiss,
                   size_hint=(0.5, 1.15), text='Close'))
        self.box_layout.add_widget(bottom_buttons_layout)
        self.add_widget(self.box_layout)

    @staticmethod
    def show_error_notification(message):
        content = Label(text=message)
        popup = Popup(title='Error', content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def save_image_to_folder(self):
        if self.image_path:
            destination_folder = "images"
            filename = os.path.basename(self.image_path)
            destination = os.path.join(destination_folder, filename)
            counter = 1
            while os.path.exists(destination):
                base, ext = os.path.splitext(filename)
                filename = f"{base}_{counter}{ext}"
                destination = os.path.join(destination_folder, filename)
                counter += 1
            try:
                shutil.copy(self.image_path, destination)
                self.image_path = destination
                print(f'Saved Image to: {destination}')
                return filename
            except Exception as e:
                print(f'Error saving image: {e}')
                self.show_error_notification("Error saving image")

    def file_selected(self, chooser, selected, touch=None):
        if selected:
            self.image_path = selected[0]
            self.image_label.source = self.image_path

    def choose_recipe_picture(self, instance):
        file_chooser = FileChooserIconView(on_submit=self.file_selected, path='.')
        popup = Popup(content=file_chooser, size_hint=(0.9, 0.9), title='Select an Image')
        popup.open()

    def show_image(self, instance):
        if self.image_path:
            image_source = f'images/{os.path.basename(self.image_path)}'
            image_widget = KivyImage(source=image_source, size_hint=(1, 1))
            self.box_layout.add_widget(image_widget)

    def set_rating(self, instance):
        self.recipe_rating = int(instance.text)
        print(f'Rating set to: {self.recipe_rating}')

    def submit_data(self, instance):
        if not self.recipe_name.text:
            self.show_error_notification("No recipe name is entered, try again")
            return
        try:
            image_description = self.image_description.text or None
            recipe_instructions = self.recipe_instructions.text or None
            session = self.session_manager.create_session()
            existing_recipe = session.query(RecipeData).filter_by(recipe_name=self.recipe_name.text).first()
            if existing_recipe:
                message = f"Recipe with the name\n'{self.recipe_name.text}'already exists,\nchoose a different name"
                print(message)
                self.show_error_notification(message)
                session.close()
                return
            self.save_image_to_folder()
            new_image = ImageData(
                image_id=session.query(ImageData).count() + 1,
                image_path=self.image_path,
                image_description=image_description
            )
            session.add(new_image)
            new_recipe = RecipeData(
                recipe_name=self.recipe_name.text,
                image_path=self.image_path,
                image_description=image_description,
                recipe_instructions=recipe_instructions,
                recipe_rating=self.recipe_rating
            )
            session.add(new_recipe)
            session.commit()
            session.close()
            print("Data submitted")
            main_screen = App.get_running_app().root.get_screen('main_screen')
            main_screen.update_scroll_view()
            self.dismiss()
        except Exception as e:
            print(f'Error submitting data: {e}')
            self.show_error_notification("Error submitting data")


class MainScreen(Screen):
    def __init__(self, session_manager, **kwargs):
        super().__init__(**kwargs)
        self.session_manager = session_manager
        self.label = None
        self.main_layout = FloatLayout()
        self.main_layout.canvas.before.add(Color(0.8, 0.8, 0.8, 1))
        self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.canvas.before.add(self.rect)
        self.main_layout.bind(size=self.update_rect, pos=self.update_rect)
        self.scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        self.show_label()
        self.scroll_view = ScrollView(opacity=0, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.8, 0.3))
        Clock.schedule_once(lambda dt: self.fade_label(dt, 1, 0), 3.5)
        self.scroll_view.add_widget(self.scroll_layout)
        self.main_layout.add_widget(self.scroll_view)
        Clock.schedule_once(self.update_scroll_view, 5.0)
        Clock.schedule_once(self.add_search_recipe_button, 5.0)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def fade_label(self, dt, start_opacity, end_opacity):
        animation = Animation(opacity=end_opacity, duration=1.5)
        animation.start(self.label)

    def show_label(self):
        session = self.session_manager.create_session()
        user_data = session.query(UserData).first()
        user_name = user_data.user_name if user_data else None
        session.close()
        self.label = Label(
            color='#050A30',
            font_size=36,
            opacity=0,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            text=f"Welcome to Grin & Gourmet, {user_name}! Enjoy the app!"
        )
        self.main_layout.add_widget(self.label)
        self.add_widget(self.main_layout)
        Clock.schedule_once(lambda dt: self.fade_label(dt, 0, 1), 0.5)

    def on_edit_recipe(self, instance):
        pass

    def update_scroll_view(self, dt=None):
        self.scroll_layout.clear_widgets()
        session = self.session_manager.create_session()
        recipe_data = (session.query(RecipeData.recipe_name, RecipeData.recipe_rating).all())
        for recipe_name, recipe_rating in recipe_data:
            if recipe_rating is None:
                recipe_rating = '-'
            edit_recipe_button = Button(
                background_color='#145DA0',
                height=60,
                on_press=self.on_edit_recipe,
                size_hint_y=None,
                text=f"{recipe_name} - Rating: {recipe_rating}/5 Stars"
            )
            self.scroll_layout.add_widget(edit_recipe_button)
        session.close()
        Animation(opacity=1, duration=1.5).start(self.scroll_view)

    def add_search_recipe_button(self, dt):
        search_label = Label(
            color='#050A30',
            font_size=24,
            opacity=0,
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
            text="Search for recipes"
        )
        self.main_layout.add_widget(search_label)
        search_bar = TextInput(
            multiline=False,
            size_hint=(0.8, 0.08),
            opacity=0,
            pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )
        self.main_layout.add_widget(search_bar)
        make_recipe_button = Button(
            background_color='#145DA0',
            on_press=self.show_recipe_dialog,
            opacity=0,
            pos_hint={'right': 0.98, 'top': 0.98},
            size_hint=(0.2, 0.1),
            text="Make a Recipe!"
        )
        self.main_layout.add_widget(make_recipe_button)
        Animation(opacity=1, duration=1.5).start(search_label)
        Animation(opacity=1, duration=1.5).start(search_bar)
        Animation(opacity=1, duration=1.5).start(make_recipe_button)

    def show_recipe_dialog(self, instance):
        recipe_dialog = RecipeDialog(session_manager=self.session_manager)
        recipe_dialog.open()


class StartScreen(Screen):
    pass


class StartApp(App):
    def __init__(self):
        super().__init__()
        self.button = None
        self.label = None
        self.rect = None
        self.user = None
        self.title = "GrinAndGourmet"
        self.icon = "images/gg-icon.png"
        self.screen_manager = ScreenManager()
        self.session_manager = SessionManager()

    def build(self):
        if self.check_user_data():
            print("User data is detected")
            self.switch_to_main_screen()
        else:
            print("User data is not detected")
            print("Creating a start screen")
            start_screen = StartScreen(name='start_screen')
            start_layout = self.create_start_layout()
            start_screen.add_widget(start_layout)
            self.screen_manager.add_widget(start_screen)
        Window.minimum_width = 640
        Window.minimum_height = 480
        return self.screen_manager

    @staticmethod
    def show_error_notification(message):
        content = Label(text=message)
        popup = Popup(title='Error', content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def create_start_layout(self):
        start_layout = FloatLayout()
        with start_layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(size=start_layout.size, pos=start_layout.pos)
        self.rect.size = start_layout.size
        start_layout.bind(size=self.update_rect, pos=self.update_rect)
        start_layout.add_widget(self.create_start_window())
        return start_layout

    def store_name_and_switch(self, instance):
        if self.user.text:
            if len(self.user.text) > 20:
                self.user.text = self.user.text[:17] + "..."
            session = self.session_manager.create_session()
            session.add(UserData(user_name=self.user.text))
            session.commit()
            session.close()
            self.switch_to_main_screen()
        else:
            print("No input detected")
            self.show_error_notification("No input detected")

    def create_start_window(self):
        window = GridLayout()
        window.cols = 1
        window.size_hint = (0.6, 0.7)
        window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        window.add_widget(Image(source="images/gg-title.png"))
        self.label = Label(
            color='#050A30',
            font_size=24,
            text="What is your name?"
        )
        window.add_widget(self.label)
        self.user = TextInput(
            multiline=False,
            padding=(5, 5),
            size_hint=(1, 0.5)
        )
        window.add_widget(self.user)
        self.button = Button(
            background_color='#145DA0',
            bold=True,
            size_hint=(1, 0.5),
            text="ENTER"
        )
        self.button.bind(on_press=self.store_name_and_switch)
        window.add_widget(self.button)
        return window

    def check_user_data(self):
        session = self.session_manager.create_session()
        user_data = session.query(UserData).first()
        session.close()
        return user_data is not None

    def switch_to_main_screen(self):
        main_screen = MainScreen(name='main_screen', session_manager=self.session_manager)
        self.screen_manager.switch_to(main_screen)
        print("Switched to main screen")


if __name__ == "__main__":
    print("Commencing initialization of the Grin & Gourmet app")
    StartApp().run()
