#THIS SHOULD NOT BE NEEDED ANYMORE
#FUNCTIONS WERE INCLUDED DIRECTLY INTO MASTER

import subprocess
import sys
from multiprocessing import Pool
from functools import partial

user = open("login.txt","r",encoding="utf8").read()

def ssh_test(ip):
    try:
        output = subprocess.Popen(["ssh", f"{user}@{ip}", f"ls /tmp/{user}"], stdin=subprocess.PIPE)
        return output.communicate(timeout=20)
    except:
        print("erreur", ip)

def scp_(ip, input_, output_):
    try:
        subprocess.Popen(f"ssh -q -o StrictHostKeyChecking=no {user}@{ip} mkdir -p {output_}".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        subprocess.run(f"scp {input_} {user}@{ip}:{output_}",timeout=20)
        return True
    except:
        print("erreur", ip)
        return False

def rm_(ip):
    try:
        subprocess.Popen(f"ssh {user}@{ip} rm -rf /tmp/{user}/".split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL).communicate(timeout=20)
        for dir in ["splits","maps","shuffles","shufflesreceived","reduces"]:
            subprocess.Popen(f"ssh -q {user}@{ip} mkdir -p /tmp/{user}/{dir}/".split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL).communicate()
        #output = subprocess.Popen(f"ssh {user}@{ip} ls /tmp/{user}".split(), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL).communicate()
        return True
    except:
        print("erreur", ip)
        return ip


def main():
    funct_ = sys.argv[1]
    p = Pool()
    if funct_ == "--test":
        filename = sys.argv[2]
        result = p.map(ssh_test, open(filename,'r',encoding='utf8').read().split()) 
        #print(result)   
    elif funct_ == "--scp":
        filename = sys.argv[4]
        ips = open(filename,'r',encoding='utf8').read().split()
        input_, output_ = sys.argv[2], sys.argv[3]
        result = p.map(partial(scp_, input_=input_), ips)
        #print(result)
    elif funct_ == "--clean":
        filename = sys.argv[2]
        ips = open(filename,'r',encoding='utf8').read().split()
        #folder = sys.argv[2]
        result = p.map(rm_, ips)
        #print(result)
    else:
        print("Syntax : python DEPLOY.py [--test] [--scp input output] [--clean] hostnames.txt")
        print("--test will test ssh connections")
        print("--scp will copy a file from input to output")    
        return False
    print(*[x for x in result if x != True])
    print(len([x for x in result if x != True]))
    return True

if __name__ == '__main__':
  main()