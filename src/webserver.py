#!/mnt/LinuxHome/tanmay/MyLearning/learn_matplotlib/bin/python

from __future__ import print_function # adds compatibility to python 2
from __future__ import unicode_literals

import sys
reload(sys)
import logging
logging.basicConfig(level=logging.INFO)
import web
import json
import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library
import matplotlib as mpl
import matplotlib.pyplot as plt
import xlrd
import os


def loadCoronaDataFile(country):
    print("Country to be loaded from datafile: " + country)
    df_corona = pd.read_csv('../data/corona_Tracker_30-04-2020.csv')
    df_corona.drop(['FIPS','Admin2', 'Last_Update','Province_State','Lat', 'Long_', 'Combined_Key', 'Confirmed'], axis=1, inplace=True)
    df_corona.set_index('Country_Region', inplace=True)
    df_country = df_corona.loc[country]
    return df_country


def plotBarChart(df_country,countryName):
    df_country.plot(kind='bar', figsize=(10, 6))
    plt.xlabel('Year') # add to x-label to the plot
    plt.ylabel('Number of Patients') # add y-label to the plot
    plt.title(countryName + ' Corona Status') # add title to the plot
    plt.legend()
    fileName =  'Corona_BarChart.png'
    print("FIleName of Saved file"+ fileName)
    #os.remove('images/'+fileName)
    plt.savefig('images/'+fileName)



urls = ("/", "Index", "/(.*)" ,"ImageDisplay")
        

render = web.template.frender('tutorial.html')
#app = web.application(urls, globals())
#my_form = web.form.Form(web.form.Textbox('', class_='textfield', id='textfield'),)


class Index(object):
    # In the browser, this displays "Index", but also causes the error on the server side.
    def GET(self):
        #form = my_form()
        return render()

    # Doesn't do anything, but causes the error
    def POST(self):
        data = web.data()
        web.header('Content-Type', 'application/text')
        #result  = data;
        result = json.loads(data)
        logging.info("[Server] Index " + json.dumps(result))
        country =result["message"] 
        logging.info("[Server] Value " + country)
        df_country = loadCoronaDataFile(country)
        print ("Country Selected" + country)
        plotBarChart(df_country, country)
        fileName= "Corona_BarChart.png"
        print ("Filename to be retured" + fileName)
        return render()


class ImageDisplay(object):
    def GET(self,fileName):
        if(fileName is None):
            fileName='Corona_BarChart.png'
        imageBinary = open("./images/"+fileName,'rb').read()
        return imageBinary


if __name__ == "__main__":
    logging.info("[Server] Starting server.")
    app = web.application(urls, globals())
    app.run()
