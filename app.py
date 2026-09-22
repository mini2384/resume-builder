import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# .env 파일에서 환경변수 로드
load_dotenv()

# 프로젝트 루트 디렉토리 (Vercel Serverless 및 로컬 실행 공통 경로 지원)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask 애플리케이션 초기화
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# 백엔드 로그 설정 (요청, 응답, 오류 기록)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)
logger = app.logger


def get_gemini_client():
    """Gemini API 클라이언트를 초기화하고 반환합니다."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "your_gemini_api_key_here":
        raise ValueError(
            ".env 파일에 올바른 GEMINI_API_KEY가 설정되지 않았습니다. "
            "Google AI Studio에서 발급받은 실제 API Key를 .env 파일에 입력해 주세요."
        )
    return genai.Client(api_key=api_key.strip())


def build_prompt(name, job_title, experience, projects, tone, prompt_type):
    """사용자 입력과 프롬프트 유형(A/B)에 따라 Gemini 프롬프트를 구성합니다."""
    if prompt_type == "B":
        # Prompt B: 전문가 모드 (성과 지향, STAR 기법, 임팩트 중심)
        prompt = f"""
당신은 최고 수준의 테크 및 비즈니스 채용 전문 커리어 컨설턴트입니다.
제공된 정보를 바탕으로 인사담당자의 시선을 사로잡을 수 있는 고품질의 [이력서(Resume)]와 [포트폴리오(Portfolio)] 초안을 Markdown 형식으로 작성해 주세요.

[작성 지침 - 전문가 모드]
1. 톤앤매너: {tone} 어조를 유지하면서도 전문적이고 자신감 있는 비즈니스 어조를 사용하세요.
2. 성과 중심 서술: 단순 업무 나열이 아닌 STAR(Situation, Task, Action, Result) 구조와 정량적 성과(수치, 지표, 기여도)를 부각하세요.
3. 역량 키워드: 지원 직무({job_title})에 맞는 산업 핵심 키워드와 기술 스택을 자연스럽게 포함하세요.
4. 구성:
   - ## 1. Professional Resume (이력서)
     - 프로필 요약 (Executive Summary)
     - 핵심 역량 (Core Competencies)
     - 주요 경력 사항 (Professional Experience - 성과 지향 불릿포인트)
     - 학력 및 기타 (Education & Certifications)
   - ## 2. Project Portfolio (포트폴리오)
     - 프로젝트 개요 및 문제 정의 (Problem Statement)
     - 본인의 역할 및 해결 접근 방식 (Approach & Solutions)
     - 핵심 결과 및 비즈니스 임팩트 (Key Results & Impact)

[지원자 정보]
- 이름: {name}
- 지원 직무: {job_title}
- 경력 사항:
{experience}
- 수행 프로젝트:
{projects}
"""
    else:
        # Prompt A: 일반 모드 (명확하고 표준적이며 친근한 스타일)
        prompt = f"""
당신은 친절하고 꼼꼼한 이력서 작성 코치입니다.
제공된 정보를 바탕으로 읽기 쉽고 표준적인 [이력서(Resume)]와 [포트폴리오(Portfolio)] 초안을 Markdown 형식으로 작성해 주세요.

[작성 지침 - 일반 모드]
1. 톤앤매너: {tone} 어조로 정중하고 명확하게 작성하세요.
2. 가독성: 글머리 기호(불릿)를 활용하여 한눈에 내용을 파악하기 쉽게 정리하세요.
3. 구성:
   - ## 1. 이력서 (Resume)
     - 자기소개 요약
     - 지원 직무 관련 핵심 보유 역량
     - 경력 사항 (담당 업무 및 경험 상세)
   - ## 2. 포트폴리오 (Portfolio)
     - 프로젝트 명칭 및 소개
     - 주요 담당 역할 및 사용 기술
     - 프로젝트를 통해 배운 점 및 성과

