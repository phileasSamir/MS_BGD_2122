import subprocess
import sys
import time
import os
import glob
import datetime
import shutil
from collections import Counter
from multiprocessing import Pool

user = open("login.txt","r",encoding="utf8").read().strip()
wdir = open("wdir.txt","r",encoding="utf8").read().strip()+f"/{os.getpid()}" #this allows multiple mapreduce jobs to run separately
#we could use a hash to avoid collision even further

def create_splits(machines, splits):
    raw = open("wet.paths","r").read().split()
    for i in range(machines):
        open(f"splits/S{i}.txt","w",encoding="utf8").write("\n".join(raw[i*splits:(i+1)*splits]))

def clean_(ip): 
    for dir in ["splits","maps","shuffles","shufflesreceived","reduces","urls"]:
        yield subprocess.Popen(f"ssh {user}@{ip} mkdir -p {wdir}/{dir}/".split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def split_(ip, split):
    return subprocess.Popen(f"scp {split} {user}@{ip}:{wdir}/urls/".split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)

def slave_(ip, funct_):
    return subprocess.Popen(f"ssh {user}@{ip} python3 {wdir}/SLAVE_BIG.py --{funct_}".split(), stdin=subprocess.PIPE)

def scp_(ip, input_, output_):
    return subprocess.Popen(f"scp {input_} {user}@{ip}:{output_}".split(),stdout=subprocess.DEVNULL)

def clean_slave_(ip):
    return subprocess.Popen(f"ssh {user}@{ip} rm -rf {wdir}".split(), stdin=subprocess.PIPE) 

def read_dict(f):
    dict_ = {}
    for l in open(f,"r",encoding="utf8").readlines():
        if l.split():
            dict_[l.split()[0]] = int(l.split()[1])
    return dict_

def main(args = None):
    dictimes = {}
    t00 = time.time()
    print(f"{datetime.datetime.now().time().strftime('[%H:%M:%S]')} START")
    if not args:
        filename = sys.argv[1]
        nmachines = int(sys.argv[2])
        nsplits = int(sys.argv[3])
    else: 
        filename, nmachines, nsplits = args
    dictimes["file"] = "BIG"
    dictimes["nmachines"] = nmachines
    dictimes["nsplits"] = nsplits
    ips = open(filename,'r',encoding='utf8').read().split()
    shutil.rmtree('./splits', ignore_errors=True)
    shutil.rmtree('./results', ignore_errors=True)
    os.makedirs("./splits", exist_ok=True)
    os.makedirs("./results", exist_ok=True)
    t0 = time.time()
    mkdirs = [list(clean_(ip)) for ip in ips]
    result = [] 
    for i, ip in enumerate(ips[:nmachines]):
        try:
            if not mkdirs[i][0].communicate(timeout=5)[1]:
                result.append(ip)
        except:
            continue
    i = 1
    while len(result)<nmachines:
        try:
            x=list(clean_(ips[nmachines+i]))[0].communicate(timeout=2)[1]
            if not x:
                result.append(ips[nmachines+i])
        except:
            continue
        i+=1
    t1 = time.time()
    print(f"{datetime.datetime.now().time().strftime('[%H:%M:%S]')} clean done", result, f"time : {int(t1-t0)}s")
    dictimes["clean"] = t1-t0
    ips = result
    open("./machines.txt","w").write("\n".join(ips))
    list(map(lambda x: x.communicate(), [scp_(ip, "./SLAVE_BIG.py", wdir) for ip in ips]))
    list(map(lambda x: x.communicate(), [scp_(ip, "./machines.txt", wdir) for ip in ips]))
    #deploy to remotes and only use available machines from then on
    t0 = time.time()
    create_splits(len(ips), nsplits)
    t1 = time.time()
    print(f"{datetime.datetime.now().time().strftime('[%H:%M:%S]')} splits created time : {int(t1-t0)}s")
    dictimes["createsplits"] = t1-t0
    splits = glob.glob("./splits/*")
    t0 = time.time()
    result = list(map(lambda x: x.communicate(), [split_(ip, split) for ip, split in zip(ips, splits)]))
    t1 = time.time()
    print(f"{datetime.datetime.now().time().strftime('[%H:%M:%S]')} splits sent time : {int(t1-t0)}s")
    dictimes["sendsplits"] = t1-t0
    for fun in ["map","shuffle","reduce"]:
        t0 = time.time()
        result = list(map(lambda x: x.communicate(), [slave_(ip, fun) for ip in ips]))
        if fun == "reduce":
            tgetreduces = time.time()
            list(map(lambda x: x.communicate(),
            [subprocess.Popen(f"scp {user}@{ip}:{wdir}/reduces/* ./results/".split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL) 
            for ip in ips]))
            dictimes["getreduces"] = time.time()-tgetreduces
        t1 = time.time()
        print(f"{datetime.datetime.now().time().strftime('[%H:%M:%S]')} {fun} done time : {int(t1-t0)}s")
        dictimes[fun] = t1-t0
    t0 = time.time()
    dict_ = Counter()
    p = Pool()
    result = p.map(read_dict, glob.glob("./results/*"))
    [dict_.update(x) for x in result]
    t1 = time.time()
    dictimes["localreduce"] = t1-t0
    os.system("cls")
    t0 = time.time()
    sorted_ = dict_.most_common()
    t1 = time.time()
    [print(f"{k} {v}") for k,v in sorted_[:10]]
    dictimes["sort"] = t1-t0
    print(f"{datetime.datetime.now().time().strftime('[%H:%M:%S]')} sort and reduce time : {int(dictimes['sort']+dictimes['localreduce'])}s")
    open("./output.txt","w", encoding="utf8").writelines([f"{k} {v}\n" for k,v in sorted_])
    print(f"{datetime.datetime.now().time().strftime('[%H:%M:%S]')} final time : {int(time.time()-t00)}s")
    print(f"{datetime.datetime.now().time().strftime('[%H:%M:%S]')} END")
    dictimes["final"] = time.time()-t00
    open(f"exps/experimentsBIG.csv","a").writelines([f"{v}," for _,v in dictimes.items()]+["\n"])
    [clean_slave_(ip) for ip in ips]
    return True

if __name__ == '__main__':
    main()