import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget

prompt = 'What type of interview would you like to prepare for?'
CGPT = 'ChatGPT'

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

    def session(self, name_in, api_key_in):
        global name
        name = name_in
        global api_key 
        api_key = api_key_in
        if name == '':
            return
        self.root.current = 'main'

    def go_back(self):
        self.root.ids.main_screen.ids.chatlist.clear_widgets()
        self.root.current = 'start'

    def load_main(self):
        if len(self.root.ids.main_screen.ids.chatlist.children) == 0:
            file = open("./application/storage/transcript.txt", 'w')
            file.write(CGPT + ': ' + prompt)
            self.add_msg(CGPT, prompt)
            self.add_msg(name, 'temp')

    def add_msg(self, name, msg):
        if name == 'ChatGPT':
            icon = 'robot-happy-outline'
            radius = [50, 50, 50, 0]
            color = self.theme_cls.primary_dark
        else:
            icon = 'account-circle-outline'
            radius = [50, 50, 0, 50]
            color = self.theme_cls.primary_color
        widget = TwoLineAvatarIconListItem(
            IconLeftWidget(
                icon=icon
            ),
            text=name,
            secondary_text=msg,
            bg_color=color,
            radius=radius
        )
        self.root.ids.main_screen.ids.chatlist.add_widget(widget)

if __name__ == "__main__":
    MainApp().run()
