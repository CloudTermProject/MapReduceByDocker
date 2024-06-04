### 여기에 map, reduce function 정의하기.

#map
#(value가 string으로 주어지는 경우)
def map(key, value):
    d = []
    for word in value.strip().split():
        d.append((word, 1))
    return d

#reduce
def reduce(key, value): 
    return key,sum(value)