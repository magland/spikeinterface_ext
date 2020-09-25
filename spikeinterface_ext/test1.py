from typing import Union
from spikeinterface_ext.SignalBlock import SampleIndex, SignalBlock, ChannelIndex

def test1(a: SampleIndex):
    print(a + 1)

x = SampleIndex(5)

test1(x - 1)
test1(3)