import os
import socket
import sys
import subprocess
from multiprocessing import Pool
from functools import partial
import glob
import socket
from collections import Counter

user = os.getlogin()

def java_hash(s: str) -> int:
    """Function to mimic java hashcode"""
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000 

def map_(split, wdir): 
  open(f"{wdir}/maps/UM"+split.split("S")[-1], "w").writelines([word + "\n" for word in open(split,'r').read().split()])
  return True

def shuffle0_(map, wdir): 
  list_ = open(f"{wdir}/machines.txt","r").read().split()
  ntot = len(list_)
  dict_ = {}
  for line in open(map, "r").readlines():
    if line.split():
      hash_ = java_hash(line.split()[0])
      nmachine = list_[hash_ % ntot]
      if nmachine in dict_:
        dict_[nmachine] += [line]
      else:
        dict_[nmachine] = [line] 
  for k,v in dict_.items():
    open(f"{wdir}/shuffles/{socket.gethostname()}|{k}.txt", "a").write("".join(v))
  return True
  
def shuffle1_(shuffle, wdir):
  output_ = f"{wdir}/shufflesreceived/"
  bashCommand = f"scp {shuffle} {user}@{os.path.basename(shuffle).split('|')[-1][:-4]}:{output_}".split()
  subprocess.Popen(bashCommand, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).communicate()
  return True

def reduce0_(file, machines):
  dict_={}
  if os.path.basename(file).split("|")[-2] in machines:
    for line in open(file,"r").readlines():
      x = line.strip()
      if x:
        if x in dict_:
          dict_[x] += 1
        else:
          dict_[x] = 1
  return dict_    

def main():
  wdir = os.path.dirname(sys.argv[0])
  if sys.argv[1] == "--map":
    p = Pool()
    p.map(partial(map_, wdir=wdir), glob.glob(f"{wdir}/splits/*"))
    return True
  if sys.argv[1] == "--shuffle":
    p = Pool()
    p.map(partial(shuffle0_, wdir=wdir), glob.glob(f"{wdir}/maps/*"))
    #when nmachines>10, this is not reliable anymore
    #list(map(lambda x: x.communicate(), [shuffle1_(shuffle, wdir) for shuffle in glob.glob(f"{wdir}/shuffles/*")]))
    #this solves the problem but is too slow
    #for shuffle in glob.glob(f"{wdir}/shuffles/*"):
    #  shuffle1_(shuffle, wdir).communicate()
    p = Pool(5)
    result = p.map(partial(shuffle1_, wdir=wdir), glob.glob(f"{wdir}/shuffles/*"))
    return True
  if sys.argv[1] == "--reduce":
    dict_ = Counter()
    p = Pool()
    result = p.map(partial(reduce0_, machines=open(f"{wdir}/machines.txt","r").read()), glob.glob(f"{wdir}/shufflesreceived/*"))
    [dict_.update(x) for x in result]
    open(f"{wdir}/reduces/{socket.gethostname()}.txt", "w").writelines([f"{k} {v}\n" for k, v in dict_.most_common()])
    return True

if __name__ == '__main__':
  main()