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
              collapsed: false,
              items: [
                { label: '데일리 뉴스 홈', slug: 'study-leader/daily-news' },
                { label: '20260608', slug: 'study-leader/daily-news/20260608' },
              ],
            },
            { label: '경제잡지', slug: 'study-leader/economy-magazine' },
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
              collapsed: false,
              items: [
                { label: '2주차 개요', slug: 'gen-4/week-02-2026-06-11' },
                {
                  label: '윤혜상',
                  collapsed: false,
                  items: [
                    { label: '테스트 공정', slug: 'gen-4/week-02-2026-06-11/yun-hyesang/semiconductor-test' },
                    { label: '패키징 공정', slug: 'gen-4/week-02-2026-06-11/yun-hyesang/semiconductor-packaging' },
                  ],
                },
                {
                  label: '서혜인',
                  collapsed: false,
                  items: [
                    { label: '포토공정', slug: 'gen-4/week-02-2026-06-11/seo-hyein/semiconductor-photo' },
                  ],
                },
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
