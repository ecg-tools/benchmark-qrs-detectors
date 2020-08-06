#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script provides the list of available qrs detectors and method to use one of them on a given sampled signal."""

from ecgdetectors import Detectors
import biosppy.signals.ecg as bsp_ecg
import biosppy.signals.tools as bsp_tools
import mne.preprocessing.ecg as mne_ecg
import heartpy.peakdetection as hp_pkdetection
from heartpy.datautils import rolling_mean
from wfdb import processing
import numpy
from typing import List

# list of algorithms
algorithms_list = ['Pan-Tompkins-ecg-detector', 'Hamilton-ecg-detector', 'Christov-ecg-detector',
                   'Engelse-Zeelenberg-ecg-detector', 'SWT-ecg-detector', 'Matched-filter-ecg-detector',
                   'Two-average-ecg-detector', 'Hamilton-biosppy', 'Christov-biosppy',
                   'Engelse-Zeelenberg-biosppy', 'Gamboa-biosppy', 'mne-ecg', 'heartpy', 'gqrs-wfdb', 'xqrs-wfdb']


def run_algo(algorithm: str, sig: numpy.ndarray, freq_sampling: int) -> List[int]:
    """
    run a qrs detector on a signal

    :param algorithm: name of the qrs detector to use
    :type algorithm: str
    :param sig: values of the sampled signal to study
    :type sig: ndarray
    :param freq_sampling: value of sampling frequency of the signal
    :type freq_sampling: int
    :return: localisations of qrs detections
    :rtype: list(int)
    """
    detectors = Detectors(freq_sampling)
    if algorithm == 'Pan-Tompkins-ecg-detector':
        qrs_detections = detectors.pan_tompkins_detector(sig)
    elif algorithm == 'Hamilton-ecg-detector':
        qrs_detections = detectors.hamilton_detector(sig)
    elif algorithm == 'Christov-ecg-detector':
        qrs_detections = detectors.christov_detector(sig)
    elif algorithm == 'Engelse-Zeelenberg-ecg-detector':
        qrs_detections = detectors.engzee_detector(sig)
    elif algorithm == 'SWT-ecg-detector':
        qrs_detections = detectors.swt_detector(sig)
    elif algorithm == 'Matched-filter-ecg-detector' and freq_sampling == 360:
        qrs_detections = detectors.matched_filter_detector(sig, 'templates/template_360hz.csv')
    elif algorithm == 'Matched-filter-ecg-detector' and freq_sampling == 250:
        qrs_detections = detectors.matched_filter_detector(sig, 'templates/template_250hz.csv')
    elif algorithm == 'Two-average-ecg-detector':
        qrs_detections = detectors.two_average_detector(sig)
    elif algorithm == 'Hamilton-biosppy':
        qrs_detections = bsp_ecg.ecg(signal=sig, sampling_rate=freq_sampling, show=False)[2]
    elif algorithm == 'Christov-biosppy':
        order = int(0.3 * freq_sampling)
        filtered, _, _ = bsp_tools.filter_signal(signal=sig,
                                                 ftype='FIR',
                                                 band='bandpass',
                                                 order=order,
                                                 frequency=[3, 45],
                                                 sampling_rate=freq_sampling)
        rpeaks, = bsp_ecg.christov_segmenter(signal=filtered, sampling_rate=freq_sampling)
        rpeaks, = bsp_ecg.correct_rpeaks(signal=filtered, rpeaks=rpeaks, sampling_rate=freq_sampling, tol=0.05)
        _, qrs_detections = bsp_ecg.extract_heartbeats(signal=filtered, rpeaks=rpeaks, sampling_rate=freq_sampling,
                                                       before=0.2, after=0.4)
    elif algorithm == 'Engelse-Zeelenberg-biosppy':
        order = int(0.3 * freq_sampling)
        filtered, _, _ = bsp_tools.filter_signal(signal=sig,
                                                 ftype='FIR',
                                                 band='bandpass',
                                                 order=order,
                                                 frequency=[3, 45],
                                                 sampling_rate=freq_sampling)
        rpeaks, = bsp_ecg.engzee_segmenter(signal=filtered, sampling_rate=freq_sampling)
        rpeaks, = bsp_ecg.correct_rpeaks(signal=filtered, rpeaks=rpeaks, sampling_rate=freq_sampling, tol=0.05)
        _, qrs_detections = bsp_ecg.extract_heartbeats(signal=filtered, rpeaks=rpeaks, sampling_rate=freq_sampling,
                                                       before=0.2, after=0.4)
    elif algorithm == 'Gamboa-biosppy':
        order = int(0.3 * freq_sampling)
        filtered, _, _ = bsp_tools.filter_signal(signal=sig,
                                                 ftype='FIR',
                                                 band='bandpass',
                                                 order=order,
                                                 frequency=[3, 45],
                                                 sampling_rate=freq_sampling)
        rpeaks, = bsp_ecg.gamboa_segmenter(signal=filtered, sampling_rate=freq_sampling)
        rpeaks, = bsp_ecg.correct_rpeaks(signal=filtered, rpeaks=rpeaks, sampling_rate=freq_sampling, tol=0.05)
        _, qrs_detections = bsp_ecg.extract_heartbeats(signal=filtered, rpeaks=rpeaks, sampling_rate=freq_sampling,
                                                       before=0.2, after=0.4)
    elif algorithm == 'mne-ecg':
        qrs_detections = mne_ecg.qrs_detector(freq_sampling, sig)
    elif algorithm == 'heartpy':
        rol_mean = rolling_mean(sig, windowsize=0.75, sample_rate=100.0)
        qrs_detections = hp_pkdetection.detect_peaks(sig, rol_mean, ma_perc=20, sample_rate=100.0)['peaklist']
    elif algorithm == 'gqrs-wfdb':
        qrs_detections = processing.qrs.gqrs_detect(sig=sig, fs=freq_sampling)
    elif algorithm == 'xqrs-wfdb':
        qrs_detections = processing.xqrs_detect(sig=sig, fs=freq_sampling)
    else:
        raise ValueError(f'Sorry... unknown algorithm. Please check the list {algorithms_list}')
    cast_qrs_detections = [int(element) for element in qrs_detections]
    return cast_qrs_detections
