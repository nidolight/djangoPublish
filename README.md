# Getting Started With Django

## 장고 설치
```shell
$ pip install django
```
가상환경(venv)에서 장고 설치


## 장고로 만든 웹사이트의 작동 구조
장고 프레임워크에서는 `MVT 패턴`을 따른다.

![MVT](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FpdQ3m%2FbtqwhTpC3gU%2FvXB2IGfXViX7cGFQgXjlR1%2Fimg.png)

 - `Model` : 자료의 형태를 정의
 - `View` : 어떤 자료를 어떤 동작으로 보여줄지 정의
 - `Tamplate`: 웹 페이지에서 출력할 모습을 정의

이러한 작동구조는 [MVT 패턴](https://butter-shower.tistory.com/49)이라고 부르며 [MVC 패턴](https://velog.io/@seongwon97/MVC-%ED%8C%A8%ED%84%B4%EC%9D%B4%EB%9E%80)과 유사하다.


## Views를 처리하는 방법
장고는 원래 `함수형 뷰(FBV)`만 사용하였는데,
확장성과 커스터마이징의 편의를 위해 `클래스형 뷰(CBV)`가 만들어짐

[FBV vs CBV (함수형 뷰 vs 클래스형 뷰)](https://leffept.tistory.com/318)

>The Newer is often better, not always.


## 장고의 tamplate 기능
HTML 은 기본적으로 정적인 언어이다.(작성 후 동적으로 무언가를 변경/수정 불가)<br>
`{% %}` , `{{ }}` 와 같은 구문을 통해 HTML 내에 동적인 구문을 삽입할 수 있다.<br>
공식문서 [참조](https://docs.djangoproject.com/en/3.2/topics/templates/#the-django-template-language)

 - {{ }} 와 같은 구문은 단순 변수 출력을 위해서 쓰는 태그
 - {% %} 와 같은 구문은 if, for 등 임의의 로직을 실행하기 위해 쓰이는 태그

---
## Bootstrap
### What is Bootstrap
- 웹 개발 시 일반적으로 쓰이는 구성 요소들을 미리 디자인 해둔 툴킷

### 일반적인 css의 적용 과정
1. 웹 브라우저(클라이언트)는 서버에 접속해 html 파일을 불러온다.
2. 해당 html 파일에 css 파일을 참조한다고 되어있다면 그 css 파일을 불러온다.
3. css 파일에 정의된 모양을 적용한 뒤 웹 프라우저 화면에 렌더링하여 출력한다.

### 장고에서의 MTV 구조
위에서의 일반적인 css의 적용 과정으로는 css파일 이 적용되지 않는다. 즉,
html파일이 있는 곳에 `bootstrap.min.css`파일을 넣어두면 적용 되지 않는다.

장고는 MTV 구조로 동작하기 때문에 앱 폴더(여기선 blog 폴더)에 있는 
templates 폴더의 html 파일은 정적인 파일이 아니므로 templates 폴더에 css,js 파일을 함꼐 넣어 두어도 해당 파일에 접근할 수 없다.

> css,js파일은 templates 폴더의 html 파일과 달리 고정된 내용만 제공하면 된다.<br>
> 따라서, 특정 URL로 접근을 하면 해당 css,js파일을 제공할 수 있도록 설정해 두면 된다.

→ static 폴더를 만들어 css,js와 같은 정적 파일을 저장

tip: 한 폴더 안에 저장하지 않고 여러 폴더로 내려가서 저장하도록 설정하면 서버에서 파일을 찾아오는 시간을 단축


## 테스트 주도 개발 - TDD
Test Driven Development(TDD)는 일종의 개발방식 또는 개발 패턴을 의미.<br>
개발하려는 항목에 대한 점검사항을 테스트 코드로 만들고 그 테스트를 통과시키는 방식으로 개발을 진행하는 방법<br>
모델의 구조가 복잡하고, 기능이 다양하고, 페이지도 많은 웹 사이트를 만들 때 효율적
장고에선 tests.py를 통해 관리

> 개발한 코드가 테스트를 만족하는지 자동으로 확인하면서 개발을 진행

1. 테스트 코드 작성 : 만들 기능을 점검할 코드 작성
2. 기능 구현 : 테스트 코드를 만족시킬 수 있게 기능을 구현
3. 리팩토링 : 코드 개선 및 테스트 코드로 다시 기능을 점검

### 테스트 코드 작성
TestCase를 이용한 테스트 방식은 실제 데이터베이스를 건들지 않고 가상의 데이터베이스를 새로 만들어 테스트한다.
따라서 이미 운영되고 있는 데이터베이스를 건들지 않고 테스트를 수행할 수 있다.

### beautiufulsoup4
테스트를 위해 HTML로 나타나는 페이지의 요소를 쉽게 다룰 수 있는 도구


## 템플릿 모듈화
메인 영역을 제외한 나머지 영역은 디자인이 일관되게 유지되어야 한다.<br>
템플릿 요소들을 모듈화하여 편하게 관리할 수 있다.

## 다대일 관계
여러 개의 모델이 하나의 모델에 연결되는 관계<br>
여기에선 포스트와 작성자의 관곋는 다대일이다. 포스트에 카테고리 정보를 추가할 떄도 마찬가지로 다대일 관계이다.
(하나의 카테고리에는 여러 개의 포스트가 포함됨, 한 포스트에는 하나의 카테고리만 지정 가능)<br>
→ 작성자 정보 하나에 여러 포스트를 연결하는 다대일 관계에는 ForeignKey(외래키)를 사용

