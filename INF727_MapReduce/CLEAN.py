import subprocess
from multiprocessing import Pool
import sys

user = open("login.txt","r",encoding="utf8").read().strip()
wdir = open("wdir.txt","r",encoding="utf8").read().strip()

def clean_(ip): 
    return [subprocess.Popen(f'ssh {user}@{ip} pkill -9 -u {user} -f "SLAVE"'.split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
    subprocess.Popen(f"ssh {user}@{ip} rm -rf {wdir}".split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
    subprocess.Popen(f"ssh {user}@{ip} mkdir -p {wdir}".split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)]


def main():
    filename = sys.argv[1]
    try:
        nmachines = int(sys.argv[2])
    except:
        nmachines = len(open(filename,'r',encoding='utf8').read().split())
    ips = open(filename,'r',encoding='utf8').read().split()[:nmachines]
    [clean_(ip) for ip in ips]
    return True

if __name__== '__main__':
    main()