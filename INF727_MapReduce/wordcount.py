import sys
import time

def build_dict(filename):
  f = open(filename,'r',encoding='utf8').readlines()
  dict_ = {}
  for l in f:
    for word in l.split():
      if word in dict_:
        dict_[word] += 1
      else:
        dict_[word] = 1
  return dict_

def print_words(filename):
  dictimes = {}
  dictimes["file"] = filename
  t0 = time.time()
  t1 = time.time()
  dict_ = list(build_dict(filename).items())
  t2 = time.time()
  dictimes["count"] = t2-t1
  t1 = time.time()
  dict_.sort(key = lambda x: (-x[1],x[0]))
  t2 = time.time()
  dictimes["sort"] = t2-t1
  for k, v in dict_[:10]: #filtering only first 10
    print(k, v)
  open("output.txt","w",encoding="utf8").writelines([f"{k} {v}\n" for k,v in dict_])
  dictimes["final"] = time.time() - t0
  open("exps/experimentslocal.csv","a",encoding="utf8").writelines([f"{v}," for _,v in dictimes.items()]+["\n"])
  return True

def main():
  if len(sys.argv) != 2:
    print('usage: ./wordcount.py file')
    sys.exit(1)
  filename = sys.argv[1]
  print_words(filename)

if __name__ == '__main__':
  main()
