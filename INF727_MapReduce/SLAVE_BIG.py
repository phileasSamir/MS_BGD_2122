import os
import socket
import sys
import subprocess
from multiprocessing import Pool
from functools import partial
import glob
from collections import Counter

user = os.getlogin()

def java_hash(s: str) -> int:
    """Function to mimic java hashcode"""
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

def get_splits(file, wdir):
  subprocess.call(f"wget https://commoncrawl.s3.amazonaws.com/{file} -P {wdir}/splits".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  file = file.split("/")[-1]
  subprocess.call(f"gzip -d {wdir}/splits/{file}".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  return True

"""def map_(split, wdir): 
  #this loop is a bit slower than loading the entire file to memory, splitting it then dumping it to map files
  #however, it uses way less memory, since you only load one line at a time to memory
  #this is why this function is different than the standard SLAVE version
  for line in open(f"{wdir}/splits/"+split,'r').readlines(): 
    open(f"{wdir}/maps/UM"+split.split("-")[-1], "a").writelines([word+"\n" for word in line.strip().split()])
  return True"""

def map_(split, wdir): 
  open(f"{wdir}/maps/UM"+split.split("-")[-1], "w").writelines([word.strip() + "\n" for word in open(f"{wdir}/splits/"+split,'r').read().split()])
  return True

def shuffle0_(map, wdir): 
  #check below for comments on speed and memory usage
  list_ = open(f"{wdir}/machines.txt","r").read().split()
  ntot = len(list_)
  dict_ = {}
  for line in open(f"{wdir}/maps/"+map, "r").readlines():
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

"""
this function is way, WAY slower BUT it does not require as much memory.
i have been unable to find a compromise between the previous method, which will use a lot of memory but write less to disks,
and this function which uses less memory but is too slow to even be considered when working on big files.
def shuffle0_(map): 
  list_ = open("{wdir}/machines.txt","r").read().split()
  ntot = len(list_)
  for line in open("{wdir}/maps/"+map, "r").readlines():
    open(f"{wdir}/shuffles/{socket.gethostname()}|{list_[java_hash(line.split()[0]) % ntot]}.txt", "a").write(line)
"""

def shuffle1_(shuffle, wdir):
  output_ = f"{wdir}/shufflesreceived/"
  bashCommand = f"scp {shuffle} {user}@{os.path.basename(shuffle).split('|')[-1][:-4]}:{output_}".split()
  return subprocess.Popen(bashCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

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
    p.map(partial(get_splits, wdir=wdir), open(glob.glob(f"{wdir}/urls/*")[0],"r").read().split())
    #p.map(partial(map_, wdir=wdir), os.listdir(f"{wdir}/splits/"))
    for split in os.listdir(f"{wdir}/splits/"):
      map_(split, wdir)
    return True
  if sys.argv[1] == "--shuffle":
    for f in os.listdir(f"{wdir}/maps/"): #looping avoids memory saturation
      shuffle0_(f, wdir)
    list(map(lambda x: x.communicate(), [shuffle1_(shuffle, wdir) for shuffle in glob.glob(f"{wdir}/shuffles/*")]))
    return True
  if sys.argv[1] == "--reduce":
    dict_ = Counter()
    p = Pool()
    result = p.map(partial(reduce0_, machines=open(f"{wdir}/machines.txt","r").read()), glob.glob(f"{wdir}/shufflesreceived/*"))
    [dict_.update(x) for x in result]
    open(f"{wdir}/reduces/{socket.gethostname()}.txt", "w").writelines([f"{k} {v}\n" for k, v in dict_.most_common()])#sorted(dict_.items(), key = lambda x: (-x[1],x[0]))])
    return True

if __name__ == '__main__':
  main()