[지원자 정보]
- 이름: {name}
- 지원 직무: {job_title}
- 경력 사항:
{experience}
- 수행 프로젝트:
{projects}
"""
    return prompt.strip()


@app.route("/")
def index():
    """메인 화면(HTML)을 렌더링합니다."""
    return render_template("index.html")


@app.route("/manifest.json")
def manifest():
    """PWA 웹 앱 매니페스트를 서빙합니다."""
    return app.send_static_file("manifest.json")


@app.route("/sw.js")
def service_worker():
    """PWA 서비스 워커를 루트 스코프 권한과 함께 서빙합니다."""
    response = app.send_static_file("sw.js")
    response.headers["Content-Type"] = "application/javascript"
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.route("/generate", methods=["POST"])
def generate():
    """사용자 입력을 검증하고 Gemini API를 호출하여 이력서 및 포트폴리오를 생성합니다."""
    data = request.get_json()

    # 1. 요청 데이터 존재 확인
    if not data:
        logger.warning("[요청 거부] JSON 요청 데이터가 비어 있습니다.")
        return jsonify({"error": "전송된 데이터가 없습니다. 양식을 올바르게 입력해 주세요."}), 400

    # 2. 필수 필드 추출 및 공백 제거
    name = data.get("name", "").strip()
    job_title = data.get("job_title", "").strip()
    experience = data.get("experience", "").strip()
    projects = data.get("projects", "").strip()
    tone = data.get("tone", "전문적이고 신뢰감 있는").strip()
    prompt_type = data.get("prompt_type", "A").strip()

    logger.info(
        f"[생성 요청 접수] 지원자: {name} | 직무: {job_title} | 모드: Prompt {prompt_type} | Tone: {tone}"
    )

    # 3. 백엔드 필수 입력값 검증
    missing_fields = []
    if not name:
        missing_fields.append("이름")
    if not job_title:
        missing_fields.append("지원 직무")
    if not experience:
        missing_fields.append("경력 사항")
    if not projects:
        missing_fields.append("프로젝트")

    if missing_fields:
        error_msg = f"다음 필수 항목을 입력해 주세요: {', '.join(missing_fields)}"
        logger.warning(f"[검증 실패] {error_msg}")
        return jsonify({"error": error_msg}), 400

    # 4. Gemini API 호출
    try:
        client = get_gemini_client()
        prompt = build_prompt(name, job_title, experience, projects, tone, prompt_type)

        logger.info("[Gemini API 호출 중...] 프롬프트를 AI 모델로 전송합니다.")

        # 최신 초경량 Gemini 모델 우선 호출 (fallback 처리 포함)
        model_name = "gemini-3.5-flash-lite"
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
        except Exception as model_err:
            logger.warning(f"[{model_name} 호출 실패, gemini-3.6-flash로 재시도]: {model_err}")
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

        result_text = response.text
        if not result_text:
            raise ValueError("Gemini API로부터 빈 응답을 받았습니다.")

        logger.info(f"[생성 성공] 지원자: {name} 님의 이력서 및 포트폴리오 생성 완료 (글자 수: {len(result_text)})")
        return jsonify({
            "success": True,
            "result": result_text
        })

    except ValueError as val_err:
        logger.error(f"[설정 오류] {val_err}")
        return jsonify({"error": str(val_err)}), 400

    except errors.APIError as api_err:
        logger.error(f"[Gemini API 오류] {api_err}")
        return jsonify({"error": f"Google Gemini API 연동 중 오류가 발생했습니다: {api_err.message}"}), 502

    except Exception as e:
        logger.exception(f"[서버 내부 오류] 예상치 못한 에러가 발생했습니다: {e}")
        return jsonify({"error": f"AI 문서 생성 중 서버 오류가 발생했습니다: {str(e)}"}), 500


if __name__ == "__main__":
    # 로컬 개발 서버 실행 (기본 포트 5000)
    logger.info("Starting Flask Resume & Portfolio Builder server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
