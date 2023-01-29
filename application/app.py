import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget

class StartScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        sm = Builder.load_file('app.kv')
        return sm

    def session(self, name, api_key):
        self.root.current = 'main'

    def go_back(self):
        self.root.current = 'start'
        
    def load_main(self):
        self.root.ids.main_screen.ids.chatlist.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    icon='robot-happy-outline'
                ),
                text='ChatGPT',
                secondary_text='What type of interview would you like to prepare for?',
                bg_color=self.theme_cls.primary_color,
                radius=[50, 50, 50, 0]
            )
        )
        self.root.ids.main_screen.ids.chatlist.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    icon='robot-happy-outline'
                ),
                text='ChatGPT',
                secondary_text='What type of interview would you like to prepare for?',
                bg_color=self.theme_cls.primary_dark,
                radius=[50, 50, 0, 50]
            )
        )

    def add_msg(self, name, msg):
        if name == 'ChatGPT':
            icon = 'robot-happy-outline'
        else:
            icon = 'account-outline'

if __name__ == "__main__":
    MainApp().run()
