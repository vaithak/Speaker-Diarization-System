import glob
from scipy.io import wavfile
from pyannote.database.util import load_rttm

class DataLoader():
    """docstring for DataLoader"""
    def __init__(self, audio_folder, labels_folder, names_only=False):
        # Audio files are assumed to have .wav extension,
        # Label files are assumed to have .rttm extension
        self.audio_files = sorted(glob.glob(audio_folder + "/*.wav"))
        self.label_files = sorted(glob.glob(labels_folder + "/*.rttm"))
        self.names_only = names_only

        assert len(self.audio_files) == len(self.label_files)
    

    def __len__(self):
        return len(self.label_files)


    def __getitem__(self, idx):
        # Extract labels from rttm file
        label_dict = load_rttm(self.label_files[idx])
        label = list(label_dict.values())
        label = label[0]

        if self.names_only:
          return (self.audio_files[idx], label)

        # Extract audio and sample rate from wav file
        samplerate, wav_data = wavfile.read(self.audio_files[idx])

        return ((samplerate, wav_data), label)
        