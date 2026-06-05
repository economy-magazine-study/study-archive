---
title: 작성 가이드
description: 경제잡지 스터디 아카이브 문서 작성 방법입니다.
sidebar:
  label: 작성 가이드
  order: 1
---

## AI 작성 프롬프트

아래 프롬프트를 AI 에이전트에 붙여넣고, 대괄호 안의 값만 바꿔서 사용합니다. 파일 생성까지 맡길 수 있도록 저장 경로와 업데이트 규칙을 포함해두었습니다.

```text
너는 경제잡지 스터디 아카이브 저장소를 수정하는 도우미야.
아래 입력 정보를 바탕으로 발표자 공유 문서를 만들고, 정해진 위치에 파일로 저장해줘.

목표:
- 스터디에서 5-10분 정도 공유할 수 있는 짧고 읽기 쉬운 문서를 만든다.
- 단순 요약보다 "무엇을 배웠는지", "무엇이 어려웠는지", "같이 이야기할 점"이 드러나게 쓴다.
- 나중에 태그 검색, 키워드 검색, 관계도 그래프를 만들 수 있도록 frontmatter 메타데이터를 성실히 채운다.
- 과장하거나 원문에 없는 사실을 만들지 않는다. 확실하지 않은 내용은 "확인 필요"라고 표시한다.
- 저장소의 기존 구조와 스타일을 유지한다.

입력 정보:
- 발표자: [이름]
- 발표자 영문 슬러그: [예: kim-yowook, 모르면 AI가 한글 이름을 읽기 쉬운 kebab-case 영문으로 제안]
- 기수: [예: 4]
- 주차: [예: 1]
- 스터디 날짜: [예: 2026-06-11]
- 발표 순서: [예: 1]
- 기사 제목: [기사 제목]
- 매체/호수/섹션: [예: The Economist / Finance & economics]
- 기사 발행일: [예: 2026-06-01]
- 기사 URL: [URL, 없으면 비워두기]
- 내가 읽고 이해한 내용 또는 원문 메모:
  [여기에 기사 요약, 발췌 메모, 내 생각, 어려웠던 부분을 붙여넣기]
- 꼭 포함하고 싶은 이미지 파일명:
  [예: chart.png, 없으면 비워두기]

파일/폴더 규칙:
- 발표 문서 경로는 아래 규칙을 따른다.
  `src/content/docs/gen-{기수}/week-{2자리 주차}-{YYYY-MM-DD}/{발표자 영문 슬러그}/index.md`
- 예시:
  `src/content/docs/gen-4/week-01-2026-06-11/kim-yowook/index.md`
- 이미지가 있으면 아래 폴더에 둔다.
  `src/content/docs/gen-{기수}/week-{2자리 주차}-{YYYY-MM-DD}/{발표자 영문 슬러그}/images/`
- 본문에서 이미지는 `![이미지 설명](./images/파일명)` 형식으로 참조한다.
- 새 발표자를 추가하면 주차 개요 문서도 업데이트한다.
  `src/content/docs/gen-{기수}/week-{2자리 주차}-{YYYY-MM-DD}/index.md`
- 사이드바가 수동 설정되어 있으면 `astro.config.mjs`의 해당 주차 항목에도 발표자 링크를 추가한다.

작업 방식:
- 위 경로의 폴더가 없으면 생성한다.
- `index.md`가 이미 있으면 덮어쓰기 전에 기존 내용을 확인하고, 기존 발표 내용이 있으면 보존할지 물어본다.
- 주차 개요 문서의 발표 순서 표에 발표자를 추가하거나 기존 행을 업데이트한다.
- `astro.config.mjs`에 같은 발표자 항목이 없을 때만 추가한다.
- 작업 후 가능하면 `pnpm build`를 실행해서 frontmatter와 링크가 깨지지 않는지 확인한다.

Markdown 문서 형식:
- 맨 위에 YAML frontmatter를 포함한다.
- frontmatter에는 아래 필드를 포함한다.
  - title: "이름 - 발표 주제"
  - description
  - author
  - date
  - generation
  - week
  - tags: 넓은 주제 3-6개
  - keywords: 핵심 개념 5-10개
  - source.title
  - source.publication
  - source.publishedDate
  - source.url
  - source.section
  - entities.countries
  - entities.regions
  - entities.organizations
  - entities.companies
  - entities.people
  - entities.indicators
  - related.topics
  - related.pages: 모르면 []
  - sidebar.label
  - sidebar.order
- 본문에는 아래 섹션을 이 순서대로 포함한다.
  - ## 한 줄 요약
  - ## 읽은 기사와 배경
  - ## 핵심 내용
  - ## 배운 점
  - ## 어려웠던 점
  - ## 같이 알면 좋은 것
  - ## 토론거리

작성 규칙:
- 한 줄 요약은 1문장으로 쓴다.
- 핵심 내용은 3개 안팎의 번호 목록으로 쓴다.
- "같이 알면 좋은 것"은 가능하면 Markdown 표로 쓴다.
- 토론거리는 질문 1-3개로 쓴다.
- 이미지 파일명이 있으면 본문 적절한 위치에 `![이미지 설명](./images/파일명)` 형식으로 넣는다.
- tags는 넓은 분류, keywords는 더 구체적인 개념으로 구분한다.
- entities에는 국가, 지역, 기관, 기업, 인물, 경제지표를 분리해서 적는다.
- URL이 없으면 `url:`을 비워둔다.
- 모르는 값은 추측하지 말고 빈 배열 `[]` 또는 빈 값으로 둔다.

마지막 응답:
- 생성/수정한 파일 경로를 짧게 알려준다.
- 빌드를 실행했다면 성공/실패를 알려준다.
- 빌드를 실행하지 못했다면 이유를 알려준다.
```

