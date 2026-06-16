// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
  site: 'https://economy-magazine-study.github.io',
  base: '/study-archive',
  integrations: [
    starlight({
      title: '寃쎌젣?≪? ?ㅽ꽣???꾩뭅?대툕',
      description: '寃쎌젣?≪? ?ㅽ꽣?붿뿉??留ㅼ＜ 怨듬??섍퀬 怨듭쑀???댁슜??紐⑥븘?먮뒗 ?꾩뭅?대툕?낅땲??',
      defaultLocale: 'ko',
      locales: { root: { label: '?쒓뎅??, lang: 'ko' } },
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
        { label: '??, slug: 'index' },
        {
          label: '?ㅽ꽣?붿옣',
          collapsed: false,
          items: [
            { label: '?ㅽ꽣?붿옣 怨듦컙', slug: 'study-leader' },
            {
              label: '?곗씪由??댁뒪',
              collapsed: false,
              items: [
                { label: '?곗씪由??댁뒪 ??, slug: 'study-leader/daily-news' },
                { label: '20260608', slug: 'study-leader/daily-news/20260608' },
                { label: '20260609', slug: 'study-leader/daily-news/20260609' },
                { label: '20260610', slug: 'study-leader/daily-news/20260610' },
                { label: '20260612', slug: 'study-leader/daily-news/20260612' },
                { label: '20260615', slug: 'study-leader/daily-news/20260615' },
                { label: '20260616', slug: 'study-leader/daily-news/20260616' },
              ],
            },
            {
              label: '寃쎌젣?≪?',
              collapsed: false,
              items: [
                { label: '寃쎌젣?≪? ??, slug: 'study-leader/economy-magazine' },
                {
                  label: '260611 諛섎룄泥??꾨젰',
                  collapsed: false,
                  items: [
                    { label: '媛쒖슂', slug: 'study-leader/economy-magazine/260611' },
                    { label: '[?쒓꼍] ?뚮????꾩떎', slug: 'study-leader/economy-magazine/260611/semi-sobu' },
                    { label: '[?쒓꼍] SK?ㅽ듃濡?紐멸컪', slug: 'study-leader/economy-magazine/260611/semi-siltron' },
                    { label: '[?쒓꼍] ?고솕怨듭젙', slug: 'study-leader/economy-magazine/260611/semi-oxidation' },
                    { label: '[?쒓꼍] HBM??鍮꾧껐', slug: 'study-leader/economy-magazine/260611/semi-hbm' },
                    { label: '[?쒓꼍] ?앷컖怨듭젙', slug: 'study-leader/economy-magazine/260611/semi-etch' },
                    { label: '[?쒓꼍] 利앹갑怨듭젙', slug: 'study-leader/economy-magazine/260611/semi-deposition' },
                    { label: '[?쒓꼍] 湲덉냽諛곗꽑怨듭젙', slug: 'study-leader/economy-magazine/260611/semi-metal' },
                    { label: '[?쒓꼍] ?뚯뒪?멸났??, slug: 'study-leader/economy-magazine/260611/semi-test' },
                    { label: '[?쒓꼍] ?⑦궎吏뺢났??, slug: 'study-leader/economy-magazine/260611/semi-packaging' },
                    { label: '[?쒓꼍] 理쒗깭???꾨왂', slug: 'study-leader/economy-magazine/260611/semi-chey' },
                    { label: '[留ㅺ꼍] K?꾨젰湲곌린', slug: 'study-leader/economy-magazine/260611/power-kgrid' },
                    { label: '[留ㅺ꼍] 紐멸컪?ㅻⅨ ?꾨젰湲곌린', slug: 'study-leader/economy-magazine/260611/power-age' },
                    { label: '[留ㅺ꼍] 洹몃━???쇳떚吏', slug: 'study-leader/economy-magazine/260611/power-shortage' },
                    { label: '[留ㅺ꼍] ?꾨젰留??⑦궎吏', slug: 'study-leader/economy-magazine/260611/power-package' },
                  ],
                },
              ],
            },
            { label: '嫄곗떆寃쎌젣', slug: 'study-leader/macro-economy' },
          ],
        },
        {
          label: '4湲?,
          collapsed: false,
          items: [
            { label: '4湲???, slug: 'gen-4' },
            {
              label: '2二쇱감 (2026-06-11)',
              collapsed: false,
              items: [
                { label: '2二쇱감 媛쒖슂', slug: 'gen-4/week-02-2026-06-11' },
                { label: '源?붿슧', slug: 'gen-4/week-02-2026-06-11/kim-yowook' },
                {
                  label: '?쒗삙??,
                  collapsed: false,
                  items: [
                    { label: '?ы넗怨듭젙', slug: 'gen-4/week-02-2026-06-11/seo-hyein/semiconductor-photo' },
                    { label: '?앷컖怨듭젙', slug: 'gen-4/week-02-2026-06-11/seo-hyein/semiconductor-etching' },
                  ],
                },
                {
                  label: '?≫븯??,
                  collapsed: false,
                  items: [
                    { label: '利앹갑怨듭젙', slug: 'gen-4/week-02-2026-06-11/song-hayoung/semiconductor-deposition' },
                    { label: '湲덉냽諛곗꽑怨듭젙', slug: 'gen-4/week-02-2026-06-11/song-hayoung/semiconductor-metal' },
                  ],
                },
                {
                  label: '?ㅽ삙??,
                  collapsed: false,
                  items: [
                    { label: '?뚯뒪??怨듭젙', slug: 'gen-4/week-02-2026-06-11/yun-hyesang/semiconductor-test' },
                    { label: '?⑦궎吏?怨듭젙', slug: 'gen-4/week-02-2026-06-11/yun-hyesang/semiconductor-packaging' },
                  ],
                },
                { label: '?꾪쁽??, slug: 'gen-4/week-02-2026-06-11/hyunho' },
                { label: '媛뺤쑀由?, slug: 'gen-4/week-02-2026-06-11/yuri-kang' },
                { label: '議곗닔吏?, slug: 'gen-4/week-02-2026-06-11/sujin' },
                { label: '?ъ냼??, slug: 'gen-4/week-02-2026-06-11/shim-soyeon' },
                {
                  label: 'sunnypark',
                  collapsed: false,
                  items: [
                    { label: '?⑥씠???쒖“ (SK?ㅽ듃濡?', slug: 'gen-4/week-02-2026-06-11/sunnypark/semiconductor-wafer' },
                    { label: '?고솕怨듭젙', slug: 'gen-4/week-02-2026-06-11/sunnypark/semiconductor-oxidation' },
                  ],
                },
              ],
            },
            {
              label: '3二쇱감 (2026-06-17)',
              collapsed: false,
              items: [
                { label: '3二쇱감 媛쒖슂', slug: 'gen-4/week-03-2026-06-17' },
                { label: '?ㅽ삙??, slug: 'gen-4/week-03-2026-06-17/yun-hyesang' },
              ],
            },
          ],
        },
        {
          label: '?댁쁺 臾몄꽌',
          collapsed: true,
          items: [{ autogenerate: { directory: 'operations', collapsed: true } }],
        },
      ],
    }),
  ],
});

