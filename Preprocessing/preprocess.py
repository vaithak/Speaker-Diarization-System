from resemblyzer import preprocess_wav

def preprocess_audio(wav_data, source_sr):
    wav_data = wav_data.astype('float64')
    wav = preprocess_wav(wav_data, source_sr = samplerate)
    return wav