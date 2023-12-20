import pyaudio
import math
import struct
import wave
import time
import os
import cv2 as cv

class Audio_Manager:
    '''
    Class to manage and process user audio input
    '''
    def __init__(self) -> None:
        '''
        Initialize class properties
        '''
        # Class constants
        self.AUDIO_FORMAT = pyaudio.paInt16
        self.AUDIO_CHANNELS = 1
        self.AUDIO_RATE = 16000
        self.AUDIO_CHUNK = 1024
        self.TIMEOUT_LENGTH = 3
        self.THRESHOLD = 10
        self.SWIDTH = 2
        self.SHORT_NORMALIZATION = (1.0/32768.0)
        self.AUDIO_DIRECTORY = "./audio_cache"
        # Class variables
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.AUDIO_FORMAT, channels=self.AUDIO_CHANNELS, rate=self.AUDIO_RATE, input=True, output=True, frames_per_buffer=self.AUDIO_CHUNK)

    def rms(self, frame):
        '''
        Calculate byte frame RMS
        '''
        count = len(frame) / self.SWIDTH
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n =  sample * self.SHORT_NORMALIZATION
            sum_squares += n*n
        rms = math.pow(sum_squares / count, 0.5)
        return rms * 1000
    
    def write(self, recording) -> str:
        '''
        Save audio recordings into .wav format files
        '''
        number_frames_to_remove = self.TIMEOUT_LENGTH * self.AUDIO_RATE
        recording = recording[: len(recording) - number_frames_to_remove]
        number_files = len(os.listdir(self.AUDIO_DIRECTORY))
        file_name = '{}.wav'.format(number_files)
        file_path = os.path.join(self.AUDIO_DIRECTORY, file_name)

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(self.AUDIO_CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.AUDIO_FORMAT))
            wf.setframerate(self.AUDIO_RATE)
            wf.writeframes(recording)
            wf.close()
        
        print('Written to file: {}'.format(file_path))
        print('Finished listening')
        return file_path
    
    def record(self, initial_chunk) -> str:
        '''
        Record audio until the timeout is completed
        '''
        print('Beginning recording...')
        recording = [initial_chunk]
        current_time = time.time()
        end_time = current_time + self.TIMEOUT_LENGTH

        while current_time <= end_time:
            data = self.stream.read(self.AUDIO_CHUNK)
            if self.rms(data) >= self.THRESHOLD:
                end_time = time.time() + self.TIMEOUT_LENGTH
            current_time = time.time()
            recording.append(data)
        return self.write(b''.join(recording))

    def listen(self):
        '''
        Listen and record user input until waiting threshold has been surpassed
        '''
        print("Listening... (Press 'Q' to stop the application)")
        while True:
            input = self.stream.read(self.AUDIO_CHUNK)
            rms_value = self.rms(input)
            if rms_value > self.THRESHOLD:
                return self.record(input)