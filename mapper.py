### Dockerfile에 의해 이미지에 합쳐짐

import sys
import mapreduce

if len(sys.argv) != 4:
    raise Exception("Arg num must be 3(path, start, end)")
else:
    path = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    
    with open(path,"r") as file:
        file.seek(start,0)
        string = file.read(end-start)
        print(mapreduce.map(None, string))
