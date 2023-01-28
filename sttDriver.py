import speechToText
import queue
import sys
from threading import Thread

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


def main():
    transcription_q = queue.Queue()
    thread = Thread(target=speechToText.start_speech_to_text, args=(transcription_q,))
    thread.start()

    while True:
        message = transcription_q.get()
        if message[1] == 1:
            sys.stdout.write(GREEN)
            sys.stdout.write("\r" + message[0] + "\n")
        else:
            sys.stdout.write(RED)
            sys.stdout.write("\r" + message[0])


if __name__ == "__main__":
    main()
