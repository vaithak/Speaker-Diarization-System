import numpy as np
import librosa
import collections
!pip install webrtcvad
from webrtcvad import Vad
from struct import pack
from scipy.ndimage.morphology import binary_dilation
# from hyperparameters import *
int16_limit = 2**15 - 1
samplerate = 16000

class vad_hp(object):
    def __init__ (self):
        self.frame_duration = 0.03
        self.target_dB = -30
        self.width_moving_average = 8
        self.max_silent_samples = 6
        
class VAD(object):
    def __init__ (self,mode,wav_data):
        self.mode = mode
        self.wav_data = wav_data
        self.vad_hp = vad_hp()
    
    def process(self):
        self.wav_data = self.normalize()
        self.wav_data = self.voice_activity_detector()
        return self.wav_data
    
    def normalize(self,variation = 1):
        power = np.sqrt( np.mean( (self.wav_data*int16_limit)**2 ) )  # RMS-Value is proportional to power of audio signal
        actual_dB = 20 * np.log10( (power/int16_limit) )    # Calcuating actual decibel level of audio input
        target_dB = self.vad_hp.target_dB
        diff_dB = target_dB - actual_dB                     # Calculating difference between desired and actual decibel level
        if ( (diff_dB < 0 and variation == 1) and (diff_dB > 0 and variation == -1) ):
            return self.wav_data 
        return self.wav_data * ( 10** (diff_dB/20) )
    
    def voice_activity_detector(self):
        silence = []
        vad = Vad(mode=self.mode)
        step = int((samplerate* self.vad_hp.frame_duration))
        self.wav_data = self.wav_data[:len(self.wav_data)-len(self.wav_data)%step]
        pcm = pack("%dh"%len(self.wav_data), *(np.round(int16_limit*self.wav_data)).astype(np.int16))
        for i in range(0, len(self.wav_data), step):
            j = i + step
            if(j > len(self.wav_data)):
                break
            segment = vad.is_speech( pcm[i*2:j*2], sample_rate = samplerate )
            silence.append(segment)
        silence = np.array(silence)
        mask = self.remove_silence(silence)
        return self.wav_data[mask==True]

    def remove_silence(self,segments):
        mask = self.smoothing_timeseries(segments, self.vad_hp.width_moving_average)
        mask = np.round(mask).astype(bool)
        mask = binary_dilation(mask, np.ones(self.vad_hp.max_silent_samples+1))
        step = int((samplerate* self.vad_hp.frame_duration))
        mask = np.repeat(mask, step)
        return mask

    def smoothing_timeseries(self,timeseries, width):
        padding = np.concatenate( (np.zeros((width-1)//2), timeseries, np.zeros((width//2))) )
        cumulative = np.cumsum(padding, dtype=float)
        cumulative[width:] = cumulative[width:] - cumulative[:-width]
        smooth_timeseries = cumulative[width-1:]/width
        return smooth_timeseriess