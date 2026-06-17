// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
  site: 'https://economy-magazine-study.github.io',
  base: '/study-archive',
  integrations: [
    starlight({
      title: '경제잡지 스터디 아카이브',
      description: '경제잡지 스터디에서 매주 공부하고 공유한 내용을 모아두는 아카이브입니다.',
      defaultLocale: 'ko',
      locales: { root: { label: '한국어', lang: 'ko' } },
      favicon: '/study-archive/favicon.svg',
      customCss: ['./src/styles/magazine-article.css'],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/economy-magazine-study/study-archive',
        },
      ],
      editLink: {
        baseUrl: 'https://github.com/economy-magazine-study/study-archive/edit/main/',
      },
      pagination: true,
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
      sidebar: [
        { label: '홈', slug: 'index' },
        {
          label: '스터디장',
          collapsed: false,
          items: [
            { label: '스터디장 공간', slug: 'study-leader' },
            {
              label: '데일리 뉴스',
              collapsed: true,
              items: [
                { label: '데일리 뉴스 홈', slug: 'study-leader/daily-news' },
                { label: '20260608', slug: 'study-leader/daily-news/20260608' },
                { label: '20260609', slug: 'study-leader/daily-news/20260609' },
                { label: '20260610', slug: 'study-leader/daily-news/20260610' },
                { label: '20260612', slug: 'study-leader/daily-news/20260612' },
                { label: '20260615', slug: 'study-leader/daily-news/20260615' },
                { label: '20260616', slug: 'study-leader/daily-news/20260616' },
                { label: '20260617', slug: 'study-leader/daily-news/20260617' },
              ],
            },
            {
              label: '경제잡지',
              collapsed: false,
              items: [
                { label: '경제잡지 홈', slug: 'study-leader/economy-magazine' },
                {
                  label: '260611 반도체/전력',
                  collapsed: true,
                  items: [
                    { label: '개요', slug: 'study-leader/economy-magazine/260611' },
                    { label: '[한경] 소부장 현실', slug: 'study-leader/economy-magazine/260611/semi-sobu' },
                    { label: '[한경] SK실트론 몸값', slug: 'study-leader/economy-magazine/260611/semi-siltron' },
                    { label: '[한경] 산화공정', slug: 'study-leader/economy-magazine/260611/semi-oxidation' },
                    { label: '[한경] HBM의 비결', slug: 'study-leader/economy-magazine/260611/semi-hbm' },
                    { label: '[한경] 식각공정', slug: 'study-leader/economy-magazine/260611/semi-etch' },
                    { label: '[한경] 증착공정', slug: 'study-leader/economy-magazine/260611/semi-deposition' },
                    { label: '[한경] 금속배선공정', slug: 'study-leader/economy-magazine/260611/semi-metal' },
                    { label: '[한경] 테스트공정', slug: 'study-leader/economy-magazine/260611/semi-test' },
                    { label: '[한경] 패키징공정', slug: 'study-leader/economy-magazine/260611/semi-packaging' },
                    { label: '[한경] 최태원 전략', slug: 'study-leader/economy-magazine/260611/semi-chey' },
                    { label: '[매경] K전력기기', slug: 'study-leader/economy-magazine/260611/power-kgrid' },
                    { label: '[매경] 몸값오른 전력기기', slug: 'study-leader/economy-magazine/260611/power-age' },
                    { label: '[매경] 그리드 쇼티지', slug: 'study-leader/economy-magazine/260611/power-shortage' },
                    { label: '[매경] 전력망 패키지', slug: 'study-leader/economy-magazine/260611/power-package' },
                  ],
                },
                {
                  label: '260617 투자전략',
                  collapsed: true,
                  items: [
                    { label: '개요', slug: 'study-leader/economy-magazine/260615' },
                    { label: '[매경] 핵심과 위성 전략', slug: 'study-leader/economy-magazine/260615/core-satellite' },
                    { label: '[한경] 자본주의 4.0시대', slug: 'study-leader/economy-magazine/260615/capitalism-40' },
                    { label: '[한경] 안정적 현금흐름 전략', slug: 'study-leader/economy-magazine/260615/cashflow-strategy' },
                    { label: '[한경] 사이클 읽는 능력', slug: 'study-leader/economy-magazine/260615/cycle-reading' },
                    { label: '[한경] 외인이 노리는 타이밍', slug: 'study-leader/economy-magazine/260615/foreign-timing' },
                    { label: '[한경] 돈은 병목으로 흐른다', slug: 'study-leader/economy-magazine/260615/bottleneck-investing' },
                    { label: '[한경] 공격과 방어의 균형전략', slug: 'study-leader/economy-magazine/260615/balance-strategy' },
                    { label: '[한경] 전쟁이 키운 비트코인', slug: 'study-leader/economy-magazine/260615/bitcoin-infrastructure' },
                    { label: '[한경] 제도가 시장을 만든다', slug: 'study-leader/economy-magazine/260615/institution-market' },
                  ],
                },
              ],
            },
            { label: '거시경제', slug: 'study-leader/macro-economy' },
          ],
        },
        {
          label: '4기',
          collapsed: false,
          items: [
            { label: '4기 홈', slug: 'gen-4' },
            {
              label: '2주차 (2026-06-11)',
              collapsed: true,
              items: [
                { label: '2주차 개요', slug: 'gen-4/week-02-2026-06-11' },
                { label: '김요욱', slug: 'gen-4/week-02-2026-06-11/kim-yowook' },
                {
                  label: '서혜인',
                  collapsed: false,
                  items: [
                    { label: '포토공정', slug: 'gen-4/week-02-2026-06-11/seo-hyein/semiconductor-photo' },
                    { label: '식각공정', slug: 'gen-4/week-02-2026-06-11/seo-hyein/semiconductor-etching' },
                  ],
                },
                {
                  label: '송하영',
                  collapsed: false,
                  items: [
                    { label: '증착공정', slug: 'gen-4/week-02-2026-06-11/song-hayoung/semiconductor-deposition' },
                    { label: '금속배선공정', slug: 'gen-4/week-02-2026-06-11/song-hayoung/semiconductor-metal' },
                  ],
                },
                {
                  label: '윤혜상',
                  collapsed: false,
                  items: [
                    { label: '테스트 공정', slug: 'gen-4/week-02-2026-06-11/yun-hyesang/semiconductor-test' },
                    { label: '패키징 공정', slug: 'gen-4/week-02-2026-06-11/yun-hyesang/semiconductor-packaging' },
                  ],
                },
                { label: '현호', slug: 'gen-4/week-02-2026-06-11/hyunho' },
                { label: '강유리', slug: 'gen-4/week-02-2026-06-11/yuri-kang' },
                { label: '이수진', slug: 'gen-4/week-02-2026-06-11/sujin' },
                { label: '심소연', slug: 'gen-4/week-02-2026-06-11/shim-soyeon' },
                {
                  label: 'sunnypark',
                  collapsed: false,
                  items: [
                    { label: '웨이퍼 (SK실트론)', slug: 'gen-4/week-02-2026-06-11/sunnypark/semiconductor-wafer' },
                    { label: '산화공정', slug: 'gen-4/week-02-2026-06-11/sunnypark/semiconductor-oxidation' },
                  ],
                },
              ],
            },
            {
              label: '3주차 (2026-06-17)',
              collapsed: false,
              items: [
                { label: '3주차 개요', slug: 'gen-4/week-03-2026-06-17' },
                { label: '윤혜상', slug: 'gen-4/week-03-2026-06-17/yun-hyesang' },
                { label: '서혜인', slug: 'gen-4/week-03-2026-06-17/seo-hyein' },
                { label: '강유리', slug: 'gen-4/week-03-2026-06-17/yuri-kang' },
                { label: '김요욱', slug: 'gen-4/week-03-2026-06-17/kim-yowook' },
              ],
            },
          ],
        },
        {
          label: '운영 문서',
          collapsed: true,
          items: [{ autogenerate: { directory: 'operations', collapsed: true } }],
        },
      ],
    }),
  ],
});
