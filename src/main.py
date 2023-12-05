# Import libraries
import cv2 as cv
from audio.audio_manager import Audio_Manager
from speech_recognition.speech_recognition import Speech_Recognizer


def main():
    '''
    Main thread of the application
    '''
    audio_manager = Audio_Manager()
    speech_recognizer = Speech_Recognizer()

    audio_file = audio_manager.listen()
    speech_language = speech_recognizer.classify_audio(audio_file)
    '''
    For Oskar:
        Speech_Language can be { "es: Spanish","en: English", "sv: Swedish" }
    '''

def translation(audio_manager: Audio_Manager, speech_recognizer: Speech_Recognizer):
    '''
    Execute translation program pipeline
    '''
    canListen = True

    while True:
        if canListen:
            audio_manager.listen()
        canListen = False
        # Stop application if user presses 'Q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

# Main program of the application
if __name__ == '__main__':
    main()