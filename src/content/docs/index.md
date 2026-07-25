---
title: 경제잡지 스터디 아카이브
description: 경제잡지 스터디에서 매주 공유한 내용을 모아두는 공간입니다.
template: splash
hero:
  tagline: 기수별, 주차별, 발표자별로 공부한 내용을 찾고 이어서 볼 수 있습니다.
  actions:
    - text: 4기 보기
      link: /study-archive/gen-4/
      icon: right-arrow
    - text: 메타데이터 탐색
      link: /study-archive/archive/
      icon: right-arrow
      variant: secondary
    - text: 작성 가이드
      link: /study-archive/operations/writing-guide/
      variant: secondary
---

## 이번 아카이브의 목적

이 저장소는 경제잡지 스터디에서 매주 각자 맡은 기사와 주제를 공부하고 공유한 내용을 모아두는 공간입니다. 스터디 당일에는 웹 페이지를 열어 발표 순서대로 넘겨보고, 이후에는 검색으로 다시 찾아볼 수 있게 만드는 것을 목표로 합니다.

## 기본 탐색 흐름

- 기수별 페이지에서 전체 주차를 확인합니다.
- 주차별 페이지에서 발표자 목록과 순서를 확인합니다.
- 발표자 문서에서 각자가 정리한 공유 내용을 읽습니다.
- 문서 하단의 이전/다음 링크로 다음 발표자로 넘어갑니다.
- [색인](/study-archive/archive/entities/)과 [관계도](/study-archive/archive/graph/)에서 주제와 엔티티 기준으로 다시 탐색합니다.

## 빠른 작성 흐름

1. `templates/weekly-share.md`를 복사합니다.
2. `src/content/docs/gen-4/week-02-2026-06-11/{name}/index.md` 형태로 저장합니다.
3. 이미지는 같은 폴더 아래 `images/`에 넣고 `![설명](./images/file.png)`로 첨부합니다.
4. 본문은 발표자가 공유하기 좋은 흐름으로 자유롭게 구성합니다.
5. 로컬에서 `pnpm dev`로 확인한 뒤 커밋합니다.
