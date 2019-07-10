#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xicam.plugins import ProcessingPlugin, Input, Output


class FFT(ProcessingPlugin):
    name = 'FFT'
    """
    Return uniformly distributed projection angles in radian.
    """
    image = Input(description='Input array, can be complex.', type='np.ndarray')
    n = Input(
        description='Length of the transformed axis of the output. If n is smaller than the length of the input, the input is cropped. If it is larger, the input is padded with zeros. If n is not given, the length of the input along the axis specified by axis is used.',
        type=int, default=None)
    axis = Input(description='Axis over which to compute the FFT. If not given, the last axis is used.', type=int,
                 default=None)
    norm = Input(description='Normalization mode.', type=str, default=None)

    out = Output(
        description='The truncated or zero-padded input, transformed along the axis indicated by axis, or the last one if axis is not specified.',
        type='np.ndarray')

    def evaluate(self):
        import numpy as np
        kwargs = dict()
        if self.n.value is not None:
            kwargs['n'] = self.n.value
        if self.axis.value is not None:
            kwargs['axis'] = self.axis.value
        if self.norm.value is not None:
            kwargs['norm'] = self.norm.value
        self.out.value = np.fft.fftshift(np.fft.fft2(self.image.value, **kwargs))
