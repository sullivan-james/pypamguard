import datetime

from pypamguard.generics import GenericModule, GenericModuleFooter
from .stdmodulefooter import StandardModuleFooter
from .stdmoduleheader import StandardModuleHeader
from pypamguard.core.readers import *

DATA_FLAG_FIELDS = [
    "TIMEMILLISECONDS",
    "TIMENANOSECONDS",
    "CHANNELMAP",
    "UID",
    "STARTSAMPLE",
    "SAMPLEDURATION",
    "FREQUENCYLIMITS",
    "MILLISDURATION",
    "TIMEDELAYSECONDS",
    "HASBINARYANNOTATIONS",
    "HASSEQUENCEMAP",
    "HASNOISE",
    "HASSIGNAL",
    "HASSIGNALEXCESS"
]

class StandardModule(GenericModule):

    _footer = StandardModuleFooter
    _header = StandardModuleHeader

    def __init__(self, file_header, module_header, filters, *args, **kwargs):
        super().__init__(file_header, module_header, filters, *args, **kwargs)
        self.millis: int = None
        self.date: datetime.datetime = None
        self.flag_bitmap: Bitmap = None
        self.time_ns: int = None
        self.channel_map: Bitmap = None
        self.uid: int = None
        self.start_sample: int = None
        self.sample_duration: int = None
        self.freq_limits: float = None
        self.millis_duration: float = None
        self.time_delays: list[float] = None
        self.sequence_map: float = None
        self.noise: float = None
        self.signal: float = None
        self.signal_excess: float = None

    def process(self, data, chunk_info):

        self.millis = NumericalBinaryReader(INTS.LONG, var_name='millis').process(data)
        
        self.date = datetime.datetime.fromtimestamp(self.millis / 1000, datetime.UTC)
        self._filters.filter('daterange', self.date)

        if self._file_header.file_format >= 3:
            self.flag_bitmap = BitmapBinaryReader(INTS.SHORT, DATA_FLAG_FIELDS, var_name='flag_bitmap').process(data)
        else: return # TODO: this should change. Waiting on issue #2 to be resolved
        
        set_flags = self.flag_bitmap.get_set_bits()
        
        if self._file_header.file_format == 2 or "TIMENANOSECONDS" in set_flags:
            self.time_ns = NumericalBinaryReader(INTS.LONG, var_name='time_ns').process(data)
        
        if self._file_header.file_format == 2 or "CHANNELMAP" in set_flags:
            self.channel_map = BitmapBinaryReader(INTS.INT, var_name='channel_map').process(data)
        
        if "UID" in set_flags:
            self.uid = NumericalBinaryReader(INTS.LONG, var_name='uid').process(data)
            self._filters.filter('uidrange', self.uid)
            self._filters.filter('uidlist', self.uid)
        
        if "STARTSAMPLE" in set_flags:
            self.start_sample = NumericalBinaryReader(INTS.LONG, var_name='start_sample').process(data)
        
        if "SAMPLEDURATION" in set_flags:
            self.sample_duration = NumericalBinaryReader(INTS.INT, var_name='sample_duration').process(data)
        
        if "FREQUENCYLIMITS" in set_flags:
            self.freq_limits = [
                NumericalBinaryReader(FLOATS.FLOAT).process(data), NumericalBinaryReader(FLOATS.FLOAT, var_name='freq_limits').process(data)
            ]

        if "MILLISDURATION" in set_flags:
            self.millis_duration = NumericalBinaryReader(FLOATS.FLOAT, var_name='millis_duration').process(data)
        
        if "TIMEDELAYSECONDS" in set_flags:
            self.time_delays = []
            num_time_delays = NumericalBinaryReader(INTS.SHORT, var_name='num_time_delays').process(data)
            for i in range(num_time_delays):
                self.time_delays.append(NumericalBinaryReader(FLOATS.FLOAT, var_name='time_delays').process(data))

        if "HASSEQUENCEMAP" in set_flags:
            self.sequence_map = NumericalBinaryReader(INTS.INT, var_name='sequence_map').process(data)

        if "HASNOISE" in set_flags:
            self.noise = NumericalBinaryReader(FLOATS.FLOAT, var_name='noise').process(data)

        if "HASSIGNAL" in set_flags:
            self.signal = NumericalBinaryReader(FLOATS.FLOAT, var_name='signal').process(data)

        if "HASSIGNALEXCESS" in set_flags:
            self.signal_excess = NumericalBinaryReader(FLOATS.FLOAT, var_name='signal_excess').process(data)

        # NOT COMPLETED YET
        # if "HASBINARYANNOTATIONS" in set_flags:
        #     annotations_length = NumericalBinaryReader(INTS.SHORT).process(data)
        #     n_annotations = NumericalBinaryReader(INTS.SHORT).process(data)
        #     for i in range(n_annotations):
        #         annotation_length = NumericalBinaryReader(INTS.SHORT).process(data) - INTS.SHORT.value.size
        #         annotation_id = StringType().process(data)
        #         annotation_version = NumericalBinaryReader(INTS.SHORT).process(data)

        #         if annotation_id == "Beer":
        #             annotations.read_beam_former_annotation(self, data)
                
        #         elif annotation_id == "Bearing":
        #             annotations.read_bearing_annotation(self, data, annotation_version)
        # else:
        #     self.annotations = []

        self.annotations = []