import kivy
import sttDriver
import queue
from threading import Thread
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock

prompt = 'What type of interview would you like to prepare for?'
CGPT = 'ChatGPT'
response_q = queue.Queue()
isTalking = False
current_time_in_minutes = 0

class StartScreen(Screen):
    pass

class SetupScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class MainApp(MDApp):

    stopwatch_time = StringProperty()
    milliseconds = NumericProperty()
    seconds = NumericProperty()
    minutes = NumericProperty()
    watch_started = False

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        sm = Builder.load_file('app.kv')

        return sm

    def setup_session(self, name_in, api_key_in):
        global name
        name = name_in
        global api_key 
        api_key = api_key_in
        if name == '' or api_key == '':
            return
        self.root.current = 'setup'

    def launch_interview(self, company_in, role_in, duration_in, difficulty_in):
        self.root.current = 'main'
        global company
        company = company_in
        global role
        role = role_in
        global duration
        duration = duration_in
        global difficulty
        difficulty = difficulty_in

    def go_back_setup(self):
        self.root.ids.main_screen.ids.chatlist.clear_widgets()
        self.reset_stopwatch()
        self.root.current = 'setup'

    def go_back_start(self):
        self.root.current = 'start'

    def load_main(self):
        if len(self.root.ids.main_screen.ids.chatlist.children) == 0:
            file = open("./storage/transcript.txt", 'w')
            file.write(CGPT + ': ' + prompt)
            self.add_msg(CGPT, prompt)
            self.add_msg(name, 'temp')
        self.stopwatch_time = "00:00:00"
        self.start_or_stop_stopwatch()

        tts_thread = Thread(target=sttDriver.stt_driver_main, args=(response_q,))
        tts_thread.start()

        Clock.schedule_interval(self.my_callback, 1 / 30.)

    def toggle_mute(self):
        icon = self.root.ids.main_screen.ids.mute.icon
        self.edit_msg('hi new msg')
        if icon == 'microphone':
            self.root.ids.main_screen.ids.mute.icon = 'microphone-off'
        else:
            self.root.ids.main_screen.ids.mute.icon = 'microphone'

    def start_or_stop_stopwatch(self):
        pass

    # add this function
    def get_string_time(self, dt):
        """Function to increment milliseconds and convert the time elapsed to string format to which the label is set"""
        self.increment_milliseconds()

        milliseconds = str(self.milliseconds)
        seconds = str(self.seconds)
        minutes = str(self.minutes)

        if len(milliseconds) < 2:
            milliseconds = '0' + milliseconds

        if len(seconds) < 2:
            seconds = '0' + seconds

        if len(minutes) < 2:
            minutes = '0' + minutes

        self.stopwatch_time = minutes + ":" + seconds + ":" + milliseconds
        global current_time_in_minutes
        current_time_in_minutes = minutes

    # Modify start_or_stop_stopwatch to look as follows
    def start_or_stop_stopwatch(self):
        """Function to stop the stopwatch if it is not running otherwise stop it"""
        if self.watch_started:
            self.watch_started = False
            self.root.ids.main_screen.ids['play_pause_btn'].icon = 'play'
            Clock.unschedule(self.get_string_time) # Unschedule the get_string_time function
        else:
            self.watch_started = True
            self.root.ids.main_screen.ids['play_pause_btn'].icon = 'pause'
            Clock.schedule_interval(self.get_string_time, 0.1) # schedule the get_string_time function to run every 10ms

    # add the following function
    def increment_milliseconds(self):
        """Increment the milliseconds by 10ms"""
        self.milliseconds += 10

        if self.milliseconds == 100:
            self.increment_seconds()
            self.milliseconds = 0

    # add the following function
    def increment_seconds(self):
        """Increment the seconds by 1 second"""
        self.seconds += 1

        if self.seconds == 60:
            self.increment_minutes()
            self.seconds = 0

    # add the following function
    def increment_minutes(self):
        """Increment the minutes by 1 minute"""
        self.minutes += 1

    def reset_stopwatch(self):
        """Set the stopwatch to 00:00:00"""
        if self.watch_started:
            self.watch_started = False
            self.root.ids.main_screen.ids['play_pause_btn'].icon = 'play'
            Clock.unschedule(self.get_string_time) # Unschedule the get_string_time function
        self.stopwatch_time = "00:00:00"
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        
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

    def my_callback(self, soup):
        global isTalking
        if not response_q.empty():
            response = response_q.get()
            print(CGPT)
            print(super)
            if response[1] == sttDriver.CHATGPT_MESSAGE:
                self.add_msg(CGPT, response[0])
            elif response[1] == sttDriver.USER_MESSAGE_FINAL:
                isTalking = False

                self.edit_msg(response[0])
            else:
                if not isTalking:
                    isTalking = True
                    self.add_msg(name, response[0])
                else:
                    self.edit_msg(response[0])

    def edit_msg(self, text):
        self.root.ids.main_screen.ids.chatlist.children[0].secondary_text = text


if __name__ == "__main__":
    MainApp().run()
