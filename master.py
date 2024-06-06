
import docker
import os
import string

client = docker.from_env()
cwd = os.getcwd()                # Current Working Directory
inputpath = "./bible.txt"        # input 파일
split_size = 800000             # 한 컨테이너에서 처리할 단위.(byte)

#-------- dockerfile image build ------#

if len(client.images.list("mapreduceimg")) == 0: #만약 mapreduce를 위한 image가 없는 경우
    client.images.build(path=cwd,tag="mapreduceimg")  #새로 만들기

# ------------ Splitting --------------#
# input data가 어떤 단어인 경우, 입력파일을 나눌 때 단어가 쪼개지지 않아야 한다.

offsets = [0]
with open(inputpath,"r") as file:
    filesize = file.seek(0,2) # 파일의 총 크기

    for i in range(split_size, filesize,split_size):
        file.seek(i, 0)  # 경계로 감
        peek = file.read(1) # 경계 글자를 읽음
        while(peek not in string.whitespace): # 그것이 공백이 아닐 때까지 계속 읽음
            peek = file.read(1)
        offsets.append(file.tell()) # 문자가 공백일 때의 offset을 기록

offsets.append(filesize)
#print(offsets)

# ------------ Create Map Containers --------------#

split_num = len(offsets) - 1
mapcontainers = []                  # 실행된 컨테이너의 정보
complete = [False] * split_num      # 실행 완료된 컨테이너 목록
complete_n = 0                      # 실행 완료된 컨테이너의 수
intermediate = {}                   # 중간 데이터

print("Map Container")
for i in range(split_num):
    argv = " {} {} {}".format(inputpath,offsets[i], offsets[i+1])  # offset 전달
    mapcontainers.append(client.containers.run("mapreduceimg","python3 mapper.py"+argv,detach=True, volumes=[cwd+':/home/python/src']))
    print(mapcontainers[i])

# ------------ Shuffle & Sorting -----------------#

while(complete_n != split_num):
    for i in range(len(mapcontainers)):
        if complete[i] == False and mapcontainers[i].logs() != b'': # 무언가 print된 경우
            resultlist = eval(mapcontainers[i].logs()) # 결과(list string)을 list로 변환.
            for pair in resultlist:    # list를 intermediate dictionary에 정리 (Shuffle)
                if pair[0] in intermediate.keys():
                    intermediate[pair[0]].append(pair[1])
                else:
                    intermediate[pair[0]] = [pair[1]]
            complete[i] = True
            complete_n += 1

intermediate = sorted(intermediate.items())  # Sorting과 동시에 list(key, list(value)) 형태로 변환

#...
import pickle
with open("intermediate.bin",'wb') as file:
    pickle.dump(intermediate, file)

# ----------- Create Reduce Container ------------#
reduce_num = 5 #len(intermediate)

key_num = len(intermediate)

ind = list(range(0,key_num,key_num // reduce_num + 1))
ind.append(key_num)

reducecontainers = []

print("Result Container")
for i in range(reduce_num):
    argv = " {} {}".format(ind[i],ind[i+1])
    reducecontainers.append(client.containers.run("mapreduceimg","python3 reducer.py "+argv,detach=True,volumes=[cwd+':/home/python/src']))
    print(reducecontainers[i])
    
#----------- Result -------------#
complete = [False] * reduce_num
complete_n = 0
result = []

while(complete_n != reduce_num):
    for i in range(len(reducecontainers)):
        if complete[i] == False and reducecontainers[i].logs() != b'': 
            result.extend(eval(reducecontainers[i].logs())) # 결과.
            complete[i] = True
            complete_n += 1

result.sort(key=lambda x : x[0])
print(result)


# 다 쓴 (종료된)컨테이너 삭제
client.containers.prune()