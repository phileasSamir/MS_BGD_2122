#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pandasql import sqldf
import requests
import subprocess
import sys
from cassandra.cluster import Cluster
from random import choice
from shutil import move
from os import path, mkdir
from time import time
from IPython.display import display

t0=time()


file = "masterfilelist.txt"
url = "http://data.gdeltproject.org/gdeltv2"
liste = requests.get(f"{url}/{file}").content.decode("utf-8").split("\n")
masterfile0 = [i for i in liste if "/2021" in i]
#open(f"{file}","w",encoding="utf8").write("\n".join(liste))

file = "masterfilelist-translation.txt"
url = "http://data.gdeltproject.org/gdeltv2"
liste = requests.get(f"{url}/{file}").content.decode("utf-8").split("\n")
masterfile1 = [i for i in liste if "/2021" in i]
#open(f"{file}","w",encoding="utf8").write("\n".join(liste))


def dl_unzip(url, file, tardir):
  subprocess.call(f"wget {url}{file} -O {tardir}{file}".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  #subprocess.call(f"unzip {tardir}{file} -d {tardir}".split())#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  #subprocess.call(f"rm {tardir}{file}".split())#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  return True

url = "http://data.gdeltproject.org/gdeltv2"

def nettoyage_event(file):
    col = ['GlobalEventID', 'Day', 'MonthYear', 'Year', 'FractionDate',
           'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode',
           'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code',
           'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 'Actor2Code',
           'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode',
           'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code',
           'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code', 'IsRootEvent',
           'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass',
           'GoldsteinScale', 'NumMentions', 'NumSources', 'NumArticles', 'AvgTone',
           'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode',
           'Actor1Geo_ADM1Code', 'Actor1Geo_ADM2Code', 'Actor1Geo_Lat',
           'Actor1Geo_Long', 'Actor1Geo_FeatureID', 'Actor2Geo_Type',
           'Actor2Geo_FullName', 'Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code',
           'Actor2Geo_ADM2Code', 'Actor2Geo_Lat', 'Actor2Geo_Long',
           'Actor2Geo_FeatureID', 'ActionGeo_Type', 'ActionGeo_FullName',
           'ActionGeo_CountryCode', 'ActionGeo_ADM1Code', 'ActionGeo_ADM2Code',
           'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID', 'DATEADDED',
           'SOURCEURL']
    df = pd.read_csv(file, sep="\t", usecols=list(range(len(col))), names=col, encoding="ISO-8859-1",keep_default_na=False)
    df = df.loc[df["Year"]==2021][['GlobalEventID', 'Day', 'MonthYear', 'Year',
                                   'ActionGeo_CountryCode']]
    df.columns = ['event_id', 'jour_event', 'mois_event', 'annee_event', 'pays']
    df["pays"] = df["pays"].fillna("00")
    df["pays"] = df["pays"].replace("", "00")
    df.to_csv(file.strip(".zip"), sep="\t", header=True, index=False, encoding="ISO-8859-1")
    #return df


def nettoyage_mentions(file):
    col = ['GlobalEventID', 'EventTimeDate', 'MentionTimeDate', 'MentionType',
           'MentionSourceName', 'MentionIdentifier', 'SentenceID',
           'Actor1CharOffset', 'Actor2CharOffset', 'ActionCharOffset', 'InRawText',
           'Confidence', 'MentionDocLen', 'MentionDocTone',
           'MentionDocTranslationInfo']
    df = pd.read_csv(file, sep="\t", usecols=list(range(len(col))), names=col, encoding="ISO-8859-1")
    
    # Evénements de 2021, et seulement les colonnes qui nous intéressent
    df = df.loc[df["EventTimeDate"] >= 20210000000000][['GlobalEventID', 'MentionIdentifier', 
                                                        'MentionDocTranslationInfo','MentionTimeDate']]
    # Langue de l'article qui mentionne l'événement
    df["MentionDocTranslationInfo"] = df["MentionDocTranslationInfo"].fillna("eng")
    df["MentionDocTranslationInfo"] = df["MentionDocTranslationInfo"].apply(lambda x: x if x=="eng" else x[6:9])
    df["MentionTimeDate"] = df["MentionTimeDate"].astype(str)
    df["MentionTimeDate"] = df["MentionTimeDate"].str[0:8]
    df["month"] = df["MentionTimeDate"].str[0:6]
    df["year"] = df["MentionTimeDate"].str[0:4]
    df[["year","month","MentionTimeDate"]] = df[["year","month","MentionTimeDate"]].astype(int)
    df.columns = ['event_id', 'mention_id', 'langue', 'jour_mention', 'mois_mention', 'annee_mention']
    df.to_csv(file.strip(".zip"), sep="\t", header=True, index=False, encoding="ISO-8859-1")


def nettoyage_gkg(file):
    col = ['GKGRECORDID','V2.1DATE','V2SOURCECOLLECTIONIDENTIFIER',
           'V2SOURCECOMMONNAME','V2DOCUMENTIDENTIFIER','V1COUNTS','V2.1COUNTS',
           'V1THEMES','V2ENHANCEDTHEMES','V1LOCATIONS','V2ENHANCEDLOCATIONS',
           'V1PERSONS','V2ENHANCEDPERSONS','V1ORGANIZATIONS',
           'V2ENHANCEDORGANIZATIONS','V1.5TONE','V2.1ENHANCEDDATES','V2GCAM',
           'V2.1SHARINGIMAGE','V2.1RELATEDIMAGES','V2.1SOCIALIMAGEEMBEDS',
           'V2.1SOCIALVIDEOEMBEDS','V2.1QUOTATIONS','V2.1ALLNAMES','V2.1AMOUNTS',
           'V2.1TRANSLATIONINFO','V2EXTRASXML']
    df = pd.read_csv(file, sep="\t", usecols=list(range(len(col))), names=col, encoding="ISO-8859-1")
    # éléments de 2021
    df = df.loc[df["V2.1DATE"] > 2021_00_00_00_00_00]
    # Dates au format int(YYYYMMDD) (sans les heures minutes secondes)
    df["V2.1DATE"] = df["V2.1DATE"].apply(lambda x: str(x)[0:8])
    # Extraction de la langue originale
    df["V2.1TRANSLATIONINFO"] = df["V2.1TRANSLATIONINFO"].fillna("eng")
    df["V2.1TRANSLATIONINFO"] = df["V2.1TRANSLATIONINFO"].apply(lambda x: x if x=="eng" else x[6:9])

    # Colonnes utiles uniquement
    df = df[['GKGRECORDID', 'V2SOURCECOMMONNAME',
             'V1THEMES','V1LOCATIONS','V1PERSONS',
             'V1.5TONE','V2.1TRANSLATIONINFO', 'V2.1DATE']]
    #Extraction des valeurs de TONE intéressantes
    df["TONE"] = df["V1.5TONE"].str.split(pat=",", expand=True)[[0]]
    df.drop(labels="V1.5TONE",axis=1, inplace=True)
    
    # Dates
    df["MONTH"] = df["V2.1DATE"].str[0:6].astype(int)
    df["YEAR"] = df["V2.1DATE"].str[0:4].astype(int)
    df["V2.1DATE"] = df["V2.1DATE"].astype(int)

    df = df[["GKGRECORDID", "V2SOURCECOMMONNAME", "V1THEMES", "V1LOCATIONS", "V1PERSONS", \
	     "TONE", "V2.1TRANSLATIONINFO", "V2.1DATE", "MONTH", "YEAR"]]

    # header cool
    df.columns = ["gkg_id", "source", "theme", "lieu", "personne", "ton", "langue", "jour", "mois", "annee"]
    
    df["personne"] = df["personne"].str.split(";").apply(lambda x: x[:2] if isinstance(x, list) else x)
    df["theme"] = df["theme"].str.split(";").apply(lambda x: x[:2] if isinstance(x, list) else x)
    df["lieu"] = df["lieu"].str.split(";").apply(lambda x: x[:2] if isinstance(x, list) else x)
    # Explode les theeeeeeemes !!!!! \m/ 
    df = df.explode("personne").explode("theme").explode("lieu")
    
    # Extraction du CountryCode uniquement pour LOCATION
    df["lieu"] = df["lieu"].apply(lambda x: x.split("#")[2] if isinstance(x,str) else x)
    
    #df.fillna("", inplace=True)
    df[["source","theme","lieu","personne"]] = df[["source","theme","lieu","personne"]].fillna("UNK").replace("","UNK")
    df[["source","theme","lieu","personne","langue"]] = df[["source","theme","lieu","personne","langue"]].astype(str)
    df = df.drop_duplicates()
    #display(df.head())
    df_c = sqldf("SELECT source, theme, personne, lieu, jour, mois, annee, COUNT(*) as total, SUM(ton) as somme_ton\
		FROM df\
		GROUP BY source, theme, personne, lieu, jour, mois, annee")
    df_d = sqldf("SELECT lieu, langue, jour, mois, annee, COUNT(*) as total, SUM(ton) as somme_ton\
		FROM df\
		GROUP BY lieu, langue, jour, mois, annee")
    #display(df_c.head())
    #display(df_d.head())
    df_c.to_csv(file.strip(".zip"), sep="\t", header=True, index=False, encoding="ISO-8859-1")
    df_d.to_csv(file.strip(".csv.zip")+"_d.csv", sep="\t", header=True, index=False, encoding="ISO-8859-1")
    #return df

if __name__=="__main__":

    timespan = sys.argv[1]

    files_en = list(map(lambda x: x.split(url)[-1], masterfile0))
    files_tr = list(map(lambda x: x.split(url)[-1], masterfile1))
    if timespan == "hour":
        files = files_en[-3*4:] + files_tr[-3*4:]
    elif timespan == "day":
        files = files_en[-3*4*24:] + files_tr[-3*4*24:]
    elif timespan == "week":
        files = files_en[-3*4*24*7:] + files_tr[-3*4*24*7:]
    elif timespan == "month":
        files = files_en[-3*4*24*30:] + files_tr[-3*4*24*30:]
    elif timespan == "year":
        files = files_en[-3*4*24*30*365:] + files_tr[-3*4*24*365:]
    else:
        print("Please provide a valid timespan")
    
    subprocess.call(f"rm -rf /tmp/tests/{timespan}".split())
    subprocess.call(f"mkdir -p /tmp/tests/{timespan}".split())

    for file in files:
        #print(f'file:= {file}')
        dl_unzip(url, file, f"/tmp/tests/{timespan}")
        file = f"/tmp/tests/{timespan}"+file
        #coord = choice(nodes) # choix d'un coordinateur different pour ne pas saturer le même ordi
        #session = loginDB(coord,'test')
        #if not path.exists('/tmp/tests/traiter'):
        #    mkdir('/tmp/tests/traiter')
        if "export" in file:
            df=nettoyage_event(file)
            subprocess.call(f"gzip {file.strip('.zip')}".split())
            #move(file, '/tmp/tests/traiter/')
        elif "mentions" in file:
            df=nettoyage_mentions(file)
            subprocess.call(f"gzip {file.strip('.zip')}".split())
            #move(file, '/tmp/tests/traiter/')
        elif "gkg" in file:
            df=nettoyage_gkg(file)
            subprocess.call(f"gzip {file.strip('.zip')}".split())
            subprocess.call(f"gzip {file.strip('.csv.zip')+'_d.csv'}".split())
            #move(file,'/tmp/tests/traiter')"""
        else: pass
        subprocess.call(f"rm {file}".split())#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



    t = time()-t0
    m = t//60
    s = t%60

    print(f'\nDUREE EXECUTION: {int(m)}min:{int(s)}sec')
