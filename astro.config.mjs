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
      components: {
        Head: './src/components/Head.astro',
      },
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
                { label: '20260618', slug: 'study-leader/daily-news/20260618' },
                { label: '20260619', slug: 'study-leader/daily-news/20260619' },
                { label: '20260622', slug: 'study-leader/daily-news/20260622' },
                { label: '20260623', slug: 'study-leader/daily-news/20260623' },
                { label: '20260624', slug: 'study-leader/daily-news/20260624' },
                { label: '20260625', slug: 'study-leader/daily-news/20260625' },
                { label: '20260626', slug: 'study-leader/daily-news/20260626' },
                { label: '20260629', slug: 'study-leader/daily-news/20260629' },
                { label: '20260630', slug: 'study-leader/daily-news/20260630' },
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
                {
                  label: '260625 금리인상·리테일머니',
                  collapsed: true,
                  items: [
                    { label: '개요', slug: 'study-leader/economy-magazine/260625' },
                    { label: '[한경] 금리인상의 시간', slug: 'study-leader/economy-magazine/260625/interest-rate-hike' },
                    { label: '[한경] 금리인상, 증시는 반도체로 버틸 것', slug: 'study-leader/economy-magazine/260625/rate-hike-bill' },
                    { label: '[한경] 깨진 공식과 새로운 시대', slug: 'study-leader/economy-magazine/260625/broken-formula' },
                    { label: '[한경] 롯데의 완벽한 부활', slug: 'study-leader/economy-magazine/260625/lotte-revival' },
                    { label: '[매경] 달라진 돈줄기, 리테일 머니', slug: 'study-leader/economy-magazine/260625/retail-money' },
                    { label: '[매경] 머니무브 가속, 리테일 런 뇌관', slug: 'study-leader/economy-magazine/260625/money-move' },
                    { label: '[매경] 힘 세진 개미, 4가지 신풍속도', slug: 'study-leader/economy-magazine/260625/retail-newwave' },
                    { label: '[매경] 리테일 머니의 미래', slug: 'study-leader/economy-magazine/260625/retail-future' },
                  ],
                },
                {
                  label: '260701 부동산',
                  collapsed: true,
                  items: [
                    { label: '개요', slug: 'study-leader/economy-magazine/260701' },
                    { label: '[매경] 한강벨트 표심·보유세 조절', slug: 'study-leader/economy-magazine/260701/hangang-belt' },
                    { label: '[매경] 오세훈 5대 부동산 정책', slug: 'study-leader/economy-magazine/260701/seoul-housing-policy' },
                    { label: '[매경] 연말까지 집값 상승·수혜지', slug: 'study-leader/economy-magazine/260701/housing-outlook' },
                    { label: '[매경] 재건축 吳 vs 세금 李', slug: 'study-leader/economy-magazine/260701/oh-vs-lee' },
                  ],
                },
                {
                  label: '[책] 실거주 한 채 샀습니다만',
                  collapsed: true,
                  items: [
                    { label: '책 개요', slug: 'study-leader/economy-magazine/book-realestate' },
                    { label: '2장-01 가용자금 계산법', slug: 'study-leader/economy-magazine/book-realestate/ch2-01-available-funds' },
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
              collapsed: true,
              items: [
                { label: '3주차 개요', slug: 'gen-4/week-03-2026-06-17' },
                { label: '박선희', slug: 'gen-4/week-03-2026-06-17/park-sunhee' },
                { label: '윤혜상', slug: 'gen-4/week-03-2026-06-17/yun-hyesang' },
                { label: '서혜인', slug: 'gen-4/week-03-2026-06-17/seo-hyein' },
                { label: '강유리', slug: 'gen-4/week-03-2026-06-17/yuri-kang' },
                { label: '김요욱', slug: 'gen-4/week-03-2026-06-17/kim-yowook' },
                { label: '임현호', slug: 'gen-4/week-03-2026-06-17/hyunho' },
                { label: '송하영', slug: 'gen-4/week-03-2026-06-17/song-hayoung' },
                { label: '조수진', slug: 'gen-4/week-03-2026-06-17/sujin' },
              ],
            },
            {
              label: '4주차 (2026-06-25)',
              collapsed: false,
              items: [
                { label: '4주차 개요', slug: 'gen-4/week-04-2026-06-25' },
                { label: '윤혜상', slug: 'gen-4/week-04-2026-06-25/yun-hyesang' },
                { label: '강유리', slug: 'gen-4/week-04-2026-06-25/yuri-kang' },
                { label: '조수진', slug: 'gen-4/week-04-2026-06-25/sujin' },
                { label: '서혜인', slug: 'gen-4/week-04-2026-06-25/seo-hyein' },
                { label: '김요욱', slug: 'gen-4/week-04-2026-06-25/kim-yowook' },
              ],
            },
            {
              label: '5주차 (2026-07-01)',
              collapsed: false,
              items: [
                { label: '5주차 개요', slug: 'gen-4/week-05-2026-07-01' },
                {
                  label: '윤혜상',
                  collapsed: false,
                  items: [
                    { label: '보유세·한강벨트 표심', slug: 'gen-4/week-05-2026-07-01/yun-hyesang/property-tax' },
                    { label: '오세훈 5대 부동산 정책', slug: 'gen-4/week-05-2026-07-01/yun-hyesang/housing-policy' },
                  ],
                },
                { label: '서혜인', slug: 'gen-4/week-05-2026-07-01/seo-hyein' },
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
