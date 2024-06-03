### Dockerfile에 의해 이미지에 합쳐짐

import sys
import mapreduce
import pickle

if len(sys.argv) != 2:
    raise Exception("Arg num must be 1(index)")
else:
    index = int(sys.argv[1])

    with open("intermediate.bin","rb") as file:
        intermediate = pickle.load(file)

    print(mapreduce.reduce(intermediate[index][0], intermediate[index][1]))