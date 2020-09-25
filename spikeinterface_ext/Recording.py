from spikeinterface_ext.types import ChannelId, ChannelIndex, Order, SamplingFrequencyHz
import spikeextractors as se
from typing import List, Union
from .RecordingSegment import SampleIndex, RecordingSegment, RecordingSegmentFromExtractor
# todo: rename RecordingSegment -> SignalSegment
# todo: also allow channel_index input



class Recording(object):
    def __init__(self, sampling_frequency: SamplingFrequencyHz, channel_ids: List[ChannelId]):
        self._signal_segments: List[RecordingSegment] = []
        self._channel_ids = channel_ids

    def add_recording_segment(self, signal_segment: RecordingSegment):
        # todo: check channel count and sampling frequency
        self._signal_segments.append(signal_segment)

    def get_channel_ids(self):
        return self._channel_ids
    
    def get_num_channels(self):
        return len(self.get_channel_ids())

    def get_num_segments(self):
        return len(self._signal_segments)
    
    def _check_segment_index(self, segment_index: Union[int, None]) -> int:
        if segment_index is None:
            if self.get_num_segments() == 1:
                return 0
            else:
                raise ValueError()
        else:
            return segment_index

    def get_num_samples(self, segment_index: Union[int, None]):
        segment_index = self._check_segment_index(segment_index)
        return self._signal_segments[segment_index].get_num_samples()

    def get_traces(self,
            segment_index: Union[int, None]=None,
            start: Union[SampleIndex, None]=None,
            end: Union[SampleIndex, None]=None,
            channel_ids: Union[List[ChannelId], None]=None,
            order: Order = Order.K
        ):
        segment_index = self._check_segment_index(segment_index)
        channel_indices = [ChannelIndex(self._channel_ids.index(id)) for id in channel_ids]
        S = self._signal_segments[segment_index]
        return S.get_traces(start=start, end=end, channel_indices=channel_indices, order=order)

def recording_from_extractor(recording_extractor: se.RecordingExtractor):
    R = Recording(
            sampling_frequency=recording_extractor.get_sampling_frequency(),
            channel_ids=recording_extractor.get_channel_ids()
        )
    B = RecordingSegmentFromExtractor(recording=recording_extractor)
    R.add_recording_segment(B)
    return R

def SubRecording(Recording):
    pass
