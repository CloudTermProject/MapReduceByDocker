### 여기에 map, reduce function 정의하기.

#map function
def map(key, value):     
    return map_headcount(key,value)

#reduce function
def reduce(key, value): 
    return reduce_headcount(key, value)

#--------------------------------------------#
# 단어의 빈도 확인하기
def map_wordcount(key, value):  # string으로 주어지는 value에서 단어의 등장 횟수를 체크
    d = []
    for word in value.strip().split():
        d.append((word, 1))
    return d
def reduce_wordcount(key, value): # 각 key(단어)마다 등장 횟수([1,1,1,1,]과 같은 형태)를 더함
    return key, sum(value)

# 단어의 앞글자 빈도 확인하기
def map_headcount(key, value):
    d = []
    for word in value.strip().split():
        d.append((word[0],1))
    return d
def reduce_headcount(key, value):
    return key, sum(value)

# 단어의 길이 빈도 확인하기
def map_lencount(key, value):
    d = []
    for word in value.strip().split():
        d.append((len(word),1))
    return d
def reduce_lencount(key, value):
    return key, sum(value)

# 단어 길이가 2 이하인 것들만 모으기
def map_len2(key, value):
    d = []
    for word in value.strip().split():
        if len(word) <= 2:
            d.append((word,1))
    return d
def reduce_len2(key, value):
    return key

# 알파벳 빈도 파악하기
def map_alphabetcount(key, value):
    d = []
    for word in value.strip().split():
        for alphabet in word:
            if alphabet.isalpha():
                d.append((alphabet, 1))
    return d
def reduce_alphabetcount(key, value):
    return key, sum(value)