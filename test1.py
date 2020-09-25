from spikeinterface_ext.Sorting import sorting_from_extractor
from spikeinterface_ext.RecordingSegment import RecordingSegment, RecordingSegmentFromExtractor
from spikeinterface_ext.types import ChannelId, SampleIndex, SamplingFrequencyHz, UnitId
import spikeextractors as se
import numpy as np
from spikeinterface_ext import NumpyRecordingSegment
from spikeinterface_ext.Recording import Recording, recording_from_extractor

# X = np.random.normal(0, 1, (1000, 4))

# B = NumpyRecordingSegment(X, sampling_frequency=SamplingFrequencyHz(30000.))

# print(B.get_sampling_frequency())
# print(B.get_num_samples())
# print(B.get_num_channels())
# print(B.get_traces(start=SampleIndex(0), end=SampleIndex(3)))


recording, sorting = se.example_datasets.toy_example()

# B2 = RecordingSegmentFromExtractor(recording=recording)
# print(B2.get_sampling_frequency())
# print(B2.get_num_samples())
# print(B2.get_num_channels())
# print(B2.get_traces(start=SampleIndex(0), end=SampleIndex(3)))

R = recording_from_extractor(recording)

print(R.get_channel_ids())
print(R.get_num_samples(segment_index=0))
print(R.get_traces(segment_index=0, channel_ids=[ChannelId(1)], start=SampleIndex(0), end=SampleIndex(5)))

S = sorting_from_extractor(sorting)
print(S.get_unit_ids())
print(S.get_unit_spike_train(unit_id=UnitId(1))[:20])