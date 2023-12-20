# Import libraries
from audio.audio_manager import Audio_Manager
from audio.audio_to_text import Audio_To_Text
from translation.translation_manager import Translation_Manager
from auto_reply.auto_response import Auto_Response

def main():
    '''
    Main thread of the application
    '''
    audio_manager = Audio_Manager()
    audio_to_text = Audio_To_Text()
    translation_manager = Translation_Manager()
    auto_response = Auto_Response()

    translation(audio_manager, audio_to_text, translation_manager, auto_response)

def translation(audio_manager: Audio_Manager, audio_to_text: Audio_To_Text, translation_manager: Translation_Manager, auto_response: Auto_Response, default_translation_language='es'):
    '''
    Execute translation program pipeline
    '''
    base_language = 'en'
    translation_language = default_translation_language

    # Iterate flow until stoppage 
    while True:
        # Listen to user input
        audio_file = audio_manager.listen()
        # Obtain text and language of recorded audio
        text, language = audio_to_text.transcribe_audio(audio_file)
        write_log("Language {language_detected}: {text}".format(language_detected=language, text=text))
        # If audio was in English
        if language == base_language:
            translated_text = translation_manager.translate_from_english(translation_language, text)
            write_log("\tTranslation to {language}: {translation}".format(language=translation_language, translation=translated_text))
            # Generate smart response
            smart_response = auto_response.generate_response(text)
            write_log("\tSuggested answer in {language}: {suggested_answer}\n".format(language=language, suggested_answer=smart_response))
        # If audio is Spanish or Swedish
        else:
            translation_language = language
            translated_text = translation_manager.translate_to_english(translation_language, text)
            write_log("\tTranslation to {language}: {translation}".format(language=base_language, translation=translated_text))
            # Generate smart response
            smart_response = auto_response.generate_response(translated_text)
            write_log("\tSuggested answer in {language}: {suggested_answer}\n".format(language=base_language, suggested_answer=smart_response))

def write_log(message, file_name='conversation.txt'):
    # Open file in append mode
    file = open(file=file_name, mode="a", encoding='utf8')
    # Write log
    file.write(message)
    # Write line jump
    file.write("\n")
    # Close file
    file.close()

# Main program of the application
if __name__ == '__main__':
    main()