# 현재 브랜치로 나누어서 작업중입니다. 브랜치 확인해주시면 감사하겠습니다!

### Docker SDK로 구현
Docker sdk를 이용해서 간단하게 구현해보았습니다.

어떤 통신 방식을 사용하기보단 디렉토리 공유/파일 위주로 일단 한번 해봤습니다...

단어 빈도 측정은 아래에 언급할 문제점 때문에 거의 불가능해서 일단 단어의 첫 알파벳 빈도 측정으로 map과 reduce를 설정했습니다.

master.py를 실행시키면 됩니다.

### 동작 방식
참고) master.py는 컨테이너에서 돌아가지는 않습니다..

1. master에서, map과 reduce에 필요한 containter의 이미지가 이미 있는지 확인합니다. 만약 없으면 Dockerfile을 이용해 새로 build합니다.

2. input data를 나눕니다. 이때 input data는 단어로만 이루어진 파일로 가정하였습니다. 파일 크기를 읽어서 미리 정해진 크기만큼 나누는데, 나누는 경계 지점에 단어가 있으면 손상(갈라지기)될 수 있으니까 이때는 가까운 공백으로 경계를 옮깁니다. 그러면 input data를 어느 지점에서 나눌 지에 대한 offset list가 나옵니다.

3. Map을 수행할 컨테이너를 생성합니다. 파라미터로 input data의 경로와 해당 컨테이너가 읽어야 할 offset 정보를 제공합니다. 또한 detach=True로 설정해 background에서 돌아가도록 하고, 현재 폴더를 마운트합니다.

4. 각 map container에서는 mapper.py이 실행됩니다. 그러면 mapreduce.py 모듈을 참고하여 map function을 input data(쪼개짐)에 적용시키고, 이를 출력합니다.

5. 다시 master에서는, map 컨테이너를 모두 실행한 후에, 각 컨테이너로부터 출력값을 기다립니다. 이는 컨테이너의 logs()를 호출하면 알 수 있는데, 출력이 없는 경우 빈 문자열이지만 출력이 있으면 그것을 리턴합니다. 이것을 받아 eval을 수행해 값을 받은 뒤, 중간 데이터 intermediate에 저장합니다.(dictionary 타입이라, key에 맞게 잘 정리됩니다)

6. 모든 map 컨테이너에서 값을 받아왔다면, intermediate 데이터를 정렬한 뒤, 갯수에 맞게 reduce container를 생성하여 (key, list(value))값을 전달해야 합니다. (이건 마땅한 방법이 생각나지 않아 일단 dump를 뜨는 방식을 사용)

7. reduce를 수행할 컨테이너를 생성하고, 인자로 자신이 처리해야 하는 중간데이터 list의 index를 전달해줍니다.

8. 그러면 컨테이너에서는 reducer.py를 수행하면서 reduce 작업을 수행합니다. 마찬가지로 mapreduce.py를 참고해 reduce를 수행합니다.

9. map container때와 마찬가지로, master에서 모든 컨테이너에 대해 출력값을 기다립니다. 모든 컨테이너의 출력이 끝나면, 이를 하나로 모아 정렬해 결과를 출력합니다.


### 문제점
컨테이너 생성이 너무 느립니다. 0.5초 정도 간격을 두고 생성되는 바람에 중간 데이터에서 key가 엄청 많이 생성되면, 컨테이너도 너무 많이 생성되고 시간도 너무 오래 걸리게 됩니다. (특히 온전한 단어의 경우.)

map container의 개수 같은 경우는 input file의 크기와 split 크기를 조절하면 제어 가능하지만 reduce container의 경우 어떤 key가 나올 지 모르기 때문에, 좋은 방법을 생각해 봐야 할 것 같습니다. (컨테이너를 미리 실행시킨다거나, 기존에 있던 것을 재활용한다거나?)

하나의 컨테이너가 하나의 map/reduce작업만 수행하기엔 자원이 너무 아까우니까 여러 개의 map/reduce 작업을 시키는 것도 괜찮은 것 같습니다. (master가 작업을 잘 분배하게 해서...)




![pingu](https://github.com/CloudTermProject/MapReduceByDocker/assets/104819783/eb8a9520-8ee9-44b0-8113-298b1ce9eae8)