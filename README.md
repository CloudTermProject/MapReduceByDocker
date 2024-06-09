# 최종 보고서

## 프로젝트명 

Map-Reduce와 Docker를 이용한 word counter

## 멤버이름, 멤버별 담당 파트 

- 조승현: 통신규약 정하기, Mapper 구현, Master 구현, Auto-Scaling 구현, 최종 결과물 동영상 촬영
- 조수현: 통신규약 정하기, Mapper 구현, Master 구현, Auto-Scaling 구현, 최종 결과물 PPT 제작
- 김정민: 통신규약 정하기, Mapper 구현, Reducer 구현, Auto-Scaling구현, 최종 보고서 작성
- 김지훈: 통신규약 정하기, Mapper 구현, Reducer 구현, Auto-Scaling구현, 최종 결과물 소스코드 작성

## 프로젝트 소개

맵 리듀스 기술과 도커 컨테이너 기술을 이용한 word counter 서비스이다.

사용자에게서 입력받은 대용량 파일(txt파일)에서 한 번이라도 출현하는 word들을 추출하고, 각각의 빈도를 짝지어 튜플(tuple)로 출력하는 시스템 구현에 목적을 둔다. '맵리듀스(MapReduce)'알고리즘과 auto-scaling 메커니즘을  도커 컨테이너로 구현한 것이 특징이다.

# 프로젝트 필요성 소개

현대 사회에서는 점점 더 큰 대용량 데이터를 처리하는 것을 요구하는 서비스가 많아지고 있다. 가령 AI 기술에서는 자연어 처리 과정에서 텍스트 데이터를 처리하고 분석하는 과정에서 텍스트를 토큰화 하고 정규화 하는 과정 등에서 대용량 텍스트를 다룰 수 있어야하며, 빅데이터 분석 기술 또한 대용량의 텍스트 데이터를 효율적으로 처리하고 분석함으로써 AI 알고리즘에 필요한 대규모의 학습 데이터를 요구한다. AI 기술 뿐만 아니라 대용량 데이터를 처리를 요구하는 곳은 점점 더 늘어나고 있다. 이 시스템을 이용하면 대용량 데이터 중 word 파일, txt 파일을 효율적으로 분석, 처리할 수 있게 해준다.

이 시스템은 사용자의 input file 과 map function, reduce function을 입력 받는다. 이 데이터를 map reduce를 이용해 분석한 뒤, 찾고자 하는 word(key)와 그 빈도 수(value) 쌍을 도출한다.

기존의 상업화된 프로그램 등은 컨테이너를 사용하지 않았기 때문에 클라우드 환경에서의 확장성이 부족하다. 본 시스템은 이를 극복하고, 도커를 이용한 오토스케일링과 map reduce 기술의 연계로 실행속도, 배포 협업의 편리함 측면에서 향상된 성능을 보여 줄 수 있는 가능성을 보여주는 점에서 의의를 찾을 수 있다.

실제 사례에서 이 시스템을 이용한다면, 가령 기업이 대규모의 고객 피드백 데이터를 다루고 있고, 이를 분석하여 제품에 대한 고객의 관심사를 파악하고자 할때, 피드백 데이터를 효율적으로 처리하고 각 단어의 빈도를 계산할 수 있을 것이다.

# 관련 기술 / 논문 / 특허 조사 내용

1) 기술
- Hadoop
  - 설명: 아파치 하둡(Apache Hadoop)은 오픈 소스 분산 컴퓨팅 프레임워크로, MapReduce 모델을 기반으로 하둡 분산 파일 시스템(HDFS)과 함께 대용량 데이터 처리에 사용됩니다.
  - 특징: 오픈 소스, HDFS를 통해 고가용성 데이터 저장, YARN을 통한 리소스 관리, 다양한 데이터 형식의 지원 (CSV, JSON, Parquet, Avro 등)

- Spark
  - 설명: 아파치 스파크(Apache Spark)는 메모리 기반의 분산 데이터 처리 엔진으로, MapReduce 모델을 확장하여 인메모리 컴퓨팅을 통한 빠른 데이터 처리를 지원합니다.
  - 특징: 배치 및 스트리밍 데이터 처리 통합, 인메모리 컴퓨팅을 통한 빠른 데이터 처리, 다양한 언어 지원 (Java, Scala, Python, R)

- Dyrad
  - 설명: 마이크로소프트의 Dryad는 MapReduce와 유사한 데이터 병렬 처리 프레임워크로, DAG(Directed Acyclic Graph) 기반의 작업을 분산 환경에서 병렬로 처리합니다.
  - 특징: DAG 기반의 데이터 흐름, 다양한 데이터 소스와의 연동, LINQ 언어 지원

2) 논문 
- Dean, Jeffrey, and Sanjay Ghemawat. "MapReduce: simplified data processing on large clusters." *Communications of the ACM* 51.1 (2008): 107-113

- Shvachko, Konstantin, Hairong Kuang, Sanjay Radia, and Robert Chansler. "The Hadoop distributed file system." 2010 IEEE 26th symposium on mass storage systems and technologies (MSST). IEEE, 2010.

- Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, Ankur Dave, Justin Ma, Murphy McCauley, Michael J. Franklin, Scott Shenker, Ion Stoica. “Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing”

- Zaharia, Matei, Mosharaf Chowdhury, Michael J. Franklin, Scott Shenker, and Ion Stoica. "Spark: Cluster computing with working sets." Proceedings of the 2nd USENIX conference on Hot topics in cloud computing. Vol. 10. 2010

- Isard, Michael, Mihai Budiu, Yuan Yu, Andrew Birrell, and Dennis Fetterly. "Dryad: distributed data-parallel programs from sequential building blocks." ACM SIGOPS operating systems review 41, no. 3 (2007): 59-72.

3) 특허
- US Patent 7650331 B1: Jeffrey Dean, Sanjay Ghemawat, "System and method for efficient large-scale data processing," filed December 21, 2007.

# 프로젝트 개발 결과물 소개

시스템의 전체 구조도는 다음과 같다.

<div align="center">
  <img src="https://github.com/CloudTermProject/MapReduceByDocker/assets/49471288/f317fe9a-f888-4e69-83cc-a2980f53705a" width="800px" />
</div>

프로그램 시작 후, map container와 Reduce Container를 생성하기 위한 도커이미지가 존재하는지 확인하고, 없다면 새로 생성한다.

지정된 경로에 있는 txt파일에 접근하여, input data를 나눈다. 파일 크기를 읽어서 미리 정해진 크기만큼 나누는데, 나누는 경계 지점에 단어가 있으면 손상될 수 있기 때문에, 가까운 공백으로 경계를 옮김으로써 이를 방지한다.
Map을 수행할 컨테이너들을 생성한다. 매개변수로는 input data의 경로와 해당 컨테이너가 그 input data안에서 읽어야할 offset 정보를 준다. 또한 detach=True를 전달해 background에서 돌아가도록하고, 현재 폴더에 마운트까지 해준다.
Map container에서는 mapper.py가 실행된다.

map container를 모두 실행한 후에, master.py에서는 각 컨테이너로부터 출력값을 기다린다. 각 컨테이너의 logs()를 호출해서 eval을 통해 값을 받은뒤, 이를 intermediate 변수에 저장한다.

<div align="center">
  <img src="https://github.com/CloudTermProject/MapReduceByDocker/assets/49471288/f40278be-dda6-4750-b800-b0f27b136526" width="800px" />
</div>


모든 map 컨테이너의 결과 값을 받아왔다면, intermediate 데이터를 정렬한 뒤, 갯수에 맞게 reduce container를 생성하여 key, list(value)를 전달한다. 


매개 변수를 전달 받은 reduce 컨테이너는 reducer.py를 수행한다. master에서 모든 출력값을 기다린후, 출력이 끝나면 이를 하나로 모아 정렬해 결과를 출력한다. 



이를 플로우 차트로 나타내면 다음과 같다.

<div align="center">
  <img src="https://github.com/CloudTermProject/MapReduceByDocker/assets/49471288/956ab79c-8737-4e84-9dc3-ead39db13ece" width="500px" />
</div>





# 개발 결과물을 사용하는 방법 소개

1. 사용자는 분석하고 싶은 txt파일을 프로젝트 src폴더에 업로드한 후 master.py의 input path를 수정한다.
2. 프로젝트 최상위 디렉토리에서 python3 src/master.py 로 master.py를 실행한다. (import docker에서 막히는 경우, pip install docker를 통해 라이브러리를 설치해야 할 수 있음)
3. 실시간으로 도커 컨테이너가 실행되고 있는 환경이 출력된다. 
4. 수행하는 컨테이너들이 완수되면, txt파일의 모든 단어들이 빈도 수와 함께 튜플로 출력된다.
5. 컨테이너에서 실행되는 파일(mapper.py, reducer.py) 를 수정해야하는 경우, 기존에 만들어진 mapreduceimg 이미지를 도커에서 삭제해야함. (삭제 후 master.py를 실행하면 재빌드 됨.)

# 개발 결과물 활용 방안 소개

본 프로그램의 핵심은 대용량 파일을 도커를 이용한 오토 스케일링을 이용해 향상된 속도로 분석할 수 있다는 것이다.
전술한 것과 같이, 기존의 시스템은 컨테이너를 사용하지 않았기 때문에 클라우드 환경에서의 확장성이 부족하다. 따라서 클라우드 환경을 적극 활용하여 word counter 더 나아가 map reduce를 활용하는 기술을 구현하고자 하는 기업에게는 이 프로젝트의 결과물이 큰 도움이 될 것이다. 

또한 오토스케일링을 잘 수행하기 때문에, 타임 리밋이 있는 프로젝트 개발에 본 프로젝트의 시스템 구조를 활용하여 개발한다면 도움이 될 것이다. 

본 프로젝트의 본질인 word counter 기술을 이용해, 자연어 처리 모델 등의 학습 시키기 위한 대규모 텍스트 데이터를 전달하여, 빈도 높은 단어를 파악하여 토큰화, 정규화 과정에 활용할 수 있다. 이는 AI 기술이 발전하는 현 시대에 효용성있는 서비스라고 할 수 있다.
