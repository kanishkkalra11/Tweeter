import time
import os
from multiprocessing import Pool

def RUN(i):
    os.system("python client_" + str(i) +".py")
    return "Done"

if __name__ == "__main__":
    p = Pool(8)
    result = p.map(RUN, range(1,9))
    p.close()
    p.join()
