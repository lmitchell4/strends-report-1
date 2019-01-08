# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 13:49:43 2018
script to write a json file of data repository urls
@author: jsaracen
"""

import json
import sys


def main():
    OUTFILENAME = 'data_filenames.json'
#    DATA_ROOT = "data"
#    FLOW_DIR = "FLOW"    
#    FTP_ZOOPLANKTON_DIR = "IEP_Zooplankton"
#    FTP_DS_DIR = "Delta Smelt"
#    FTP_LS_DIR = "BayStudy/CatchMatrices"
#    BAYSTUDY_DIR = "BayStudy"

    FLOW_INDEX_FILENAME = "dayflowCalculations2017.csv"
    EMP_PHYTOPLANKTON_FILENAME = "emp_phytoplankton.csv"
    ZOOPLANKTON_CBMATRIX_FILENAME = "1972-2017CBMatrix.xlsx"
    ZOOPLANKTON_MYSID_FILENAME = "1972-2017MysidMatrix.xlsx"
    ZOOPLANKTON_PUMP_FILENAME = "1972-2017PumpMatrix.xlsx"
    LS_SMELT_FILENAME = "Bay Study_MWT_1980-2017_FishMatrix.xlsx"
    LS_SMELT_FILENAME_ZIP = "Bay Study_FishCatchMatrices_1980-2017.zip"
    SLS_FILENAME = "SLS.mdb"
    SKT_FILENAME = "SKT.mdb"
    YBP_SALMON_FILENAME = "ybp_salmon.csv"  
    
    filenames = {"FLOW_INDEX_FILENAME":FLOW_INDEX_FILENAME,
                 "EMP_PHYTOPLANKTON_FILENAME":EMP_PHYTOPLANKTON_FILENAME,
                 "ZOOPLANKTON_MYSID_FILENAME":ZOOPLANKTON_MYSID_FILENAME,
                 "ZOOPLANKTON_PUMP_FILENAME":ZOOPLANKTON_PUMP_FILENAME,
                 "ZOOPLANKTON_CBMATRIX_FILENAME":ZOOPLANKTON_CBMATRIX_FILENAME,
                 "LS_SMELT_FILENAME":LS_SMELT_FILENAME,
                 "LS_SMELT_FILENAME_ZIP":LS_SMELT_FILENAME_ZIP,
                 "SLS_FILENAME":SLS_FILENAME,
                 "SKT_FILENAME":SKT_FILENAME,
                 "YBP_SALMON_FILENAME":YBP_SALMON_FILENAME,
    }

    with open(OUTFILENAME, 'w') as fp:
        json.dump(filenames, fp)

    return


if __name__ == "__main__":
    sys.exit(main())
