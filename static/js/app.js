// DOM 요소 캐싱
document.addEventListener("DOMContentLoaded", () => {
    const resumeForm = document.getElementById("resumeForm");
    const generateBtn = document.getElementById("generateBtn");
    const loadingIndicator = document.getElementById("loadingIndicator");
    const emptyState = document.getElementById("emptyState");
    const resultContainer = document.getElementById("resultContainer");
    const actionButtons = document.getElementById("actionButtons");
    const errorMessage = document.getElementById("errorMessage");
    const copyBtn = document.getElementById("copyBtn");
    const downloadBtn = document.getElementById("downloadBtn");

    // 원본 마크다운 텍스트를 저장할 변수 (복사 및 다운로드에 활용)
    let currentRawMarkdown = "";
    let currentApplicantName = "resume";

    // 폼 제출(Submit) 이벤트 처리
    resumeForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        // 1. 사용자 입력값 가져오기
        const name = document.getElementById("name").value.trim();
        const jobTitle = document.getElementById("jobTitle").value.trim();
        const experience = document.getElementById("experience").value.trim();
        const projects = document.getElementById("projects").value.trim();
        const tone = document.getElementById("tone").value;
        const promptType = document.querySelector('input[name="prompt_type"]:checked').value;

        // 2. 프론트엔드 유효성 검사 (빈 값 체크)
        if (!name || !jobTitle || !experience || !projects) {
            showError("모든 필수 항목(*)을 빠짐없이 입력해 주세요.");
            return;
        }

        currentApplicantName = name;

        // 3. UI 상태를 '로딩 중'으로 전환
        setLoadingState(true);
        hideError();

        // 4. 백엔드 Flask 서버의 /generate 엔드포인트로 비동기 요청 전송
        try {
            const response = await fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    job_title: jobTitle,
                    experience: experience,
                    projects: projects,
                    tone: tone,
                    prompt_type: promptType
                })
            });

            const data = await response.json();

            // 백엔드 오류 응답 처리
            if (!response.ok) {
                const errorText = data.error || "알 수 없는 오류가 발생했습니다. 다시 시도해 주세요.";
                showError(errorText);
                return;
            }

            // 5. AI 생성 결과 렌더링
            if (data.success && data.result) {
                currentRawMarkdown = data.result;

                // 마크다운 라이브러리(marked)를 사용하여 깔끔한 HTML로 변환 출력
                if (window.marked && typeof window.marked.parse === "function") {
                    resultContainer.innerHTML = marked.parse(currentRawMarkdown);
                } else {
                    // 라이브러리 로드 실패 시 일반 텍스트 표시 폴백
                    resultContainer.textContent = currentRawMarkdown;
                }

                // 결과 영역 활성화
                emptyState.style.display = "none";
                resultContainer.style.display = "block";
                actionButtons.style.display = "flex";

                // 결과창으로 부드럽게 스크롤 이동
                resultContainer.scrollIntoView({ behavior: "smooth", block: "nearest" });
            } else {
                showError("생성된 결과가 비어 있습니다. 잠시 후 다시 시도해 주세요.");
            }

        } catch (err) {
            console.error("API 요청 오류:", err);
            showError("서버와의 통신에 실패했습니다. Flask 서버가 실행 중인지 확인해 주세요.");
        } finally {
            // 로딩 종료 및 버튼 복구
            setLoadingState(false);
        }
    });

    // 6. 결과 복사 기능
    copyBtn.addEventListener("click", async () => {
        if (!currentRawMarkdown) return;

        try {
            await navigator.clipboard.writeText(currentRawMarkdown);
            const originalText = copyBtn.textContent;
            copyBtn.textContent = "복사 완료! 🐥";
            copyBtn.style.backgroundColor = "#c6f6d5";
            copyBtn.style.color = "#22543d";

            setTimeout(() => {
                copyBtn.textContent = originalText;
                copyBtn.style.backgroundColor = "";
                copyBtn.style.color = "";
            }, 2000);
        } catch (err) {
            console.error("클립보드 복사 실패:", err);
            alert("클립보드 복사에 실패했습니다. 브라우저 보안 설정을 확인해 주세요.");
        }
    });

    // 7. Markdown (.md) 파일 다운로드 기능
    downloadBtn.addEventListener("click", () => {
        if (!currentRawMarkdown) return;

        const blob = new Blob([currentRawMarkdown], { type: "text/markdown;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        const safeName = currentApplicantName.replace(/[^a-zA-Z0-9가-힣_-]/g, "_");
        
        a.href = url;
        a.download = `${safeName}_이력서_포트폴리오.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    // 도우미 함수: 로딩 상태 UI 제어
    function setLoadingState(isLoading) {
        if (isLoading) {
            loadingIndicator.style.display = "block";
            emptyState.style.display = "none";
            resultContainer.style.display = "none";
            actionButtons.style.display = "none";
            generateBtn.disabled = true;
            generateBtn.textContent = "트위티가 작성 중입니다... ⭐";
        } else {
            loadingIndicator.style.display = "none";
            generateBtn.disabled = false;
            generateBtn.textContent = "AI 이력서 & 포트폴리오 생성하기";
        }
    }

    // 도우미 함수: 에러 메시지 표시
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = "block";
        emptyState.style.display = "block";
        resultContainer.style.display = "none";
        actionButtons.style.display = "none";
    }

    // 도우미 함수: 에러 메시지 숨기기
    function hideError() {
        errorMessage.style.display = "none";
        errorMessage.textContent = "";
    }
});
