#!/usr/bin/env python

from __future__ import print_function # adds compatibility to python 2
from __future__ import unicode_literals

import sys
import logging
import web
import json
import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import xlrd
import os
import importlib

if sys.version_info < (3, 0):
    # python 2 compatible function
    reload(sys)
else:
    # python 3 compatible function
    importlib.reload(sys) 

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',filename='./logs/CovidPlot.log',level=logging.INFO)
web.config.debug = False

def plotBarChart(country,chartType):
    logging.info("[Country] " + country)
    df_corona = pd.read_csv('../data/corona_Tracker_09-24-2020.csv')
    df_corona.drop(['FIPS','Admin2', 'Last_Update','Province_State','Lat', 'Long_', 'Combined_Key', 'Confirmed','Incidence_Rate','Case-Fatality_Ratio'], axis=1, inplace=True)
    df_corona.set_index('Country_Region', inplace=True)
    df_country = df_corona.loc[country]
    df_country.plot(kind=chartType, figsize=(7, 6))
    plt.xlabel('Category') # add to x-label to the plot
    plt.xticks(rotation=None)
    plt.ylabel('Number of Patients') # add y-label to the plot
    plt.title(country + ' Corona Status') # add title to the plot
    #plt.legend()
    fileName =  country +'_Corona_'+chartType+'_Chart.png'
    logging.info("[FileName] "+ fileName)
    plt.savefig('images/'+fileName)
    plt.close();
    del df_corona
    del df_country
    del country
    return fileName

urls = ("/", "Index", "/(.*)" ,"ImageDisplay")
        
render = web.template.frender('./static/plot.html')

class Index(object):
    # In the browser, this displays "Index", but also causes the error on the server side.
    def GET(self):
        return render()


class ImageDisplay(object):
    def GET(self,country):
        if (country == 'favicon.ico'):
            pass
        else:
            user_data = web.input(ctype=None)
            
            if user_data.ctype is None:
                logging.info("No params passed")
                chartType="bar"  #default type
            else:
                logging.info("[ChartType] " + user_data.ctype)
                chartType = user_data.ctype
            
            logging.info("[Server] " + country)
            logging.info("[ChartType] " + chartType)
            fileName= plotBarChart(country,chartType)
            imageBinary = open("./images/"+fileName,'rb').read()
            del fileName
            del country
            return imageBinary
            

if __name__ == "__main__":
    logging.info("[Server] Starting server.")
    app = web.application(urls, globals())
    app.run()
