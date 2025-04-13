import speech_recognition as sr
from main import assistant, ask_model


if __name__ == '__main__':
    r = sr.Recognizer()
    listening = True
    while listening:
        print('========================================')
        try:
            if len(input('PRESS ENTER TO ASK SOMETHING\n')) < 1:
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source,timeout=100)
                print(f'... translating ...')
                try:
                    text = r.recognize_vosk(audio,"en-us")  # You can replace google with other engines like sphinx
                    print(f'... asking morpheus: {text}')
                    result = assistant(text)
                    print(f'Reply:\n{result}\n========================================')
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
        except KeyboardInterrupt:
            listening = False
            print(f'Killing Speech to Text')
            pass
