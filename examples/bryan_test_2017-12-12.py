# -*- coding: utf-8 -*-
"""
Created on Thu Dec 07 21:12:15 2017

@author: bfh3admin
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
sys.path.insert(0, 'D:/Python code/Env_is_Everything_11_20_17/')
from chgpt_detect_ft_v9C import *
#from chgpt_detect_ft_v9C_v2 import *
#import chgpt_detect_ft_v9C
import time
from datetime import datetime as dt
from datetime import timedelta
import datetime
import pandas as pd
import numpy as np
import dateutil.parser
import pymssql
import queue
import threading

# main package
import osisoftpy

#silence the certificate warnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#define clustering time frame for alarms and alerts in hours.  clusting time would be the time between two alarms (or two alerts)
#that they would still be considered a cluster.
cluster_hours = 30


# initialize sql connection
####################################################################################################################

GCSSdevSQLserver = 'gcssdbsqldev01'
username = 'PGE\BFH3'
pw = 'password'
#dbtest ='RegFailure'

## instance a python db connection object- same form as psycopg2/python-mysql drivers also
#conn = pymssql.connect(server="gcssdbsqldev01", user="PGE\BFH3",password="")
conn = pymssql.connect(server=GCSSdevSQLserver, user=username, password=pw)
##
stmt = "SELECT * FROM [RegFailure].[dbo].[Alerts] WHERE [End Time] IS NULL"
# Excute Query here
alerts = pd.read_sql(stmt,conn)







# make connection to pi server
############################################################################################################################

#'''
#PGE Pi webapi:
#use dev and qa for testing
#'''
qa='https://piudniisqa02.utility.pge.com/piwebapi/'
dev='https://piudniisdev01.utility.pge.com/piwebapi/'
#prod='https://piudnpiwebapi/piwebapi/'
prod='https://piudniisprd02.utility.pge.com/piwebapi/'

path = 'D:/Python code/Env_is_Everything_11_20_17/'

#logfilepath = str(outputpath + 'log.txt')
############################################################## reenable these 2 lines for logfile
#logfile = open('D:/Python code/Env_is_osisoftpy_2.2_9_20_17/connexmple_9_20_17_output/log.txt','a')
#logfile.write(str(datetime.datetime.now()))
###################################################################
#logfile.close()


#use this section only if using basic authentication#
#'''
#lanid= raw_input('lanid: ')
#pwd= getpass.getpass() #mask password

#'''


#connection confirmation#
t='error'
def cnnt_message():
    try:
        #osisoftpy.webapi(qa,authtype='basic', username=lanid,password=pwd)
        osisoftpy.webapi(dev, authtype='kerberos')
    except Exception:  #catch any general exception#
        return t


#'''
#While server is down, try again (max='recnnt_max')
#time delay bewteen each hit: 'delay'
#
#'''
delay= 60#raw_input('Preferred deplay time: ')
recnnt_max= 3#raw_input('Max Reconnection: ')
i=cnnt_message()
k=1
while i=='error': #try 'recnnt_max' times only#
    #print ('Try Connection:',dt.now().strftime("%Y-%m-%d %H:%M:%S"),k)
    k+=1
    i=cnnt_message()
    time.sleep(float(delay))
    if k==float(recnnt_max):
        #print ("Connection Failed",k)
        break
else:
    webapi = osisoftpy.webapi(dev, authtype='kerberos')
    ##################################################################################reenable these 1 lines for logfile
    #logfile.write('Connection Successful'+ str(dt.now().strftime("%Y-%m-%d %H:%M:%S"))+str(k))
    print('Connection Successful'+ str(dt.now().strftime("%Y-%m-%d %H:%M:%S"))+str(k))
    #additional analysis code here#




# create function for getting value updates
############################################################################################################################
df = pd.DataFrame(columns=['tag name','DateTime', 'Pressure'])
#dfcopy = pd.DataFrame(columns=['tag name','DateTime', 'Pressure'])
#df = df.append({'tag':1, 'time':2, 'value':3}, ignore_index=True)

def callback_current(sender):
    global df
    #global dfcopy

    if isinstance(sender.current_value.value, dict)== False:
        value = sender.current_value.value
    elif sender.current_value.value.get('IsSystem') == False:

        value = str(sender.current_value.value.get('Value'))
    else:
        value = str(sender.current_value.value.get('Name'))
    #str(dateutil.parser.parse(str(sender.current_value.timestamp)).astimezone(PST))[:19]
    #df = df.append({'tag name':sender.name, 'DateTime':str(dateutil.parser.parse(str(sender.current_value.timestamp)).astimezone(PST))[:19], 'Pressure':sender.current_value.value}, ignore_index=True)
    df = df.append({'tag name':sender.name, 'DateTime':str(dateutil.parser.parse(str(sender.current_value.timestamp)))[:19], 'Pressure':value}, ignore_index=True)
    #dfcopy = dfcopy.append({'tag name':sender.name, 'DateTime':str(dateutil.parser.parse(str(sender.current_value.timestamp)))[:19], 'Pressure':sender.current_value.value}, ignore_index=True)








# create class for point operations
############################################################################################################################


class PointMonitoring:
    def __init__(self, pointname):

        # make the global variables visible for overal point list, the value update dataframe,
        global points
        global df
        global qu
        global alerts
        global cluster_hours
        global stmt
        global conn

        # initialize time trackers for this tag
        self.timefunction = dt.now()
        self.timesincelastupdate = dt.now()
        self.numberofupdates = 0

        self.pointname = pointname

        # use tagname to get point definitions from the pi server, initiate all tables, pull 2 weeks of data, and run initial algorithm builder
        # build string for point query, get point definition from pi server
        self.PointQueryString = ''
        self.PointQueryString += ('name: ' + self.pointname)

        self.points = webapi.points(query=self.PointQueryString, scope='pi:PIUDNAPPDEV01')

        # check that point exists and that there is only one
        if len(self.points) <> 1:
            print(self.pointname + ' returned this many points: ' + str(len(self.points)))
        else:
            print('started else area of initialization for ' + self.pointname)
            points.append(self.points[0])

            # get two weeks of data and initialize the algorithm for this point

            self.name = []
            self.timestamp = []
            self.value = []


            # pull values from pi for this point
            self.recorded_values = self.points[0].recorded(starttime='t-14d', endtime='*', maxcount=100000)
            #len(recorded_values)

            # sign this point up for updates after pulling the initial data
            webapi.subscribe(self.points, 'current', callback=callback_current)

            print('started initialize area for ' + self.pointname)
            #v = recorded_values[0]
            for self.v in self.recorded_values:

                self.name.append(self.pointname)

                #timestamp.append(str(dateutil.parser.parse(str(v.timestamp)).astimezone(PST))[:19])
                self.timestamp.append(str(dateutil.parser.parse(str(self.v.timestamp)))[:19])

                if isinstance(self.v.value, dict)== False:
                    self.value.append(self.v.value)
                elif self.v.value.get('IsSystem') == False:
                    self.value.append(str(self.v.value.get('Value')))
                else:
                    self.value.append(str(self.v.value.get('Name')))

            self.df3 = pd.DataFrame(np.column_stack([self.name, self.timestamp, self.value]),
                                    columns = ['tag name','DateTime', 'Pressure'])

            self.df3.drop_duplicates(inplace = True)

            self.df3['DateTime'] = pd.to_datetime(self.df3['DateTime']).apply(lambda x:x.strftime('%m/%d/%Y %X'))
            #for value in df3.index.tolist():
            #    df3.loc[value,'DateTime'] = pd.to_datetime(df3.loc[value,'DateTime']).strftime('%m/%d/%Y %X')

            print(self.pointname + ' time to prep data for function = ' + str(dt.now() - self.timefunction))

            #for point in points:
            #    [filleddatastream[point.name], params[point.name], modelupdate_FLAG[point.name], learningstill_FLAG[point.name]] = chgpt_detect_ft_v9C(pastdata = None, datastream = df3[df3['tag name'] == point.name], params = None, hihi = 60,lolo = 5, modelupdate_FLAG = 1, learningstill_FLAG = 1)
            [self.filleddatastream, self.params, self.modelupdate_FLAG, self.learningstill_FLAG] = chgpt_detect_ft_v9C(pastdata = None, datastream = self.df3[self.df3['tag name'] == self.pointname], params = None, hihi = 60,lolo = 5, modelupdate_FLAG = 1, learningstill_FLAG = 1)


            # build string for point query for sub points we are pushing data too
            ####################################################################################################################
            # create list of all the tag suffixes we need to build
            self.suffixnames = ['.Prediction', '.PredictionAlert', '.PredictionComAlert', '.PredictionHigh', '.PredictionLow']

            # create dictionary to hold tag names
            self.subpoints = {}

            # build a tag retrieval string for each the sub points with each suffixes
            self.PointQueryString = ''
            # loop through suffixes to build a tag retrieval string for each
            for self.suffix in self.suffixnames:
                # first part of string doesnt get the 'OR'
                if self.suffix == self.suffixnames[0]:
                    self.PointQueryString += ('name: ' + self.pointname + self.suffix)
                else:
                    self.PointQueryString += (' OR name: ' + self.pointname + self.suffix)

                # get points from pi server
                self.subpoints = webapi.points(query=self.PointQueryString, scope='pi:PIUDNAPPDEV01')

            # print out time it took to initialize
            print(self.pointname + ' time to initialize total = ' + str(dt.now() - self.timefunction))

            # set time we release the point back to the queue
            self.timesincelastupdate = dt.now()

            # after initialization place in queue for updates
            qu.put(self.pointname)



    def update(self):
        # make the global variables visible for overal point list, the value update dataframe,
        global points
        global df
        global qu
        global alerts
        global cluster_hours
        global stmt
        global conn
        # print out time it took to initialize
        if (dt.now() - self.timesincelastupdate)> timedelta(seconds=15):
            print(self.pointname + ' time to initialize = ' + str(dt.now() - self.timesincelastupdate))

        self.timefunction = dt.now()

        # check for point updates.  if there is a point update then send to function to process errors, push results to pi, and check for new alerts for sql

        try:
            self.points[0].current()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            # place in queue for next update
            qu.put(self.pointname)
            return

        # =============================================================================
        # if we got new values for this point
        if not df[df['tag name'] == self.pointname].empty:
            # start new thread here
            #self.thread = threading.Thread(target = self.updatenewvalues, args = ())
            #self.thread.start()

            # spin off a thread to take care of it
            #             # temp time measure start
            #             timestartprep = dt.now()
            #             print(point.name + ' new')

            #df['DateTime'] = pd.to_datetime(df3['DateTime']).apply(lambda x:x.strftime('%m/%d/%Y %X'))
            #df['DateTime'][df['tag name'] == point.name] = pd.to_datetime(df3['DateTime'][df['tag name'] == point.name]).apply(lambda x:x.strftime('%m/%d/%Y %X'))
            for value in df[df['tag name'] == self.pointname].index.tolist():
                df.loc[value,'DateTime'] = pd.to_datetime(df.loc[value,'DateTime']).strftime('%m/%d/%Y %X')
            #             df.drop_duplicates(inplace = True)
            #             print(str(dt.now() - timestartprep) + ' prep')
            #             timestartEP = dt.now()
            #             # check new points for flags
            [self.filleddatastream2, self.params, self.modelupdate_FLAG, self.learningstill_FLAG] = chgpt_detect_ft_v9C(pastdata = self.filleddatastream, datastream = df[df['tag name'] == self.pointname], params = self.params, hihi = 60,lolo = 5, modelupdate_FLAG = self.modelupdate_FLAG, learningstill_FLAG = self.learningstill_FLAG)
            #             print(str(dt.now() - timestartEP) + ' EP function')
            #             timestartpiprep = dt.now()
            #             # update old data with the new data
            self.filleddatastream = pd.concat([self.filleddatastream, self.filleddatastream2], ignore_index=True)
            #
            #             # push data values off to pi
            #
            #             #points2[0].update_value('2017-09-21T10:02:00Z', 53)
            #             #points2[1].update_value('*', 53)
            #             #record = 0
            for record in self.filleddatastream2.index.tolist():
                #                 #filleddatastream2[point.name]['DateTime'][record] = str(filleddatastream2[point.name]['DateTime'][record].isoformat())
                self.filleddatastream2.loc[record,'DateTimeStr'] = str(self.filleddatastream2['DateTime'][record].isoformat())
            #                 #filleddatastream2[point.name].loc[record,'DateTimeStr'] = str(filleddatastream2[point.name]['DateTime'][record].isoformat())

            # convert np.ints to ints
            #filleddatastream2[point.name]['alertflags'].astype('str')
            #type(int(filleddatastream2[points[1].name]['alertflags'][0]))
            #type(filleddatastream2[point.name]['alertflags'].tolist()[0])
            #             print(str(dt.now() - timestartpiprep) + ' pi prep')
            #             timestartpi = dt.now()
            #             #timestamps_to_be_inserted = ['2017-09-21T10:02:00Z', '2017-09-21T10:04:00Z', '2017-09-21T10:05:00Z', '2017-09-21T10:06:00Z']
            #             #values_to_be_inserted = [50, 95, 120, 121]
            self.subpoints[0].update_values(self.filleddatastream2['DateTimeStr'], self.filleddatastream2['prediction'].tolist())
            self.subpoints[1].update_values(self.filleddatastream2['DateTimeStr'], self.filleddatastream2['alertflags'].tolist())
            self.subpoints[2].update_values(self.filleddatastream2['DateTimeStr'], self.filleddatastream2['purpleflags'].tolist())
            self.subpoints[3].update_values(self.filleddatastream2['DateTimeStr'], self.filleddatastream2['predictionhigh'].tolist())
            self.subpoints[4].update_values(self.filleddatastream2['DateTimeStr'], self.filleddatastream2['predictionlow'].tolist())
            #             #filleddatastream2[point.name]['DateTime'][1].isoformat()
            #             #dt.isoformat(filleddatastream2[point.name]['DateTime'])
            #             #print (lambda x: dt.isoformat(x), filleddatastream2[point.name]['DateTime']
            #             print(str(dt.now() - timestartpi) + ' pi upload')

            #             timesql = dt.now()
            # if there is an alert in the last 30 hours, but there is no alert record for this tag, create a new alert record.
            if (len(self.filleddatastream[(self.filleddatastream['alertflags'] == 1) & (self.filleddatastream['DateTime'] > (dt.now() - timedelta(hours=cluster_hours)))])
                    and alerts[alerts['Tag Name'] == self.pointname].empty):

                try:
                    with conn.cursor() as cursor:
                        # Create a new record
                        #cursor = conn.cursor()
                        #sql = "INSERT INTO [RegFailure].[dbo].[Alerts] ([Tag Name], `password`) VALUES (%s, %s)"

                        self.sqlinsert = 'INSERT INTO [RegFailure].[dbo].[Alerts] ([Tag Name],[Alert Type ID],[Start Time],[Last Updated Time]) VALUES (\'' + self.pointname + '\', 2, \'' + str(min(self.filleddatastream['DateTime'][(self.filleddatastream['alertflags'] == 1) & (self.filleddatastream['DateTime'] > (dt.now() - timedelta(hours=cluster_hours)))])) + '\', \'' + str(dateutil.parser.parse(str(dt.now())))[:19] + '\')'

                        #conn.execute()
                        cursor.execute(self.sqlinsert)

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        #conn.commit()
                except:
                    print("trouble inserting!")

                #update alerts table since we changed it
                alerts = pd.read_sql(stmt,conn)

            # if there is are not alerts in the last 30 hours, but there is an alert record for this tag, then close it out by updating it with an end time.
            elif (self.filleddatastream[(self.filleddatastream['alertflags'] == 1) & (self.filleddatastream['DateTime'] > (dt.now() - timedelta(hours=cluster_hours)))].empty
                  and len(alerts[alerts['Tag Name'] == self.pointname])):

                try:
                    with conn.cursor() as cursor:
                        # Create a new record
                        #cursor = conn.cursor()
                        #sql = "INSERT INTO [RegFailure].[dbo].[Alerts] ([Tag Name], `password`) VALUES (%s, %s)"
                        self.sqlinsert = 'UPDATE [RegFailure].[dbo].[Alerts] SET [End Time] = \'' + str(dateutil.parser.parse(str(dt.now())))[:19] + '\',[Last Updated Time] = \'' + str(dateutil.parser.parse(str(dt.now())))[:19] + '\' WHERE [Alert ID] = ' + str(int(alerts['Alert ID'][alerts['Tag Name'] == self.pointname]))
                        #conn.execute()
                        cursor.execute(self.sqlinsert)

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        #conn.commit()
                except:
                    print("trouble updating!")

                #update alerts table since we changed it
                alerts = pd.read_sql(stmt,conn)

            #             print(str(dt.now() - timesql) + ' sql bit')
            #             # check for alerts, if there is, check sql cache if it already exists.  if not push it to sql
            #
            #             # check sql cache for open data issue on this point.  if so, check for alerts in last 8 hours.  if none, then close the sql alert and cache alert
            #

            #             # drop rows from the df so we don't use them again
            #             timedrop = dt.now()
            df.drop(df[df['tag name'] == self.pointname].index, inplace = True)

            # drop old records from history
            self.filleddatastream.drop(self.filleddatastream[self.filleddatastream['DateTime'] > (dt.now() - timedelta(days=14))].index, inplace = True)


            #
            #             # temp time measure end/print
            #             print(str(dt.now() - timedrop) + ' pi upload')

            # print out time it took to run the update
            print(self.pointname + ' time to update = ' + str(dt.now() - self.timefunction))

        # set time we release the point back to the queue
        self.timesincelastupdate = dt.now()

        # place in queue for next update
        qu.put(self.pointname)
# =============================================================================




# Main code loop
############################################################################################################################################33

# get tag names from file
# this will need to be updated later to pull from AF
TagNamePath = path + 'TagNames_11_27_17.csv'
#TagNamePath = path + 'TagNames_36tags_12_12_17.csv'
TagNames = pd.read_csv(TagNamePath)

# initialize the list of point definitions
points = []
# initialize dictionary of point monitoring classes
pointsmonitored = {}

# initialize queue.  this queu fifo queue is the queu for updates.  anything in it has no current process running, and it has been at least a wait time since last update call
qu = queue.Queue()

#lock = threading.Lock()

timeallinitials = dt.now()
# build string for point query for single tag
for tag in TagNames['Tag']:
    pointsmonitored[tag] = PointMonitoring(tag)
    #pointsmonitored['GO.CC_MON_RM17_PT3'] = PointMonitoring('GO.CC_MON_RM17_PT3')
# =============================================================================
# while qu.qsize() < 7:
#     time.sleep(10)
#     print(str(qu.qsize()))
# print('time to initialize all of them = ' + str(dt.now() - timeallinitials))
# =============================================================================


# loop through queue and update
#qu.qsize()
#while 1:
i = 0
while i<1000:
    if qu.empty():
        time.sleep(1)
    else:
        tag = qu.get()
        pointsmonitored[tag].update()
    i =+ 1

# PI connection cleanup
webapi.unsubscribe(points, 'current')

# SQL connection cleanup
conn.close()