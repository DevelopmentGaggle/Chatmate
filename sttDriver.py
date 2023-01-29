import speechToText
import sys
import ChatGPT
import queue
import os
import application.app as app
from io import BytesIO
from playsound import playsound
from gtts import gTTS
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play


RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


def stt_driver_main(response_q):
    transcription_q = queue.Queue()
    thread = Thread(target=speechToText.start_speech_to_text, args=(transcription_q,))
    thread.start()

    tc = ChatGPT.TimedConversation("Google", "Software Engineer", transitions=(5, 10, 15), difficulty=2)

    transaction = 0

    while True:
        message = transcription_q.get()
        if message[1] == 1:
            sys.stdout.write(GREEN)
            sys.stdout.write("\r" + message[0] + "\n")

            response_q.put([message[0], 1])
            response = tc.get_prompt(message[0], app.current_time_in_minutes)
            print(response)
            response_q.put([response, 0])

            mp3_fp = BytesIO()
            tts = gTTS(text=response, lang='en')
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            song = AudioSegment.from_file(mp3_fp, format="mp3")

            tts_thread = Thread(target=play, args=(song,))
            tts_thread.start()
            tts_thread.join()
            while not transcription_q.empty():
                transcription_q.get()

            transaction = transaction + 1
        else:
            sys.stdout.write(RED)
            sys.stdout.write("\r" + message[0])


# rbq = RankByQualifier("Strong problem-solving and analytical skills")
# rbq = RankByQualifier("motivated")
# rbq = RankByQualifier("confident and commanding")
#rbq = RankByQualifier("positive")
#print("Bad: " + rbq.get_prompt("I was unfortunately unable to meet the deadline. My VHDL code also never worked."))
#print("Good: " + rbq.get_prompt("I was unfortunately unable to meet the deadline. Despite this, I worked with my managers to develop a plan to recover from this and was able to meet the second milestone in advance of the deadline!"))


#chat_gpt3 = ChatGPT3(initial_context="""You are a senior computer engineer interviewing me for a position at your company, Google. You will ask several questions and I will respond to those questions until you initiate the end of the interview after four or so questions. The only exception to this will be during the intrpductions at the start of the mock interview where I introduce myself first

#""")

#for i in range(6):
#    user_input = input()
#    if user_input == "quit":
#        break
#    print(chat_gpt3.get_prompt(user_input, i > 3))

