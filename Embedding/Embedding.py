from resemblyzer import VoiceEncoder

def Embedding(wav, return_partials=True, rate=16):
    encoder = VoiceEncoder("cpu")
    return encoder.embed_utterance(wav, return_partials=return_partials, rate=rate)