# 기여 가이드 (Contributing Guide)

이 문서는 CTF 문제 출제 및 관리를 위한 Git 워크플로우와 커밋 규칙을 정의합니다. 원활한 협업을 위해 아래 규칙을 준수해 주시길 바랍니다.

## 1. 브랜치 전략

### 개요

브랜치는 계층 구조를 가지며, 각 브랜치의 역할은 다음과 같습니다.

- main: 최종 배포/운영 브랜치. (실제 사용 가능한, 완전히 검수된 문제들)
- dev: 통합 개발 브랜치. (main으로 가기 전 검수 대기)
- problem/{문제이름}: 개별 문제 개발의 중심이 되는 통합 브랜치입니다.
- problem/{문제이름}/{기능}: 실제 코드를 수정하는 가장 작은 단위의 기능 브랜치입니다.

### 네이밍 규칙

- 문제 이름: 영어로 시작해야 하며, 영어 대소문자, 숫자, _ (언더스코어)만 사용 가능합니다.
    - (예: problem/Web_Login_Easy)
- 기능 이름: 브랜치의 목적을 명확히 알 수 있도록 간결하게 작성합니다.
    - (예: problem/Web_Login_Easy/add_dockerfile, problem/Pwn_Basic_BOF/fix_overflow)

### 작업 흐름

0. 레포지토리 포크
    - Github에서 fork를 통해서 자신의 레포지토리를 생성해 개발을 시작합니다.
    - 이 때 옵션에서 메인 브랜치만 포크하기를 해제하여 줍니다.

1. 문제 통합 브랜치 생성 (문제 개발 시작)
    - dev 브랜치에서 새로운 문제의 통합 브랜치를 분기합니다.
    - git switch dev
    - git pull origin dev
    - git switch -c problem/Pwn_Basic_BOF

2. 기능 브랜치 생성 (세부 기능 개발)
    - 생성한 problem/{문제이름} 브랜치에서 기능 브랜치를 분기합니다.
    - git switch problem/Pwn_Basic_BOF
    - git switch -c problem/Pwn_Basic_BOF/add_exploit_code

3. 커밋 (Commit)
    - 기능 브랜치에서 작업하며 Commit 메시지 규칙에 따라 커밋합니다.

4. Pull Request (PR)
    - 기능 → 문제 통합: 세부 기능 개발이 완료되면, 기능 브랜치를 problem/{문제이름} 브랜치로 PR합니다.
        - (예: problem/Pwn_Basic_BOF/add_exploit_code → problem/Pwn_Basic_BOF)
    - 문제 통합 → dev: 하나의 문제가 완성되면 (관련 기능들이 모두 병합되면), problem/{문제이름} 브랜치를 dev 브랜치로 PR합니다.

5. 병합 (Merge)
    - Hackerlogin/CTF_PROBLEM:dev으로 PR을 보냅니다.
      - 관리자는 브랜치 형식에 맞도록 브랜치 생성 후 PR을 수정하여 올바른 브랜치로 통합될 수 있도록 합니다.
      - 이 후 코드리뷰 및 문제 검증을 과정을 거친 이후 dev 브랜치로 머지합니다.
    - main 브랜치로의 병합은 관리자(운영진)가 수행합니다.

## 2. Commit 메시지 규칙

커밋 히스토리의 가독성을 높이기 위해 Conventional Commits 양식을 따릅니다.

### 기본 형식
```
<type>(<scope>): <subject>
<body>
```

- `<type>`: 커밋 유형
    - feat: 새로운 문제 추가, 문제에 새로운 기능 추가 (e.g., Dockerfile)
    - fix: 문제 버그 수정, 풀이 코드 오류, 오타 수정
    - docs: README.md 수정, 문제 설명(writeup) 추가
    - refactor: 동작은 같지만 코드 개선 (e.g., 변수명 변경, 구조 개선)
    - style: 코드 포맷팅, 세미콜론 추가 등 (기능 변경 없음)
    - chore: .gitignore 수정, 빌드 스크립트 변경 등 프로젝트 관리 작업

- `<scope>`: 작업 범위
    - 문제 이름을 괄호 안에 적습니다. (e.g., Web_Login_Easy, Pwn_Basic_BOF)
    - 여러 문제에 공통으로 적용되면 common을 사용합니다.

- `<subject>`: 제목
    - 50자 이내로, 무엇을 했는지 명확하게 요약합니다.
    - "~함", "~수정"과 같이 명령조로 작성합니다. (e.g., Add admin page validation)
- `<body>`: 상세 수정사항(선택)
    - 자신의 수정사항을 상세히 기술하고 싶을때 사용합니다.
    - 일반적으로는 사용하지 않는 것을 추천드립니다.

### 예시
- feat(Pwn_Baby_BOF): Add initial challenge files
- fix(Web_Login_Easy): Sanitize user input to prevent XSS vulnerability
- docs(common): Update branching strategy and commit rules
- chore(Web_Login_Easy): Add .flag file to .gitignore

## 3. 로컬환경 설정(Sparse Checkout 권장)
본 저장소는 Monorepo(단일 저장소)로 운영되므로, 모든 문제 파일이 루트에 존재합니다. 새 문제 작업 시, 다른 문제 디렉터리로 인한 불편함을 줄이기 위해 Sparse Checkout 사용을 강력히 권장합니다.

1. 저장소 Clone (파일 없이)
    ```
    git clone --no-checkout git@github.com:{ID}/CTF_PROBLEM.git
    cd CTF_PROBLEM
    ```
2. Sparse Checkout 활성화 및 경로 설정
    ```
    git sparse-checkout init
    git sparse-checkout set 'README.md' 'CONTRIBUTING.md' 'problem/{문제이름}'
    ```
3. 파일 다운로드 및 브랜치 생성(dev 브랜치 기준 파생)
    ```
    git pull origin dev
    git checkout -c problem/{문제이름}
    ```
