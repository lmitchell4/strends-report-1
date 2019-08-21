# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 13:49:43 2018
script to write a json file of data repository urls
@author: jsaracen
"""

import json
import os
from pathlib import Path


def main():
    SOURCE_DIR = str(Path().resolve()) #os.curdir
    CONFIG_DIR = r"config"
#TODO:make json output pretty
    OUTFILENAME = os.path.join(SOURCE_DIR, CONFIG_DIR, 'data_portal_urls.json')
    #EDI
    EDI_PORTAL_DOWNLOAD_ROOT = "https://pasta.lternet.edu/package/data/eml/edi/"
    DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL = EDI_PORTAL_DOWNLOAD_ROOT + "244/2/1c7e55b76e6455b3093f6a66cb3ba38c"
    YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL = EDI_PORTAL_DOWNLOAD_ROOT + "233/1/8b5ba731b0956bf719d3abaacdda5c70"
    #EMP
    EMP_BAY_DELTA_LIVE_PORTAL_DOWNLOAD_ROOT = "https://emp.baydeltalive.com/assets/06942155460a79991fdf1b57f641b1b4/text/csv/"
    EMP_PHYTOPLANKTON_URL = EMP_BAY_DELTA_LIVE_PORTAL_DOWNLOAD_ROOT + "Phytoplankton_Algal_Type_Data_1975_-2016.csv"
    #CDFW
    CDFW_FTP_ADDR = 'ftp.dfg.ca.gov'
    CDFW_FMWT_URL = 'http://www.dfg.ca.gov/delta/data/fmwt/indices.asp'
    #USFWS_REDBLUFF_SALMON_URL - sacpass url has year in it to specify the year which can be 2004 or later. Can be specified using example str.format(2014)
    USFWS_REDBLUFF_SALMON_URL = 'http://www.cbr.washington.edu/sacramento/data/php/rpt/redbluff_daily.php?outputFormat=csv&year={year}&biweekly=other&wtemp=default'
    portal_urls = {
        "DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL":
        DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL,
        "YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL":
        YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL,
        "EMP_PHYTOPLANKTON_URL":
        EMP_PHYTOPLANKTON_URL,
        "CDFW_FTP_ADDR":
        CDFW_FTP_ADDR,
        "CDFW_FMWT_URL":
        CDFW_FMWT_URL,
        "USFWS_REDBLUFF_SALMON_URL":
        USFWS_REDBLUFF_SALMON_URL}
    with open(OUTFILENAME, 'w') as fp:
        json.dump(portal_urls, fp, indent = 4, sort_keys=True)

    return


#if __name__ == "__main__":
#    sys.exit(main())
main()