
### 장고 설치
```shell
$ pip install django
```
가상환경(venv)에서 장고 설치


### 장고로 만든 웹사이트의 작동 구조
장고 프레임워크에서는 MVT 패턴을 따른다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FpdQ3m%2FbtqwhTpC3gU%2FvXB2IGfXViX7cGFQgXjlR1%2Fimg.png)

 - `Model`로 자료의 형태를 정의
 - `View`로 어떤 자료를 어떤 동작으로 보여줄지 정의
 - `Tamplate`으로 웹 페이지에서 출력할 모습을 정의

이러한 작동구조는 [MVT 패턴](https://butter-shower.tistory.com/49)이라고 부르며 [MVC 패턴](https://velog.io/@seongwon97/MVC-%ED%8C%A8%ED%84%B4%EC%9D%B4%EB%9E%80)과 유사하다.

### Views를 처리하는 방법

장고는 원래 함수형 뷰(FBV)만 사용하였는데,
확장성과 커스터마이징의 편의를 위해 클래스형 뷰(CBV)가 탄생 했습니다.

[FBV vs CBV (함수형 뷰 vs 클래스형 뷰)](https://leffept.tistory.com/318)

>The Newer is often better, not always.

