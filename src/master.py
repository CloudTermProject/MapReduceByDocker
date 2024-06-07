
import docker
import os
import string
import math
import pickle


client = docker.from_env()       # Docker 연결
cwd = os.getcwd()                # Current Working Directory

#------------- parameters -------------#
inputpath = "./data_bible.txt"     # input 파일
split_size = 800_000                  # 한 컨테이너에서 처리할 단위.(byte)
max_reduce_num = 4                # 생성할 최대 reduce 컨테이너의 수(원하는 만큼 생성되지 않을 수 있음)


#-------- dockerfile image build ------#

if len(client.images.list("mapreduceimg")) == 0: #만약 mapreduce를 위한 image가 없는 경우
    client.images.build(path=cwd,tag="mapreduceimg")  #새로 만들기

# ------------ Splitting --------------#
# input data가 단어들의 집합인 경우, 입력파일을 나눌 때 단어가 쪼개지지 않아야 한다.
# 만약 나누는 point가 단어 쪼갠다면, 가까운 다음 공백으로 옮긴다.

offsets = [0]
with open(inputpath,"r") as file:
    filesize = file.seek(0,2) # 파일의 총 크기

    for i in range(split_size, filesize,split_size):
        file.seek(i, 0)  # 경계로 감
        peek = file.read(1) # 경계에 해당하는 글자를 읽음
        while(peek not in string.whitespace): # 그것이 공백문자가 아니라면, 파일을 계속 읽어 공백문자를 찾음.
            peek = file.read(1)
        offsets.append(file.tell()) # 공백문자를 찾으면 그 offset을 기록

offsets.append(filesize) # 파일의 끝도 포함
#print(offsets)

# ------------ Create Map Containers --------------#
# Map container를 생성하고, 각자 파일의 어떤 부분을 읽고 처리해야 하는지 전달한다.

split_num = len(offsets) - 1        # 파일을 몇 개로 나누는지(map container의 수와 동일)
mapcontainers = []                  # map 컨테이너의 정보
complete = [False] * split_num      # 실행 완료된 컨테이너 목록
complete_n = 0                      # 실행 완료된 컨테이너의 수
intermediate = {}                   # 중간 데이터

print("Creating Map Container...")
for i in range(split_num):
    argv = " {} {} {}".format(inputpath,offsets[i], offsets[i+1])                     # 파일 경로와, 읽어야 할 파일의 위치(offset) 전달
    mapcontainers.append(client.containers.run("mapreduceimg",                        # mapreduce를 수행하는 컨테이너 이미지
                                               "python3 mapper.py" + argv,            # 컨테이너마다 mapper.py를 실행하고 argv를 전달
                                               detach=True,                           # 백그라운드 모드에서 동작
                                               volumes=[cwd+':/home/python/src']))    # 현재 디렉토리를 볼륨 마운트 시킴
    print(mapcontainers[i])        # 백그라운드 모드에서 실행할 시, client.containers.run()의 결과는 container id를 나타냄.


# ------------ Shuffle & Sorting -----------------#
# Map container의 실행 결과물을 같은 key끼리 모은 뒤 정렬한다.

while(complete_n != split_num):              # 모든 컨테이너가 실행 완료 될때까지 반복
    for i in range(len(mapcontainers)):      # 만들어진 모든 map 컨테이너를 확인
        
        # 만약 완료되지 않은 컨테이너에 log가 찍혀 있는 경우, 컨테이너 수행이 완료되었음을 의미
        if complete[i] == False and mapcontainers[i].logs() != b'':
            # map container의 반환값은 항상 list를 표현한 문자열임. "[(key, value), (key, value),...]"
            # 따라서 list가 아닌 경우, 에러를 발생시킴.
            if chr(mapcontainers[i].logs()[0]) != "[":      # 문자열의 가장 앞이 대괄호가 아니면 에러로 간주.
                raise Exception(mapcontainers[i].logs().decode())
            
            resultlist = eval(mapcontainers[i].logs())      # 결과(list string)을 list로 변환.

            for pair in resultlist:                         # list를 intermediate dictionary에 정리 (Shuffle)
                if pair[0] in intermediate.keys():          # 만약 해당 key가 있다면, key에 해당하는 list에 추가
                    intermediate[pair[0]].append(pair[1])   
                else:                                       # key가 없다면, 새로 key를 만들고 그에 해당하는 list도 생성
                    intermediate[pair[0]] = [pair[1]]

            complete[i] = True     # 현재 컨테이너를 실행완료로 체크
            complete_n += 1        # 완료된 컨테이너 수를 하나 증가


