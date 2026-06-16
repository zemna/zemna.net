---
title: "54개 디자인 시스템 해부해서 내 Hugo 블로그에 Linear.app DNA를 이식한 하루"
date: 2026-06-16T18:00:00+07:00
draft: false
description: "popular-web-designs 스킬로 54개 실제 서비스 디자인 시스템을 분석하고, Linear.app의 디자인 토큰을 Hugo 정적 블로그에 통째로 이식한 과정. MiniMax, GLM, GPT 모델 3종을 번갈아가며 같은 작업을 시켜본 비교 후기도 담았다."
cover: "covers/linear-design-system.png"
categories: ["Build"]
tags: ["Design-System", "Hugo", "Linear", "CSS", "AI-Agent", "Build-in-Public", "Hermes"]
---

오늘 아침 내 블로그 zemna.net을 열어봤다. 구렸다. 아니, 정확히 말하면 "구리다"라고 내 에이전트에게 직설적으로 말했다.

15년차 개발자 블로그가 2015년 티스토리보다 못한 디자인이라는 게 용납이 안 됐다. 그래서 Hermes 에이전트에게 요구했다. "54개 디자인 시스템 다 뒤져서 제일 나은 걸로 갈아엎어."

## 54개 중에 Linear.app을 고른 이유

`popular-web-designs`라는 Hermes 스킬이 있다. Stripe, Linear, Vercel, Notion, Figma 등 실제 서비스 54개의 디자인 토큰과 CSS 패턴을 템플릿화해둔 스킬이다.

에이전트가 5개를 추천했다:

| 디자인 | 특징 | 적합도 |
|---|---|---|
| **Linear.app** | 다크모드 네이티브, 3-tier weight, indigo accent | ★★★★★ |
| Vercel | Black & white, Geist font | ★★★★ |
| Stripe | Purple gradient, marketing | ★★★ |
| Sanity | Red accent, editorial | ★★★ |
| Framer | Bold + motion | ★★ |

Linear.app을 선택한 이유는 간단하다. **IT/AI 개발자 블로그의 정석**이기 때문. 다크모드가 기본이고, 과하지 않은 indigo accent, 3단계 font-weight 시스템이 코드 블록과 기술 문서에 최적화되어 있다.

## 디자인 토큰을 Hugo로 이식하기

Linear의 디자인 시스템에서 추출한 핵심 요소:

```css
/* 다크모드 네이티브 */
--zn-surface-0: #08090a;  /* 거의 검정 — Linear의 marketing black */

/* 3-tier weight — Linear 시그니처 */
--zn-wt-read: 400;   /* body */
--zn-wt-ui: 510;     /* UI 강조 */
--zn-wt-strong: 590; /* strong */

/* 반투명 white border — Linear의 다크 on 다크 */
--zn-border-subtle: rgba(255, 255, 255, 0.05);
--zn-border:        rgba(255, 255, 255, 0.08);
--zn-border-strong: rgba(255, 255, 255, 0.12);
```

이걸 Hugo의 `assets/css/tokens.css`로 옮겼다. `theme.css`, `article.css`, `featured.css`, `interactions.css`까지 총 5개 CSS 파일을 Linear 원칙으로 재작성했다. 811줄 추가, 706줄 삭제.

가장 신경 쓴 부분은 **Zemnanet 브랜드와 Linear DNA를 충돌 없이 섞는 것**이었다.

| 요소 | Zemnanet 브랜드 | Linear DNA |
|---|---|---|
| Primary | Navy `#1A2238` | Indigo `#5e6ad2` (accent로) |
| Accent | Vermilion `#E34234` | 유지 (Zernio와 일관성) |
| 배경 | — | `#08090a` (Linear 채택) |
| 폰트 | D2Coding | Inter Variable + cv01/ss03 |

결론: **Linear의 구조 위에 Zemnanet의 색을 얹었다.** Indigo는 CTA와 강조에만 쓰고, Vermilion은 유지해서 Zernio 브랜드와의 연결성을 놓치지 않았다.

## AI 모델 3종을 번갈아 써봤다

이 작업을 하면서 의도치 않게 모델 비교 실험이 됐다. 같은 작업을 세 모델에게 시켰다:

| 모델 | Provider | 디자인 작업 평가 |
|---|---|---|
| **MiniMax-M3** | — | 초기 시도. 디자인 감각은 있으나 세부 오차 많음 |
| **GLM-5.1** | OpenCode Go | 구조적 사고 우수. 템플릿/로직 이해 빠름. 버그 수정 정확 |
| **GPT-5.5** | OpenAI Codex | 전수 점검 + 로고 + SEO 최적화. 마무리 단계에 탁월 |

느낀 점: **한 모델로 처음부터 끝까지 하는 것보다, 역할을 나누는 게 낫다.** GLM으로 구조 잡고 MiniMax로 초안 만들고 GPT로 마무리. 사람 팀처럼 굴리는 게 결과물이 좋다.

## 결과물

하루 만에 바뀐 것들:

- **다크모드** — `#08090a` 배경, 반투명 border, indigo-accented CTA
- **폰트** — D2Coding 전역 적용. 코드와 본문의 구분이 자연스러움
- **히어로** — 자카르타 스카이라인 골든아워 배경 + 그라디언트 오버레이
- **Tags/Topics** — `/tags/` 클라우드, `/categories/` 토픽 페이지
- **여백** — 히어로 8rem→5rem, 섹션 6rem→4rem 등 전체 압축
- **로고** — Z 브릿지 마크 + indigo routing + vermilion signal dot
- **SEO** — OG 메타, favicon, 깨진 링크 3개 수정

총 Git 커밋 3회, 21개 파일 변경, CSS 1,500줄 재작성.

## 교훈

1. **54개 중에 고르는 게 3개 중에 고르는 것보다 빠르다.** 선택지가 많을수록 기준이 명확해진다.
2. **AI 에이전트한테 "이거 구리다"라고 말해도 된다.** 오히려 직설적인 피드백이 더 나은 결과를 낸다.
3. **Static site도 디자인 시스템을 가질 수 있다.** Hugo + CSS custom properties면 충분하다. 별도 도구 필요 없다.
4. **모델별로 잘하는 게 다르다.** 구조는 GLM, 디테일은 GPT. 멀티모델 파이프라인이 답이다.

---

라이브 사이트: [zemna.net](https://zemna.net)

GitHub: [github.com/zemna/zemna.net](https://github.com/zemna/zemna.net)
