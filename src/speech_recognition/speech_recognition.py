from speechbrain.pretrained import EncoderClassifier

# Constant class variables
MODEL_SOURCE = "speechbrain/lang-id-voxlingua107-ecapa"
MODEL_DIR = "./models/speech_recognition"

class Speech_Recognizer:
    '''
    Class to classify audio tensors into languages
    '''
    def __init__(self) -> None:
        '''
        Initialize class properties
        '''
        self.model = EncoderClassifier.from_hparams(source=MODEL_SOURCE, savedir=MODEL_DIR)

    def classify_audio(self, audio_file):
        '''
        Classifies the given audiofile into the given set of labels
        '''
        prediction = self.model.classify_file(audio_file)
        return prediction[3][0]