# 모든 map container가 실행 종료되고, intermediate 데이터가 완성되었으므로 이를 정렬(Sorting)
intermediate = sorted(intermediate.items())  # list(key, list(value))의 형태로 변환됨

# 중간 데이터(intermediate)를 reduce container에 넘겨주기 위해, 바이너리 파일에 그대로 덤프시킴.
with open("intermediate.bin",'wb') as file:
    pickle.dump(intermediate, file)


# ----------- Create Reduce Container ------------#
# Reduce container를 생성하고, 중간 데이터에서 어디부터 어디까지 reduce를 수행하는지 전달한다.
# 한 컨테이너에서 하나의 key에 대한 reduce만을 수행하는 것이 비효율적이라,
# 하나의 컨테이너에서 여러 개의 key에 대해 reduce를 수행한다.

key_num = len(intermediate)   # key의 갯수

if key_num == 0:
    print("There is no key data...")
    div = []
else:
    # key에 접근할 index를 max_reduce_num 개수만큼의 덩어리로 쪼갬
    # key의 개수가 적으면, 덩어리가 max_reduce_num 개수만큼 나눠지지 않기도 함.(넘지는 않음)
    # 즉 reduce container의 수가 max_reduce_num 이하일수도 있음
    div = list(range(0, key_num, math.ceil(key_num / max_reduce_num)))    
div.append(key_num)

reducecontainers = []            # reduce container id
print("Creating Reduce Container...")
for i in range(len(div) - 1):
    argv = " {} {}".format(div[i],div[i+1])                                             # 인자로, intermediate 데이터를 얼마나 처리해야하는지 전달
    reducecontainers.append(client.containers.run("mapreduceimg",                       # mapreduce를 수행하는 컨테이너 이미지
                                                  "python3 reducer.py" + argv,          # 컨테이너마다 reducer.py를 실행하고 argv를 전달
                                                  detach=True,                          # 백그라운드 모드에서 동작
                                                  volumes=[cwd+':/home/python/src']))   # 현재 디렉토리를 볼륨 마운트
    print(reducecontainers[i])


#----------- Result -------------#
complete = [False] * len(reducecontainers)    # 실행 완료된 (reduce) 컨테이너 목록
complete_n = 0                                # 실행 완료된 컨테이너 개수
result = []                                   # 결과를 저장할 list

while(complete_n != len(reducecontainers)):   # 모든 reduce container가 완료될 때까지 반복
    for i in range(len(reducecontainers)):    # 모든 reduce 컨테이너를 확인
        # 실행이 완료된 것 같다면(log에 무언가 찍히는 경우)
        if complete[i] == False and reducecontainers[i].logs() != b'': 
            # result container의 반환값도 항상 list를 표현하는 str임
            # 따라서 list가 아닌 경우 에러로 간주
            if chr(reducecontainers[i].logs()[0]) != "[":
                raise Exception(reducecontainers[i].logs().decode())
            
            result.extend(eval(reducecontainers[i].logs())) # 결과를 기록
            # 실행 완료된 컨테이너라고 기록
            complete[i] = True
            complete_n += 1

#최종 결과 출력
result.sort()
print(result)


# 다 쓰고 종료된 컨테이너 삭제
client.containers.prune()