### Dockerfile에 의해 이미지에 합쳐짐

import sys
import mapreduce
import pickle

if len(sys.argv) != 3:
    # 들어오는 인자가 3개(파일이름, start, end)가 아닌 경우 에러 발생
    raise Exception("Arg num must be 2(index)")
else:
    start = int(sys.argv[1])
    end = int(sys.argv[2])

    with open("intermediate.bin","rb") as file:  # 중간 데이터를 받아옴
        intermediate = pickle.load(file)
    
    result = []
    for i in range(start, end):                  # start부터 end-1까지의 (key, list(value)) 데이터에 reduce를 적용하고 모음
        result.append(mapreduce.reduce(intermediate[i][0], intermediate[i][1]))

    print(result)  # 결과 출력