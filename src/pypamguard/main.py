from . import *
from .logger import logger, Verbosity
from pypamguard.core.filters import Filters, DateFilter, WhitelistFilter
import datetime

if __name__ == "__main__":

    pg_filters = Filters()

    d1 = datetime.datetime.fromtimestamp(1504477746918 / 1000, tz = datetime.UTC)
    d2 = datetime.datetime.fromtimestamp(1504477758412 / 1000, tz = datetime.UTC)

    pg_filters = Filters({
        'uidlist': WhitelistFilter([119000001])
        # 'daterange': DateFilter(d1, d2),
        # 'uidlist': WhitelistFilter([5001713, 5002388, 5003215, 5008381])
    })


    with open("test1.json", "w") as f:
        # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/ClickDetector/ClickDetector_v4_test1.pgdf", verbosity=Verbosity.DEBUG, output=f, filters=pg_filters)
        # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/test.pgdf", verbosity=Verbosity.INFO)
        
        pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/RW_Edge_Detector_Right_Whale_Edge_Detector_Edges_20090328_000000.pgdf", output=f)
        
        #pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/Clip_Generator_Clip_generator_Clips_20170903_222955.pgdf", verbosity=Verbosity.DEBUG)
        # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/WhistlesMoans_Whistle_and_Moan_Detector_Contours_20240806_121502.pgdf", output=f, verbosity=Verbosity.INFO)
        print(pgdf)
        print(pgdf.data[0].peak_amp, type(pgdf.data[0].peak_amp))