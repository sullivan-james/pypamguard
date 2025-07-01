from pypamguard.standard import StandardModule
from ..core.readers import *

class RWEdgeDetector(StandardModule):

    def __init__(self, file_header, module_header, filters):
        super().__init__(file_header, module_header, filters)

        self.sound_type: int = None
        self.signal: float = None
        self.noise: float = None
        self.n_slices: int = None

        self.slice_list: np.ndarray = None
        self.low_freq: np.ndarray = None
        self.peak_freq: np.ndarray = None
        self.high_freq: np.ndarray = None
        self.peak_amp: np.ndarray = None
    
    def process(self, data, chunk_info):
        super().process(data, chunk_info)

        self.sound_type = NumericalBinaryReader(INTS.SHORT, var_name='sound_type').process(data)
        self.signal = NumericalBinaryReader(FLOATS.FLOAT, var_name='signal').process(data)
        self.noise = NumericalBinaryReader(FLOATS.FLOAT, var_name='noise').process(data)
        NumericalBinaryReader(INTS.INT).process(data)
        self.n_slices = NumericalBinaryReader(INTS.SHORT, var_name='n_slices').process(data)

        self.slice_list = np.zeros(self.n_slices, dtype=np.int16)
        self.low_freq = np.zeros(self.n_slices, dtype=np.int16)
        self.peak_freq = np.zeros(self.n_slices, dtype=np.int16)
        self.high_freq = np.zeros(self.n_slices, dtype=np.int16)
        self.peak_amp = np.zeros(self.n_slices, dtype=np.float32)

        for i in range(self.n_slices):
            self.slice_list[i] = NumericalBinaryReader(INTS.SHORT, var_name='slice_list').process(data)
            self.low_freq[i] = NumericalBinaryReader(INTS.SHORT, var_name='low_freq').process(data)
            self.peak_freq[i] = NumericalBinaryReader(INTS.SHORT, var_name='peak_freq').process(data)
            self.high_freq[i] = NumericalBinaryReader(INTS.SHORT, var_name='high_freq').process(data)
            self.peak_amp[i] = NumericalBinaryReader(FLOATS.FLOAT, var_name='peak_amp').process(data)
        
