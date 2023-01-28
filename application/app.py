import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

class StartScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "DeepPurple"
        sm = Builder.load_file('app.kv')
        return sm

    def session(self, name, api_key):
        print('name: ', name, '\napi key: ', api_key)
        self.root.current = 'main'

if __name__ == "__main__":
    MainApp().run()