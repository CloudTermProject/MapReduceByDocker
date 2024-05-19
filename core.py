import pickle

class mapreduce():
    data = None
    map = None
    reduce = None
    result = None

    def run(self):
        # [Spiltting]
        # 데이터 나누기
        # 나눈 갯수만큼 컨테이너 할당하기
        

        # [Mapping]
        # 각 컨테이너에 쪼갠 데이터와 map 전달

        # (임시) 각 컨테이너에서 수행하게 될 작업들.(일단 하나만)
        res = self.map(None, self.data) 
        with open("shareddata/m1",'wb') as file:#이름 컨테이너마다 다르게.
            pickle.dump(res, file)
        
        # [Shuffling, Sorting]
        # 컨테이너에서 작업된 결과물을 가져와 정리
        intermediateData = {}

        # map 컨테이너 개수만큼 반복해야함(지금은 하나)
        with open("shareddata/m1", "rb") as file:
            m1 = pickle.load(file)
            for tuple in m1:
                if tuple[0] in intermediateData.keys():
                    intermediateData[tuple[0]].append(tuple[1])
                else:
                    intermediateData[tuple[0]] = [tuple[1]]

        # Sorting
        intermediateData = sorted(intermediateData.items())
        
        # [Reducing]
        # 중간 데이터 key 개수만큼 reduce 컨테이너 생성
        # 각 reduce 컨테이너에 (key, values)와 reduce function 전달.

        # (임시) 각 reduce 컨테이너마다 수행할 작업들
        for i in range(len(intermediateData)):
            res = self.reduce(intermediateData[i][0], intermediateData[i][1])
            with open("shareddata/r"+str(i),"wb") as file:
                pickle.dump(res, file)
        
        # [Result]
        self.result = []
        for i in range(len(intermediateData)):
            with open("shareddata/r"+str(i),"rb") as file:
                self.result.append(pickle.load(file))
                
        
# 실행 예시

# 데이터 (임의 3~7길이 영어단어)
somewords = "Apple Beach Cherry Dance Cat Dog Car Sun Hat Pen Box Key Bus Fan Jelly Knife Lemon Money Niece Onion Pearl Quest River Shine Blaze Table Uncle Voice Whale X-ray Yield Zebra Brush Climb Drink Earth Frost Ghost Heart Issue Joint Kiosk Light Mango Noise Oasis Paper Quiet Round Trust Bird Tree Book Ball Fish Rain Moon Bear Lamp Hand Blade Chore Drove Elbow Flute Grape Horse Inner Jolly Knack Latch Mirth North Olive Pivot Country Morning Blanket Bicycle Captain Curtain Diamond Glasses Journey Pumpkin Widen Zephyr Brisk Crave Drift Exert Flash Gloom Humor Infer Joust Kneel Ledge Mount Nurse Opine Plumb Quake Ratio Seize Trend Urban Value Whisk Zealot Blaze Shine Yearn Blaze Shine Yearn Blaze Shine Yearn Blaze Shine Yearn Blaze Shine Yearn Blaze Shine Yearn Blaze Shine Yearn"

# mapping 함수들
def mymap(key, value): # 단어 빈도 파악
    d = []
    for word in value.split(" "):
        d.append((word, 1))
    return d

def mymap2(key, value):  # 단어의 첫 번째 알파벳 갯수 파악
    d = []
    for word in value.split(" "):
        d.append((word[0], 1))
    return d

def mymap3(key, value): # 단어 글자 수 파악
    d = []
    for word in value.split(" "):
        d.append((len(word), 1))
    return d

def mymap4(key, value):
    d = []
    for word in value.split(" "):
        d.append((word[-2:], 1))
    return d

# reduce 함수들
def myreduce(key, value): 
    return key,sum(value)

def myreduce2(key,value):
    return key

if __name__ == "__main__":
    MR = mapreduce()
    MR.data = somewords
    MR.map = mymap
    MR.reduce = myreduce
    MR.run()

    result = MR.result
    print(result)

'''
단어 빈도 파악 : mymap, myreduce
단어의 첫 번째 알파벳 빈도 파악 : mymap2, myreduce
단어의 글자 수 파악 : mymap3, myreduce
단어의 마지막 2글자만 모으기 : mymap4, myreduce2

'''