from pypamguard.generics import GenericModuleHeader
from pypamguard.core.readers import *

class StandardModuleHeader(GenericModuleHeader):
    
    def __init__(self, file_header, *args, **kwargs):
        super().__init__(file_header, *args, **kwargs)

        self.length: int = None
        self.identifier: int = None
        self.version: str = None
        self.binary_length: int = None

    def process(self, data, chunk_info):
        self.length = chunk_info.length
        self.identifier = chunk_info.identifier
        self.version: int = NumericalBinaryReader(INTS.INT, var_name='version').process(data)
        self.binary_length: int = NumericalBinaryReader(INTS.INT, var_name='binary_length').process(data)
