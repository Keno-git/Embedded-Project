from scipy.io.wavfile import write
from speechbrain.pretrained import EncoderClassifier
import sounddevice as sd

model = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")
duration = 5
sample_rate = 16000

print("Recording")
myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()
print("Done")

wav_file = "output.wav"
write(wav_file, sample_rate, myrecording)

model.classify_file("output.wav")