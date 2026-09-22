# 🐥 AI Resume & Portfolio Builder

> **Google Gemini AI와 함께하는 나만의 맞춤형 이력서 & 포트폴리오 원스톱 생성기**  
> 사용자의 경험과 프로젝트를 기반으로 채용 합격률을 높이는 최적의 문서를 작성하고, 귀여운 **트위티(Tweety) 동화책 감성 테마**로 친근하고 직관적인 사용자 경험을 제공합니다.

---

## 🌟 주요 기능 (Key Features)

1. **AI 맞춤형 초안 자동 생성**
   - 지원자 이름, 지원 직무, 주요 경력, 수행 프로젝트, 희망 어조(Tone)를 기반으로 **이력서(Resume)**와 **포트폴리오(Portfolio)** 초안을 Markdown 형식으로 원스톱 생성합니다.

2. **듀얼 프롬프트 모드 (Prompt A / B)**
   - **Prompt A (일반 모드)**: 정돈되고 친근하며 표준적인 작성 코치 스타일 (가독성 중심 불릿포인트)
   - **Prompt B (전문가 모드)**: **STAR 기법**(Situation, Task, Action, Result)과 정량적 성과 지표(숫자, 기여도, 비즈니스 임팩트)를 극대화한 채용 전문가 스타일

3. **실시간 마크다운 렌더링 & 편의 기능**
   - **실시간 미리보기**: `Marked.js`를 연동하여 AI가 생성한 마크다운을 브라우저에서 즉시 예쁜 서식으로 렌더링
   - **원클릭 복사**: 생성된 마크다운 전문을 클립보드로 즉시 복사하여 노션(Notion), 워드(Word), 구글 문서에 바로 활용
   - **.md 파일 다운로드**: `[이름]_이력서_포트폴리오.md` 파일로 로컬 PC에 원클릭 저장

4. **철저한 유효성 검사 & 로깅**
   - 프론트엔드 필수 입력값 체크 및 사용자 피드백
   - Flask 백엔드 유효성 검증 및 요청/오류 내역 실시간 콘솔 로깅

5. **동화책 일러스트 감성 (Disney Fairytale Theme) UI/UX**
   - 트위티 캐릭터(화가 트위티, 학사모 트위티, 정장 트위티) 일러스트 배치
   - 포근하고 따뜻한 버터크림 톤의 스케치북 입력 폼 & 스카이블루 결과 카드
   - 우측 하단 플로팅 구름 말풍선 위젯 탑재

---

## 🛠 기술 스택 (Tech Stack)

| 구분 | 기술 / 라이브러리 | 용도 및 설명 |
|---|---|---|
| **Backend** | Python 3, Flask | 경량 웹 서버 프레임워크 및 라우팅 |
| **AI Model** | Google Gemini API | `google-genai` SDK (`gemini-3.5-flash-lite`) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | 반응형 2단 레이아웃 및 비동기 Fetch 통신 |
| **Markdown** | Marked.js | AI 마크다운 텍스트 실시간 서식 렌더링 |
| **Fonts** | Google Fonts | `Bagel Fat One`, `Jua`, `Nunito` 등 |
| **Security** | python-dotenv | 환경변수를 통한 Gemini API Key 보안 분리 관리 |

---

## 📂 프로젝트 구조 (Project Structure)

```text
resume-builder/
├── app.py                  # Flask 백엔드 서버 (라우팅, 유효성 검사, Gemini API 연동)
├── requirements.txt        # 파이썬 의존성 패키지 목록
├── .env.example            # 환경변수 설정 가이드 견본 파일
├── .env                    # 실제 비밀 API Key (Git 제외)
├── .gitignore              # Git 추적 제외 목록 (.env, venv/ 등)
├── README.md               # 프로젝트 안내 문서
├── templates/
│   └── index.html          # 메인 프론트엔드 웹 화면
└── static/
    ├── css/
    │   └── style.css       # 동화책 감성 및 트위티 테마 스타일시트
    ├── js/
    │   └── app.js          # 비동기 통신, 복사, 다운로드 동작 스크립트
    └── img/
        └── reference/      # 트위티 캐릭터 일러스트 이미지 세트
```

---

## 🚀 빠른 시작 (Getting Started)

### 1. 가상환경 생성 및 활성화 (Windows PowerShell)

```powershell
# 프로젝트 디렉토리로 이동
cd C:\AI-study\resume-builder

# 가상환경 생성 (최초 1회)
python -m venv venv

# 스크립트 실행 권한 부여 후 가상환경 활성화
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

> 가상환경이 켜지면 터미널 프롬프트 앞에 **`(venv)`** 표시가 나타납니다.

### 2. 패키지 설치

```powershell
pip install -r requirements.txt
```

### 3. Gemini API Key 환경변수 설정

1. [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료 API Key 발급
2. `.env.example` 파일을 복사하여 `.env` 파일 생성
   ```powershell
   Copy-Item .env.example .env
   ```
3. `.env` 파일을 열고 발급받은 실제 API 키 입력:
   ```env
   GEMINI_API_KEY=AIzaSy...실제키입력
   ```

### 4. 웹 서버 실행

```powershell
python app.py
```

브라우저를 열고 아래 주소로 접속합니다:
👉 **`http://127.0.0.1:5000`**

---

## 💡 사용 방법 (How to Use)

1. **지원자 정보 입력**: 이름과 지원 직무를 입력합니다.
2. **스타일 모드 선택**:
   - **일반 모드 (Prompt A)**: 단정하고 친근한 표준 스타일
   - **전문가 모드 (Prompt B)**: STAR 기법 및 수치/성과 중심 스타일
3. **경력 및 프로젝트 작성**: 주요 담당 업무, 성과, 진행 프로젝트의 세부 내용을 작성합니다.
4. **이력서 & 포트폴리오 생성하기 클릭**: Gemini AI가 분석하여 우측 화면에 완성된 초안을 실시간 렌더링합니다.
5. **복사 및 다운로드**:
   - **전체 내용 복사**: 노션, 워드 등에 바로 붙여넣기
   - **.md 파일 다운로드**: 내 컴퓨터에 마크다운 파일로 저장

---

## 🔒 보안 및 주의사항 (Security)

- 비밀 API Key가 저장된 `.env` 파일은 절대 GitHub 등 원격 저장소에 커밋/푸시하지 마세요.
- [.gitignore](file:///C:/AI-study/resume-builder/.gitignore) 파일에 `.env`와 가상환경 폴더(`venv/`)가 등록되어 있어 안전하게 관리됩니다.
