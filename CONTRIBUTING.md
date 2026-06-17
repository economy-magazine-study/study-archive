# 경제잡지 스터디 아카이브 작성 방법

## 새 발표 문서 추가

1. `templates/weekly-share.md`를 복사합니다.
2. 기수와 주차에 맞는 폴더에 `index.md`로 저장합니다.
   - 예: `src/content/docs/gen-4/week-02-2026-06-11/kim-yowook/index.md`
3. 이미지는 같은 폴더의 `images/`에 저장합니다.
4. `pnpm dev`로 화면을 확인합니다.
5. 변경사항을 커밋하고 푸시합니다.

## 로컬 실행

```bash
pnpm install
pnpm dev
```

## 커밋 전 문서 메타데이터 확인

새 문서를 추가할 때 frontmatter의 `sidebar`, 주차별 `index.md` 발표 목록, `astro.config.mjs` 사이드바 등록이 빠지지 않도록 아래 검사를 실행합니다.

```bash
pnpm docs:check
```

커밋 전에 자동으로 확인하려면 한 번만 훅 경로를 설정합니다.

```bash
git config core.hooksPath .githooks
```

검사 실패 메시지에는 수정해야 할 파일 경로와 추가할 `sidebar`/링크/slug가 함께 표시됩니다.

## 빌드 확인

```bash
pnpm build
pnpm preview
```

## GitHub Pages

`main` 브랜치에 푸시하면 `.github/workflows/deploy.yml` 워크플로가 정적 사이트를 빌드해 GitHub Pages에 배포합니다. 저장소 Settings > Pages에서 Source를 `GitHub Actions`로 설정해야 합니다.
