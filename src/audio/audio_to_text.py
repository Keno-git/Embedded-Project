import whisper
import os

class Audio_To_Text:
    def __init__(self) -> None:
        '''
        Load base model into class
        '''
        self.model = whisper.load_model("base")

    def transcribe_audio(self, soundfilepath):
        '''
        Should take in a the path to the string, a np.ndarray (raw sound), or a torch.Tensor (raw sound)
        '''
        result = self.model.transcribe(soundfilepath)
        os.remove(soundfilepath)
        return result['text'], result['language']