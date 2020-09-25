from spikeinterface_ext.types import UnitId
from .Recording import Recording
from .Sorting import Sorting

class SnippetEngine(object):
    def __init__(self, recording: Recording, sorting: Sorting):
      self._recording = recording
      self._sorting = sorting
    def set_cache(self):
        # todo
        pass
    # think about this
    
