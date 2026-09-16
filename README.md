# 🐥 AI Resume & Portfolio Builder

> **Google Gemini AI와 함께하는 나만의 맞춤형 이력서 & 포트폴리오 원스톱 생성기**  
> 사용자의 경험과 프로젝트를 기반으로 채용 합격률을 높이는 최적의 문서를 작성하고, 귀여운 **트위티(Tweety) 고대비 디자인**으로 뛰어난 웹 접근성을 제공합니다.

---

## 🌟 주요 기능 (Key Features)

1. **AI 맞춤형 초안 자동 생성**
   - 이름, 지원 직무, 주요 경력, 수행 프로젝트, 원하는 문체(Tone)를 분석하여 완성도 높은 이력서와 포트폴리오를 동시 제작합니다.
2. **듀얼 프롬프트 엔지니어링 (Prompt A / B)**
   - **Prompt A (일반 모드)**: 누구나 읽기 편하고 표준적인 정돈된 스타일
   - **Prompt B (전문가 모드)**: **STAR 기법**(Situation, Task, Action, Result)과 정량적 성과 지표(숫자, 기여도)를 극대화한 채용 전문가 스타일
3. **사용자 편의 기능**
   - **원클릭 복사**: 생성된 마크다운 전문을 클립보드로 즉시 복사 (노션, 워드 붙여넣기 최적화)
   - **파일 다운로드**: `[이름]_이력서_포트폴리오.md` 파일로 내 컴퓨터에 즉시 저장
4. **철저한 유효성 검사 & 로깅**
   - 프론트엔드와 백엔드 양방향 입력 검증
   - Flask 백엔드 콘솔에 요청 접수, AI 호출 과정, 에러 내역 실시간 로깅
5. **동화책 일러스트 감성 (Disney Fairytale Theme) UI/UX**
   - **양피지 두루마리 배너 & 3D 볼륨 타이틀**: 고풍스러운 양피지 두루마리 질감과 맑고 화사한 3D 입체 옐로우 타이틀
   - **오리지널 트위티(Tweety) 일러스트**: 화가, 학사모, 합격증, 양복 트위티의 투명 배경(누끼) 캐릭터 삽화 배치
   - **색연필 손그림 입력 폼**: 스케치북에 색연필로 그린 듯한 몽글몽글하고 섬세한 1.5px 테두리와 부드러운 크림톤 입력 상자
   - **구름 말풍선 위젯**: "내가 봐떠! 합격을 봐떠!" 양복 트위티 플로팅 컴포넌트 탑재

---

## 🛠 기술 스택 (Tech Stack)

| 구분 | 기술 / 라이브러리 | 설명 |
|---|---|---|
| **Backend** | Python 3, Flask | 경량 웹 서버 프레임워크 및 라우팅 |
| **AI Model** | Google Gemini API (`gemini-3.5-flash-lite`) | Google 최신 공식 GenAI SDK 연동 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | 비동기 Fetch 통신, 반응형 2단 레이아웃 |
| **Markdown** | Marked.js | AI 마크다운 텍스트를 실시간 웹 서식으로 렌더링 |
| **Font** | Google Fonts (`Bagel Fat One`, `Jua`, `Nunito`) | 3D 볼륨 타이틀 및 둥근 가독성 폰트 |
| **Security** | python-dotenv | 개인 API Key 분리 보관 및 Git 추적 원천 차단 |

---

## 📂 프로젝트 구조 (Project Structure)

```text
resume-builder/
├── app.py                  # 백엔드 서버 (라우트, 검증, Gemini API 연동)
├── requirements.txt        # 파이썬 의존성 패키지 목록
├── .env.example            # 환경변수 설정 가이드 견본 파일
├── .env                    # 실제 비밀 API Key (Git 제외)
├── .gitignore              # Git 추적 제외 목록 (.env, venv/ 등)
├── README.md               # 프로젝트 안내 문서
├── templates/
│   └── index.html          # 프론트엔드 메인 웹 화면
└── static/
    ├── css/
    │   └── style.css       # 동화책 일러스트 및 색연필 스타일시트
    ├── js/
    │   └── app.js          # 비동기 통신, 복사, 다운로드 동작 스크립트
    └── img/
        └── reference/      # 투명 배경 트위티 일러스트 캐릭터 세트
            ├── tweety_artist.png
            ├── tweety_scholar.png
            ├── tweety_pass.png
            └── tweety_suit_bubble.png
```

---

## 🚀 빠른 시작 (Getting Started)

### 1. 가상환경 생성 및 활성화 (Windows PowerShell)

```powershell
# 가상환경 생성
py -m venv venv

# 가상환경 활성화
.\venv\Scripts\Activate.ps1
```

### 2. 패키지 설치

```powershell
py -m pip install -r requirements.txt
```

### 3. Gemini API Key 환경변수 설정

1. [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료 API Key 발급
2. 견본 파일을 복사하여 `.env` 생성
   ```powershell
   Copy-Item .env.example .env
   ```
3. `.env` 파일을 열고 발급받은 실제 키 입력:
   ```env
   GEMINI_API_KEY=AIzaSy...실제키입력
   ```

### 4. 웹 서버 실행

```powershell
py app.py
```

브라우저를 열고 다음 주소로 접속합니다:
👉 **`http://127.0.0.1:5000`**

---

## 🔒 보안 원칙 (Security)

- 비밀 API Key가 담긴 `.env` 파일은 절대 GitHub 등 원격 저장소에 업로드하지 않습니다.
- [.gitignore](file:///C:/AI-study/resume-builder/.gitignore) 파일에 `.env`와 수천 개의 가상환경 파일(`venv/`)이 기본 등록되어 있어 안전하게 관리됩니다.

---

## 💛 라이선스 및 크레딧
- Character: Tweety Bird (Warner Bros. / Looney Tunes)
- Fonts: Google Fonts (Jua by Woowa Brothers, Nunito by Vernon Adams)
- Powered by Google DeepMind & Google Gemini
