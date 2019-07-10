#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xicam.plugins import ProcessingPlugin, Input, Output
import numpy as np


class FFTConvolve(ProcessingPlugin):
    """
    Return uniformly distributed projection angles in radian.
    """
    image1 = Input(description='First array', type=np.ndarray)
    image2 = Input(description='Second array', type=np.ndarray)
    mode = Input(description='Size of output', type=str, default='full')
    axes = Input(description='Axes over which to compute the convolution. The default is over all axes.', type=int)

    convolution = Output(description='Convolution of array 1 and 2.', type='np.ndarray')

    def evaluate(self):
        from scipy import signal

        self.convolution.value = signal.fftconvolve(self.image1.value,
                                                    self.image2.value,
                                                    mode=self.mode.value,
                                                    axes=self.axes.value)
