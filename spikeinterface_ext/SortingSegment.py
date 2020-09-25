from spikeinterface_ext.types import ChannelIndex, Order, SampleIndex, SamplingFrequencyHz, UnitId
from typing import List, Union
import numpy as np
import spikeextractors as se

class SortingSegment(object):
    def __init__(self):
        pass

    def get_unit_ids(self) -> List[UnitId]:
        raise NotImplementedError

    def get_sampling_frequency(self) -> SamplingFrequencyHz:
        raise NotImplementedError

    def get_unit_spike_train(self, unit_id: UnitId) -> np.ndarray:
        raise NotImplementedError

class NumpySortingSegment(object):
    def __init__(self, unit_ids: List[UnitId], times: np.ndarray, labels: np.ndarray, sampling_frequency: SamplingFrequencyHz):
        self._times = times
        self._labels = labels
        self._unit_ids = unit_ids
        self._sampling_frequency = sampling_frequency

    def get_unit_ids(self) -> List[UnitId]:
        return self._unit_ids

    def get_sampling_frequency(self) -> SamplingFrequencyHz:
        return self._sampling_frequency

    def get_unit_spike_train(self, unit_id: UnitId) -> np.ndarray:
        # todo: this is inefficient
        return self._times[self._labels == unit_id]

class SortingSegmentFromExtractor(SortingSegment):
    def __init__(self, sorting: se.SortingExtractor):
        self._sorting = sorting

    def get_unit_ids(self) -> List[UnitId]:
        return [UnitId(uid) for uid in self._sorting.get_unit_ids()]

    def get_sampling_frequency(self) -> SamplingFrequencyHz:
        return self._sorting.get_sampling_frequency()

    def get_unit_spike_train(self, unit_id: UnitId) -> np.ndarray:
        return np.array(self._sorting.get_unit_spike_train(unit_id=unit_id))