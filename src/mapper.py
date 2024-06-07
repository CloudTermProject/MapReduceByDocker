### Dockerfile에 의해 이미지에 합쳐짐

import sys
import mapreduce

if len(sys.argv) != 4:
    # 들어오는 인자가 4개(파일이름, path, start, end)가 되지 않는 경우 에러 발생시키기
    raise Exception("Arg num must be 3(path, start, end)")
else:
    path = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    
    with open(path,"r") as file:
        try:
            file.seek(start,0)                      # start 지점까지 이동 후,
            string = file.read(end-start)           # end-start 만큼 파일 읽어옴

            result = mapreduce.map(None, string)    # map을 실행 후,
            assert isinstance(result, list)         # 결과가 list가 아니면 assert 날리기

            print(result)                           # 결과 출력

        except AssertionError:
            print("Map function's return type is not list.")
