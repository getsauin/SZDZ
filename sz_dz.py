#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 19:54:43 2021

@author: sAuMac
"""

import pandas as pd
import numpy as np



def validate_sz_dz_zone(i_df):
    i_df['SZ_Prox'] = i_df['SZ_Dist'] = i_df['DZ_Prox'] = i_df['DZ_Dist'] = 0.0
    sz_dz = ['SZ', 'DZ']
    for calc in sz_dz:
        field2Compare = 'High'
        fieldProx = 'SZ_Prox'
        fieldDist = 'SZ_Dist'
        zoneIdxArray = np.where(i_df['Zones'] == 'SZ')
        zoneIdx = curIdx = 0
        noMoreZone = False
        if (calc == 'DZ'):
            field2Compare = 'Low'
            fieldProx = 'DZ_Prox'
            fieldDist = 'DZ_Dist'
            zoneIdxArray = np.where(i_df['Zones'] == 'DZ')
        while((curIdx < len(df) and (noMoreZone == False))):
            workingIdx = curIdx
            zoneIdxInDf = zoneIdxArray[0][zoneIdx]
            zoneVal = df['Prox'][zoneIdxArray[0][zoneIdx]]
            noZoneBeat = False
            while((workingIdx < zoneIdxInDf) or ((workingIdx > zoneIdxInDf) and (workingIdx < len(df)))):
                fieldVal = df[field2Compare][workingIdx]
                if (calc == 'SZ'):
                    while(fieldVal > zoneVal):
                        zoneIdx = zoneIdx + 1
                        if (zoneIdx < (len(zoneIdxArray[0]))):
                            zoneVal = df['Prox'][zoneIdxArray[0][zoneIdx]]
                            zoneIdxInDf = zoneIdxArray[0][zoneIdx]
                        elif(zoneIdx > (len(zoneIdxArray[0]))):
                            noZoneBeat = True
                            break
                elif (calc == 'DZ'):
                    while(fieldVal < zoneVal):
                        zoneIdx = zoneIdx + 1
                        if (zoneIdx < (len(zoneIdxArray[0]))):
                            zoneVal = df['Prox'][zoneIdxArray[0][zoneIdx]]
                            zoneIdxInDf = zoneIdxArray[0][zoneIdx]
                        elif(zoneIdx > (len(zoneIdxArray[0]))):
                            noZoneBeat = True
                            break
                # get next sz index wrt working idx
                if (noZoneBeat):
                    res = (np.abs(zoneIdxArray[0] - workingIdx)).argmin()
                    if (zoneIdxArray[0][res] < workingIdx):
                        zoneIdx = res + 1
                        if (zoneIdx < len(zoneIdxArray[0])):
                            zoneIdxInDf = zoneIdxArray[0][res + 1]
                        else:
                            noMoreZone = True
                    else:
                        zoneIdx = res
                        zoneIdxInDf = zoneIdxArray[0][res]
                    break
                workingIdx = workingIdx + 1
            if (noZoneBeat == False):
                df[fieldProx][curIdx] = df['Prox'][zoneIdxInDf]
                df[fieldDist][curIdx] = df['Dist'][zoneIdxInDf]
            curIdx = curIdx + 1
            res = (np.abs(zoneIdxArray[0] - curIdx)).argmin()
            if (res < curIdx):
                zoneIdx = res + 1
                if (zoneIdx < len(zoneIdxArray[0])):
                    zoneIdxInDf = zoneIdxArray[0][res + 1]
                else:
                    noMoreZone = True
            else:
                zoneIdx = res
                zoneIdxInDf = zoneIdxArray[0][res]
            if ((curIdx == zoneIdxInDf) and ((zoneIdx + 1) < (len(zoneIdxArray[0])))):
                zoneIdx = zoneIdx + 1
                if (calc == 'SZ'):
                    zoneVal = df['Prox'][zoneIdxArray[0][zoneIdx]]
                elif (calc == 'DZ'):
                    zoneVal = df['Dist'][zoneIdxArray[0][zoneIdx]]
    
if __name__ == "__main__":
    df = pd.read_csv("NIFTY.csv")
    df.set_index('Date_time', inplace = True)
    df =  df.reset_index()
    validate_sz_dz_zone(df)
    df.to_csv('NIFTY_SZ_DZ.csv')
