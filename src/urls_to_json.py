# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 13:49:43 2018

@author: jsaracen
"""

import json
outfile = 'url_paths.json'
urls = {"djfmp_url": "https://pasta.lternet.edu/package/data/eml/edi/244/2/1c7e55b76e6455b3093f6a66cb3ba38c",
        "ybp_salmon_url": "http://pasta.lternet.edu/package/data/eml/edi/233/1/8b5ba731b0956bf719d3abaacdda5c70",
        "emp_phyto_url" : "https://emp.baydeltalive.com/assets/06942155460a79991fdf1b57f641b1b4/text/csv/Phytoplankton_Algal_Type_Data_1975_-2016.csv"
        }

with open(outfile, 'w') as fp:
    json.dump(urls, fp)
