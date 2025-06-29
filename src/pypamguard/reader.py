import struct

from . import constants
from .pamfile import PAMFile

def pamread(filename, order: str = "network", buffering: int | None = constants.DEFAULT_BUFFER_SIZE) -> PAMFile:
    """
    Read a binary PAMGuard data file into a PAMFile object
    :param filename: absolute or relative path to the .pgdt file to read
    :param order: endianess of data (defaults to 'network')
    :param buffering: number of bytes to buffer
    
    """
    if order not in constants.ORDER_MODIFIERS:
        raise ValueError(f"order must be one of: {', '.join(constants.ORDER_MODIFIERS.keys())} (got {str(order)}).")
    if buffering and type(buffering) != int:
        raise ValueError(f"buffering must be of type int or None (got {type(buffering)}).")
    if not filename or type(filename) != str:
        raise ValueError(f"filename must be of type str (got {type(filename)}).")

    data = open(filename, "rb", buffering=buffering)
    pamfile = PAMFile(filename=filename, data=data, order=order)

    loc = data.tell()
    for header in constants.HEADER_FORMAT:
        value = struct.unpack(constants.ORDER_MODIFIERS[order] + header["dtype"], data.read(struct.calcsize(header["dtype"])))
        print(value[0])
    
    return pamfile