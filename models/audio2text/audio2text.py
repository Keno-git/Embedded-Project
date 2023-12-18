import whisper

class AudioToText:
    def __init__(self) -> None:
        self.model = whisper.load_model("base")

    def TranscribeAudio(self, soundfilepath):
        '''
        Should take in a the path to the string, a np.ndarray (raw sound), or a torch.Tensor (raw sound)
        '''
        result = self.model.transcribe(soundfilepath)
        return result["text"]