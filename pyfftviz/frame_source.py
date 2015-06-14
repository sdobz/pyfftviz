# Functional programming??
import glob
from moviepy.video.VideoClip import VideoClip
from scipy.ndimage import imread as scipy_imread
from scipy.misc import imresize as scipy_imresize

# glob.iglob('*.png')

cap = lambda lower, value, upper: min(max(value, lower), upper)


class GlobStore(object):
    def __init__(self, image_pattern, resize=None):
        self.images = glob.glob(image_pattern)
        self.images_len = len(self.images)
        assert self.images_len > 0
        self.image_cache = {}
        self.resize = resize

    def image_from_normal(self, n):
        image_index = cap(0, int(n * self.images_len), self.images_len-1)

        image_filename = self.images[image_index]

        if image_filename in self.image_cache:
            return self.image_cache[image_filename]

        image_data = scipy_imread(image_filename)
        if self.resize:
            image_data = scipy_imresize(image_data, size=self.resize, interp='bicubic')
        if image_data.shape[2] == 4:
            image_data = image_data[:,:,0:3]


        self.image_cache[image_filename] = image_data
        return image_data


class AmplitudeClip(VideoClip):
    def __init__(self, glob_store, freq, fft_clip, ismask=False):

        def make_frame(t):
            freq_amplitude = fft_clip.freq_amplitude(freq, t)
            image_data = glob_store.image_from_normal(freq_amplitude)
            return image_data

        VideoClip.__init__(self, make_frame=make_frame, ismask=ismask, duration=fft_clip.duration)
