#from scipy.io.wavfile import write
from speechbrain.pretrained import EncoderClassifier
#import sounddevice as sd

def identify_language(path):


    model = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")

    #Easiest and fastest way is to read file, it may be possible to read direct from torch tensor but I'm excluding that code from here from now since it's a mess.
    """
    duration = 5
    sample_rate = 16000 
    print("Recording")
    myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    print("Done")
    wav_file = "output.wav"
    write(wav_file, sample_rate, myrecording)
    """

    matrix, tensor, shape, language = model.classify_file(path)
    return language[0]