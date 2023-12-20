import tensorflow as tf
import numpy as np
import tensorflow_text
import os

class Translation_Manager:
    '''
    Class to manage translation model
    '''
    def __init__(self) -> None:
        '''
        Initialize class properties
        '''
        self.MODEL_DIRECTORY = './models/translation'
        # Define interpreters as None
        self.english_spanish_interpreter = None
        self.spanish_english_interpreter = None
        self.english_swedish_interpreter = None
        self.swedish_english_interpreter = None

    
    def load_model(self, interpreter, file_name):

        if interpreter is None:
            interpreter = tf.lite.Interpreter(model_path=os.path.join(self.MODEL_DIRECTORY, file_name))
            interpreter.allocate_tensors()
        return interpreter

    def translate_to_english(self, language, text):
        '''
        Languages can be { 'es': Spanish,'en': English", 'sv': Swedish" }
        '''
        if language == 'sv':
            file_name = 'sv_en_translation.tflite'
            interpreter = self.load_model(self.swedish_english_interpreter, file_name)
        else:
            file_name = 'es_en_translation.tflite'
            interpreter = self.load_model(self.spanish_english_interpreter, file_name)
        
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], np.array([text]))
        interpreter.invoke()

        return interpreter.get_tensor(output_details[0]['index'])[0].decode('UTF-8')
    
    def translate_from_english(self, output_language, text):
        '''
        Languages can be { 'es': Spanish,'en': English", 'sv': Swedish" }
        '''
        if output_language == 'sv':
            file_name = 'en_sv_translation.tflite'
            interpreter = self.load_model(self.english_swedish_interpreter, file_name)
        else:
            file_name = 'en_es_translation.tflite'
            interpreter = self.load_model(self.english_spanish_interpreter, file_name)
        
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], np.array([text]))
        interpreter.invoke()

        return interpreter.get_tensor(output_details[0]['index'])[0].decode('UTF-8')