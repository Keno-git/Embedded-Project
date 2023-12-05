import pyaudio
import math
import struct
import wave
import time
import os

# Constant class variables
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHANNELS = 1
AUDIO_RATE = 16000
AUDIO_CHUNK = 1024
TIMEOUT_LENGTH = 3
THRESHOLD = 10
SWIDTH = 2
SHORT_NORMALIZATION = (1.0/32768.0)
AUDIO_DIRECTORY = "./audio_cache"

class Audio_Manager:
    '''
    Class to manage and process user audio input
    '''
    def __init__(self) -> None:
        '''
        Initialize class properties
        '''
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS, rate=AUDIO_RATE, input=True, output=True, frames_per_buffer=AUDIO_CHUNK)

    def rms(self, frame):
        '''
        Calculate byte frame RMS
        '''
        count = len(frame) / SWIDTH
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n =  sample * SHORT_NORMALIZATION
            sum_squares += n*n
        rms = math.pow(sum_squares / count, 0.5)
        return rms * 1000
    
    def write(self, recording) -> str:
        '''
        Save audio recordings into .wav format files
        '''
        number_frames_to_remove = TIMEOUT_LENGTH * AUDIO_RATE
        recording = recording[: len(recording) - number_frames_to_remove]
        number_files = len(os.listdir(AUDIO_DIRECTORY))
        file_name = '{}.wav'.format(number_files)
        file_path = os.path.join(AUDIO_DIRECTORY, file_name)

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(AUDIO_CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(AUDIO_FORMAT))
            wf.setframerate(AUDIO_RATE)
            wf.writeframes(recording)
            wf.close()
        
        print('Written to file: {}'.format(file_path))
        print('Returning to listening')
        return file_name
    
    def record(self, initial_chunk) -> str:
        '''
        Record audio until the timeout is completed
        '''
        print('Beginning recording...')
        recording = [initial_chunk]
        current_time = time.time()
        end_time = current_time + TIMEOUT_LENGTH

        while current_time <= end_time:
            data = self.stream.read(AUDIO_CHUNK)
            if self.rms(data) >= THRESHOLD:
                end_time = time.time() + TIMEOUT_LENGTH
            current_time = time.time()
            recording.append(data)
        return self.write(b''.join(recording))

    def listen(self):
        '''
        Listen and record user input until waiting threshold has been surpassed
        '''
        print('Listening...')
        while True:
            input = self.stream.read(AUDIO_CHUNK)
            rms_value = self.rms(input)
            if rms_value > THRESHOLD:
                return self.record(input)