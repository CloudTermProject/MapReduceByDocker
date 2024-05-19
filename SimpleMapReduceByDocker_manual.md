# Map-reduce를 이용한 word counter

master container 없이, map container와 reduce container를 각 1개씩 사용하여 word count 기능을 간단하게 구현하는 과정을 기술해 보았다.


## 1. 구현 과정

### 1. 디렉토리 생성
```
mkdir mapreduce
cd mapreduce
mkdir input output map reduce
```

### 2. map 디렉토리에서 “map.py” 작성, Dockerfile 작성, Docker 이미지 생성
- map.py
```
import sys

def map_function():
    for line in sys.stdin:
        words = line.strip().split()
        for word in words:
            print(f"{word}\t1")

if __name__ == "__main__":
    map_function()
```

- Dockerfile (파일 이름을 "Dockerfile"로 지정)
```
FROM python:3.8-slim

WORKDIR /app

COPY map.py .

ENTRYPOINT ["python", "/app/map.py"]
```

- 이미지 생성(map)
```
docker build -t map-container .
```


### 3. reduce 디렉토리에서 “reduce.py” 작성, Dockerfile 작성, Docker 이미지 생성
- reduce.py
```
import sys

def reduce_function():
    current_word = None
    current_count = 0

    for line in sys.stdin:
        word, count = line.strip().split('\t', 1)
        count = int(count)

        if current_word == word:
            current_count += count
        else:
            if current_word:
                print(f"{current_word}\t{current_count}")
            current_word = word
            current_count = count

    if current_word == word:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    reduce_function()
```

- Dockerfile
```
FROM python:3.8-slim

WORKDIR /app

COPY reduce.py .

ENTRYPOINT ["python", "/app/reduce.py"]
```

- 이미지 생성
```
docker build -t reduce-container .
```

### 4. input 데이터 생성
- input 디렉토리에서 vi input.txt -> 원하는 문자열 입력

### 5. map 함수 실행 (mapreduce 디렉토리에서 실행)
```
docker run -it --entrypoint /bin/sh -v $(pwd)/input:/input -v $(pwd)/output:/output map-container -c "python /app/map.py < /input/input.txt > /output/output.txt && cat /output/output.txt"
```

- map-container의 /input에 “$(pwd)/input” 폴더를 마운트, map-container의 /output에 “$(pwd)/output” 폴더를 마운트
- map.py 스크립트를 실행하면서 컨테이너 내부의 /input/input.txt 파일을 입력으로 받고, 결과를 /output/output.txt 파일에 저장
- map 실행 결과는 output.txt에 저장됨

### 6. Shuffling, Sorting (mapreduce 디렉토리에서 실행)
```
cat output/output.txt | sort > output/reduce_input.txt && cat output/reduce_input.txt
```

- output.txt에 저장된 데이터를 sorting 하여 reduce_input에 저장

### 7. reduce 함수 실행 (mapreduce 디렉토리에서 실행)
```
docker run -it --entrypoint /bin/sh -v $(pwd)/output:/output reduce-container -c "python /app/reduce.py < /output/reduce_input.txt > /output/final_output.txt && cat /output/final_output.txt"
```

- reduce 실행 결과는 final_output에 저장됨

### 8. 결과 확인
- output에서 final_output 파일을 확인

---
## 2. 실행 예시

- input.txt
```
abc
xyz
xyz
abc
abc
hello
abc
hi
abc
hello
```

map-reduce를 진행한 후, word count의 결과를 담고 있는 final_output 파일의 내용은 아래와 같다.

- final_output.txt
```
abc     5
hello   2
hi      1
xyz     2
```
