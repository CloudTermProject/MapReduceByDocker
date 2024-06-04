### Dockerfile에 의해 이미지에 합쳐짐

import sys
import mapreduce
import pickle

if len(sys.argv) != 3:
    raise Exception("Arg num must be 2(index)")
else:
    start = int(sys.argv[1])
    end = int(sys.argv[2])

    with open("intermediate.bin","rb") as file:
        intermediate = pickle.load(file)
    
    result = []
    for i in range(start, end):
        result.append(mapreduce.reduce(intermediate[i][0], intermediate[i][1]))

    print(result)