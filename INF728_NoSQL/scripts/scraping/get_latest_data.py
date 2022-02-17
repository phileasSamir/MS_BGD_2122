import requests
import subprocess
from time import time
from get_clean_data import dl_unzip, nettoyage_event, nettoyage_mentions, nettoyage_gkg


t0=time()

def get_date(str):
    return int("0"+str.split("/")[-1].split(".")[0])

process = subprocess.Popen("/opt/hadoop/bin/hdfs dfs -ls /data/ab_data/year".split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
std_out, _ = process.communicate()
last_file = std_out.decode().split()[-1]

latest_date = get_date(last_file)

file = "masterfilelist.txt"
url = "http://data.gdeltproject.org/gdeltv2"
liste = requests.get(f"{url}/{file}").content.decode("utf-8").split("\n")
masterfile0 = [i for i in liste if get_date(i) > latest_date]

file = "masterfilelist-translation.txt"
liste = requests.get(f"{url}/{file}").content.decode("utf-8").split("\n")
masterfile1 =  [i for i in liste if get_date(i) > latest_date]


if __name__=="__main__":

    files_en = list(map(lambda x: x.split(url)[-1], masterfile0))
    files_tr = list(map(lambda x: x.split(url)[-1], masterfile1))
    
    files = files_en + files_tr
    
    subprocess.call(f"rm -rf /tmp/tests/latest".split())
    subprocess.call(f"mkdir -p /tmp/tests/latest".split())

    for file in files:
        dl_unzip(url, file, f"/tmp/tests/latest")
        file = f"/tmp/tests/latest/"+file
        if "export" in file:
            df=nettoyage_event(file)
            subprocess.call(f"gzip {file.strip('.zip')}".split())
        elif "mentions" in file:
            df=nettoyage_mentions(file)
            subprocess.call(f"gzip {file.strip('.zip')}".split())
        elif "gkg" in file:
            df=nettoyage_gkg(file)
            subprocess.call(f"gzip {file.strip('.zip')}".split())
            subprocess.call(f"gzip {file.strip('.csv.zip')+'_d.csv'}".split())
        else: pass
        subprocess.call(f"rm {file}".split())

    t = time()-t0
    m = t//60
    s = t%60

    print(f"\nDUREE EXECUTION: {int(m)}min:{int(s)}sec")