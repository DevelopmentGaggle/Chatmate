import speechToText
import queue
import sys
import ChatGPT
import os
from io import BytesIO
from playsound import playsound
from gtts import gTTS
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


def main():
    transcription_q = queue.Queue()
    thread = Thread(target=speechToText.start_speech_to_text, args=(transcription_q,))
    thread.start()

    chat_gpt3 = ChatGPT.ChatGPT3(initial_context="""You are a senior computer engineer interviewing me for a position at your company, Google. You will ask several questions and I will respond to those questions until you initiate the end of the interview after four or so questions. The only exception to this will be during the intrpductions at the start of the mock interview where I introduce myself first

    """)

    transaction = 0
    while True:
        message = transcription_q.get()
        if message[1] == 1:
            sys.stdout.write(GREEN)
            sys.stdout.write("\r" + message[0] + "\n")

            response = chat_gpt3.get_prompt(message[0], transaction > 3)
            print(response)
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

if __name__ == "__main__":
    main()
