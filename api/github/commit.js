const { App } = require("octokit");

export default async function handler(req, res) {
  // CORS 설정 (게임 클라이언트에서 접근할 수 있도록 허용)
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'OPTIONS,POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // 사전 요청(Preflight) 처리
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // POST 요청만 허용
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'POST 요청만 지원합니다.' });
  }

  try {
    // 게임 클라이언트로부터 받은 데이터
    const { path, content, commitMessage, owner } = req.body;

    if (!path || !content) {
      return res.status(400).json({ error: 'path와 content 데이터가 필요합니다.' });
    }

    // 1. GitHub App 인증 (Vercel 환경변수 사용)
    const app = new App({
      appId: process.env.GITHUB_APP_ID,
      privateKey: process.env.GITHUB_PRIVATE_KEY.replace(/\\n/g, '\n'),
    });

    // 2. Octokit 클라이언트 생성
    const octokit = await app.getInstallationOctokit(process.env.GITHUB_INSTALLATION_ID);

    // ★ 본인의 깃허브 아이디로 반드시 변경해 주세요!
    const repoOwner = "snrnsp";
    const repoName = "Project-F";

    // 3. 기존 파일 존재 여부 확인 (업데이트 시 SHA 값이 필요함)
    let fileSha;
    try {
      const { data } = await octokit.rest.repos.getContent({
        owner: repoOwner,
        repo: repoName,
        path: path,
      });
      fileSha = data.sha;
    } catch (error) {
      // 파일이 없을 경우 새로 생성하는 것이므로 무시하고 진행
    }

    // 4. 깃허브에 파일 커밋 및 푸시
    const response = await octokit.rest.repos.createOrUpdateFileContents({
      owner: repoOwner,
      repo: repoName,
      path: path,
      message: commitMessage || '게임에서 데이터 자동 저장',
      content: Buffer.from(content).toString('base64'), // 깃허브 API는 Base64 인코딩 필수
      sha: fileSha,
    });

    // 성공 응답
    return res.status(200).json({ 
      success: true, 
      message: '커밋이 성공적으로 완료되었습니다!',
      url: response.data.commit.html_url 
    });

  } catch (error) {
    console.error("GitHub API 에러:", error);
    return res.status(500).json({ error: error.message });
  }
}