## 파일 위치

발표 문서는 아래 규칙으로 저장합니다.

```text
src/content/docs/gen-4/week-01-2026-06-11/kim-yowook/index.md
```

이미지는 발표자 폴더 안의 `images/`에 넣습니다.

```text
src/content/docs/gen-4/week-01-2026-06-11/kim-yowook/images/chart.png
```

## frontmatter

문서 맨 위에는 제목, 날짜, 발표자, 태그를 적습니다.

```yaml
---
title: 김요욱 - 발표 주제
description: 2026-06-11 경제잡지 스터디 공유 문서입니다.
author: 김요욱
date: 2026-06-11
generation: 4
week: 1
tags: [금리, 물가]
keywords: [기준금리, 인플레이션, 고용지표]
source:
  title: 기사 제목
  publication: The Economist
  publishedDate: 2026-06-01
  url: https://example.com/article
  section: Finance & economics
entities:
  countries: [미국]
  regions: []
  organizations: [연방준비제도]
  companies: []
  people: []
  indicators: [기준금리, CPI]
related:
  topics: [통화정책, 채권시장]
  pages: []
sidebar:
  label: 김요욱
  order: 1
---
```

## 메타데이터 수집

나중에 태그 검색, 주제별 모아보기, 문서 관계도 같은 기능을 만들 수 있도록 발표 문서를 만들 때 아래 정보를 같이 수집합니다.

| 필드 | 용도 | 작성 예시 |
| --- | --- | --- |
| `tags` | 넓은 분류입니다. 필터 UI에 쓰기 좋습니다. | `[금리, 중앙은행]` |
| `keywords` | 기사 안의 핵심 개념입니다. 검색 가중치나 키워드 클라우드에 쓰기 좋습니다. | `[기준금리, 수익률곡선]` |
| `source` | 원문 기사 정보입니다. 출처 추적과 재방문에 씁니다. | `publication`, `url` |
| `entities` | 관계도 노드 후보입니다. 국가, 기관, 기업, 인물, 지표를 나눠 적습니다. | `organizations: [연방준비제도]` |
| `related` | 발표자가 직접 연결해둔 주제나 문서입니다. | `topics: [통화정책]` |

처음부터 완벽하게 채울 필요는 없습니다. 다만 `tags`, `keywords`, `entities.indicators` 정도만 꾸준히 쌓여도 나중에 검색과 관계도 기능을 만들 때 꽤 좋은 재료가 됩니다.

## 이미지 첨부

같은 폴더 기준 상대경로를 사용합니다.

```md
![이미지 설명](./images/chart.png)
```

이미지 설명은 화면에 보이지 않더라도 검색과 접근성에 도움이 되므로 짧게 적습니다.

## 권장 문서 길이

발표용 문서는 너무 길게 쓰기보다 스터디에서 바로 읽을 수 있게 구성합니다.

- 한 줄 요약: 1문장
- 핵심 내용: 3개 안팎
- 배운 점: 2-4개
- 토론거리: 1-3개
