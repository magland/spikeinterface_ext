from spikeinterface_ext.types import ChannelIndex, Order, SampleIndex, SamplingFrequencyHz
from typing import List, Union
import numpy as np
import spikeextractors as se

class RecordingSegment(object):
    """
    Abstract class representing a multichannel timeseries, or block of raw ephys traces
    """

    def __init__(self):
        pass

    def get_num_samples(self) -> SampleIndex:
        """Returns the number of samples in this signal block

        Returns:
            SampleIndex: Number of samples in the signal block
        """
        raise NotImplementedError

    def get_num_channels(self) -> ChannelIndex:
        """Returns the number of channels in this signal block

        Returns:
            ChannelIndex: Number of channels in the signal block
        """
        raise NotImplementedError

    def get_sampling_frequency(self) -> SamplingFrequencyHz:
        """Returns the sampling frequency in Hz for this signal block

        Returns:
            SamplingFrequencyHz: The sampling frequency for this signal block
        """
        raise NotImplementedError

    def get_traces(self,
                   start: Union[SampleIndex, None] = None,
                   end: Union[SampleIndex, None] = None,
                   channel_indices: Union[List[ChannelIndex], None] = None,
                   order: Order = Order.K
                   ) -> np.ndarray:
        """Returns the raw traces, optionally for a subset of samples and/or channels

        Args:
            start (Union[SampleIndex, None], optional): start sample index, or zero if None. Defaults to None.
            end (Union[SampleIndex, None], optional): end_sample, or num. samples if None. Defaults to None.
            channel_indices (Union[List[ChannelIndex], None], optional): indices of channels to return, or all channels if None. Defaults to None.
            order (Order, optional): The memory order of the returned array. Use Order.C for C order, Order.F for Fortran order, or Order.K to keep the order of the underlying data. Defaults to Order.K.

        Returns:
            np.ndarray: Array of traces, num_samples x num_channels
        """
        raise NotImplementedError


class SubRecordingSegment(RecordingSegment):
    """A sub-array of a signal block, restricting to a time chunk and/or subset of channels
    """

    def __init__(self,
                 parent_block: RecordingSegment,
                 start: Union[SampleIndex, None] = None,
                 end: Union[SampleIndex, None] = None,
                 channel_indices: Union[List[ChannelIndex], None] = None
                ):
        """SubRecordingSegment constructor

        Args:
            parent_block: The parent signal block
            start (Union[SampleIndex, None], optional): start sample index, or zero if None. Defaults to None.
            end (Union[SampleIndex, None], optional): end_sample, or num. samples if None. Defaults to None.
            channel_indices (Union[List[ChannelIndex], None], optional): indices of channels to represent, or all channels if None. Defaults to None.
        """
        super().__init__()
        self._parent_block = parent_block
        if start is None:
            start = SampleIndex(0)
        if end is None:
            end = parent_block.get_num_samples()
        self._start = start
        self._end = end
        self._channel_indices = channel_indices

    def get_num_samples(self) -> SampleIndex:
        return self._end - self._start

    def get_num_channels(self) -> ChannelIndex:
        if self._channel_indices is None:
            return self._parent_block.get_num_channels()
        else:
            return ChannelIndex(len(self._channel_indices))

    def get_sampling_frequency(self) -> SamplingFrequencyHz:
        return self._parent_block.get_sampling_frequency()

    def get_traces(self,
                   start: Union[SampleIndex, None] = None,
                   end: Union[SampleIndex, None] = None,
                   channel_indices: Union[List[ChannelIndex], None] = None,
                   order: Order = Order.K
                   ) -> np.ndarray:
        if self._channel_indices is None:
            channel_indices_2 = self._channel_indices
        else:
            channel_indices_2 = [self._channel_indices[ii] for ii in channel_indices]
        return self._parent_block.get_traces(
            start=self._start,
            end=self._end,
            channel_indices=channel_indices_2,
            order=order
        )

class NumpyRecordingSegment(RecordingSegment):
    """In-memory implementation of RecordingSegment
    """

    def __init__(self, X: np.ndarray, sampling_frequency: SamplingFrequencyHz):
        """NumpyRecordingSegment constructor

        Args:
            X (np.ndarray): A 2-d numpy array, num_samples x num_channels
            sampling_frequency (SamplingFrequencyHz): Sampling frequency in Hz
        """
        super().__init__()
        assert X.ndim == 2, 'Array must have 2 dimensions'
        self._X = X
        self._num_channels = X.shape[1]
        self._num_samples = X.shape[0]
        self._sampling_frequency = sampling_frequency

    def get_num_samples(self) -> SampleIndex:
        return self._num_samples

    def get_num_channels(self) -> ChannelIndex:
        return self._num_channels

    def get_sampling_frequency(self) -> SamplingFrequencyHz:
        return self._sampling_frequency

    def get_traces(self,
                   start: Union[SampleIndex, None] = None,
                   end: Union[SampleIndex, None] = None,
                   channel_indices: Union[List[ChannelIndex], None] = None,
                   order: Order = Order.K
                   ) -> np.ndarray:
        if start is None:
            start = SampleIndex(0)
        if end is None:
            end = SampleIndex(self._num_samples)
        assert start >= 0, 'start sample index out of range'
        assert end <= self._num_samples, 'end sample index out of range'
        assert start < end, 'start sample must be less than end sample'
        if channel_indices is None:
            ret: np.ndarray = self._X[start:end, :]
        else:
            ret: np.ndarray = self._X[start:end, :][:, channel_indices]
        if order is Order.C:
            return ret.astype(dtype=ret.dtype, order='C', copy=False)
        elif order is Order.F:
            return ret.astype(dtype=ret.dtype, order='F', copy=False)
        elif order is Order.K:
            return ret.astype(dtype=ret.dtype, order='K', copy=False)

class RecordingSegmentFromExtractor(RecordingSegment):
    """Signal block formed from RecordingExtractor
    """

    def __init__(self, recording: se.RecordingExtractor):
        """RecordingSegmentFromExtractor constructor

        Args:
            recording(): ...
        """
        super().__init__()
        self._recording = recording

    def get_num_samples(self) -> SampleIndex:
        return self._recording.get_num_frames()

    def get_num_channels(self) -> ChannelIndex:
        return self._recording.get_num_channels()

    def get_sampling_frequency(self) -> SamplingFrequencyHz:
        return self._recording.get_sampling_frequency()

    def get_traces(self,
                   start: Union[SampleIndex, None] = None,
                   end: Union[SampleIndex, None] = None,
                   channel_indices: Union[List[ChannelIndex], None] = None,
                   order: Order = Order.K
                   ) -> np.ndarray:
        all_channel_ids = self._recording.get_channel_ids()
        if channel_indices is not None:
            channel_ids = [all_channel_ids[ii] for ii in channel_indices]
        else:
            channel_ids = None
        traces: np.ndarray = self._recording.get_traces(
            channel_ids=channel_ids,
            start_frame=int(start) if start is not None else None,
            end_frame=int(end) if end is not None else None
        ).T
        if order is Order.C:
            return traces.astype(dtype=traces.dtype, order='C', copy=False)
        elif order is Order.F:
            return traces.astype(dtype=traces.dtype, order='F', copy=False)
        elif order is Order.K:
            return traces.astype(dtype=traces.dtype, order='K', copy=False)