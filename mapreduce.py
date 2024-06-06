### 여기에 map, reduce function 정의하기.

#map function
def map(key, value):     # string으로 주어지는 value에서 단어의 등장 횟수를 체크
    d = []
    for word in value.strip().split():
        d.append((word, 1))
    return d

#reduce function
def reduce(key, value):  # 각 key(단어)마다 등장 횟수([1,1,1,1,]과 같은 형태)를 더함
    return key, sum(value)