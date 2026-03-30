# HackerLogin CTF Challenge Template

이 문서는 HackerLogin CTF 문제 출제를 위한 저장소 생성, 작업 방식, 제출 규칙을 정의합니다.

이 템플릿 저장소는 **문제별 private Repositories 생성**을 전제로 합니다.  

---

## 1. 작업 방식

출제자는 이 템플릿을 기반으로 **자신의 private 저장소를 생성**한 뒤 작업합니다.

- 문제 이름: 영어로 시작해야 하며, 영어 대소문자, 숫자, _ (언더스코어)만 사용해야 합니다. 문제 이름은 중복될 수 없습니다.

>예:
> `Phantom_Signal`

이 방식의 목적은 다음과 같습니다.

- 출제자 간 문제 접근 분리
- 다른 출제자 문제 열람 방지
- 문제별 리뷰 및 관리 단순화

---

## 2. 저장소 생성 절차

1. 템플릿 repository를 기반으로 새 private repository를 생성합니다.
2. repository 이름은 문제명을 기준으로 작성합니다.
3. 출제자는 자신의 repository에서 문제를 개발합니다.

---


### 필수 구성

```text
problem/
├─ Description.md
├─ Specfile
├─ public/
└─ private/
```

### 선택 구성
문제 구현 방식에 따라 아래 파일/디렉토리를 추가할 수 있습니다.

- Dockerfile : 단일 컨테이너 문제
- docker-compose.yaml : 멀티 컨테이너 문제
- web/, db/, scripts/, common/ 등 구현에 필요한 추가 디렉토리
- 기타 실행/배포에 필요한 파일

단, 아래 원칙을 반드시 지켜주세요.

## 3. 제출 원칙

#### 1. 참가자 제공 파일   
- 참가자에게 제공할 파일은 public/만 포함하는 것을 원칙으로 합니다.

    + 문제 바이너리
    + 소스코드 일부
    + 첨부파일
    + 공개 가능한 힌트 자료   

#### 2. 비공개 파일   
- 다음과 같은 민감한 자료는 private/ 또는 비공개 경로에만 보관해야 합니다.

    + 플래그
    + 풀이 코드 / writeup
    + 배포용 secret
    + 서버 전용 데이터
    + 운영용 설정 파일   

#### 3. 추가 파일/디렉토리   

- 기본 템플릿은 최소 권장 구조입니다.
- 문제 구현에 필요한 경우 파일/디렉토리를 자유롭게 추가할 수 있습니다.

> Ex:   
>   > web/   
>   > db/   
>   > scripts/   
>   > common/   

다만 구조가 과도하게 복잡하지 않도록 하고, 역할이 명확해야 합니다.

#### 4. 불필요한 파일 제외   
- .gitignore을 활용하여 캐시/임시 파일은 저장소에 포함하지 마세요.   

```
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
```

+ .gitignore: 루트 디렉토리에 공통 .gitignore가 있습니다. 만약 특정 문제 폴더에만 적용되어야 하는 규칙이 있다면, 해당 문제 폴더 내에 .gitignore 파일을 개별적으로 작성합니다.

---

자세한 작업 흐름은 아래 노션 링크를 참고해주세요.

* [HackerLogin 신입생 선발 CTF 출제 양식](https://www.notion.so/hackerlogin/HackerLogin-CTF-32c40ccb644d80a88e44c07948120d8a?source=copy_link)
