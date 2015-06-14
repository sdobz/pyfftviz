from __future__ import division
from moviepy.audio.io.AudioFileClip import AudioFileClip
from numpy import absolute
import numpy as np
from numpy.fft import rfft


class FFTClip(AudioFileClip):
    fft_size = 512
    fft_cache = None
    fft_cache_index = None

    def freq_amplitude(self, freq, t):
        nyquist_freq = self.fps/2
        # Normalize frequency from 0 to nyquist to 0 to 1
        # And multiply 
        freq_bucket = int((freq/nyquist_freq) * (self.fft_size/2))

        # load the correct fft
        fft_data = self.get_fft(t)
        # 0hz to nyquist is fft_data[0] to fft_data[fft_size/2]

        return fft_data[freq_bucket]

    def get_fft(self, t):
        t_frame = int(t*self.fps)
        # Find the earliest frame at a multiple of fft_size
        # This is the start of a fft_size sample long segment that we will fourier transform
        start_frame = t_frame - t_frame%self.fft_size

        # This is the index,
        # 0 to fft_size = 0
        # fft_size to 2*fft_size = 1
        # ...
        fft_index = int(start_frame/self.fft_size)

        # Load it from cache if needed
        if fft_index == self.fft_cache_index:
            return self.fft_cache

        # Compute a normalized fft over the samples from start_frame to start_frame + fft_size
        samples = self.get_samples(start_frame)
        fft_data = absolute(rfft(samples))**2

        fft_data *= 1e2
        self.fft_cache = fft_data
        self.fft_cache_index = fft_index
        return fft_data

    def get_samples(self, start_frame):
        # Get fft_size samples starting at start_frame
        frame_times = np.array([float(frame)/self.fps for frame in
            xrange(start_frame, start_frame+self.fft_size)])
        return self.make_frame(frame_times)[:,0]