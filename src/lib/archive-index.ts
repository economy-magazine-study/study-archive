import { getCollection } from 'astro:content';

export const archiveFacetTypes = [
  'countries',
  'regions',
  'organizations',
  'companies',
  'people',
  'indicators',
  'topics',
  'tags',
  'keywords',
] as const;

export type ArchiveFacetType = (typeof archiveFacetTypes)[number];

export type ArchiveFacetMeta = {
  label: string;
  group: 'entities' | 'topics';
  description: string;
  weight: number;
};

export const archiveFacetMeta: Record<ArchiveFacetType, ArchiveFacetMeta> = {
  countries: { label: '국가', group: 'entities', description: '국가 단위로 연결된 글', weight: 0.5 },
  regions: { label: '지역', group: 'entities', description: '도시, 권역, 생활권', weight: 3 },
  organizations: { label: '기관', group: 'entities', description: '정부, 연구기관, 금융기관, 매체', weight: 3 },
  companies: { label: '기업', group: 'entities', description: '기업과 브랜드', weight: 5 },
  people: { label: '인물', group: 'entities', description: '인터뷰이, 저자, 정책 인물', weight: 4 },
  indicators: { label: '지표', group: 'entities', description: '경제·산업·부동산 지표와 제도', weight: 3 },
  topics: { label: '주제', group: 'topics', description: 'related.topics 기반 주제', weight: 2 },
  tags: { label: '태그', group: 'topics', description: '문서 태그', weight: 1 },
  keywords: { label: '키워드', group: 'topics', description: '세부 키워드', weight: 1 },
};

export type ArchiveDoc = {
  id: string;
  slug: string;
  title: string;
  description: string;
  author: string;
  date: string;
  generation: number | null;
  week: number | null;
  weekLabel: string;
  sourceTitle: string;
  publication: string;
  facets: Record<ArchiveFacetType, string[]>;
};

export type ArchiveFacet = {
  type: ArchiveFacetType;
  id: string;
  key: string;
  name: string;
  label: string;
  group: ArchiveFacetMeta['group'];
  description: string;
  count: number;
  weight: number;
  docIds: string[];
};

export type ArchiveIndex = {
  docs: ArchiveDoc[];
  facets: ArchiveFacet[];
  docsById: Map<string, ArchiveDoc>;
  facetsByType: Map<ArchiveFacetType, ArchiveFacet[]>;
  facetsByKey: Map<string, ArchiveFacet>;
};

type RawDocData = {
  title?: string;
  description?: string;
  author?: string;
  date?: string | Date;
  generation?: number;
  week?: number;
  tags?: string[];
  keywords?: string[];
  source?: {
    title?: string | null;
    publication?: string | null;
  };
  entities?: Partial<Record<'countries' | 'regions' | 'organizations' | 'companies' | 'people' | 'indicators', string[]>>;
  related?: {
    topics?: string[];
  };
};

let archiveIndexCache: Promise<ArchiveIndex> | undefined;

export function withBase(path: string) {
  const base = (import.meta.env.BASE_URL ?? '/').replace(/\/?$/u, '/');
  const cleanPath = path.replace(/^\/+/, '');
  return `${base}${cleanPath}`;
}

export function docHref(slug: string) {
  return withBase(`${slug}/`);
}

export function entityHref(type: ArchiveFacetType, id: string) {
  return withBase(`archive/entities/${type}/${id}/`);
}

export function getArchiveIndex() {
  if (import.meta.env.DEV) return buildArchiveIndex();
  archiveIndexCache ??= buildArchiveIndex();
  return archiveIndexCache;
}

export function groupFacets(index: ArchiveIndex) {
  return archiveFacetTypes.map((type) => ({
    type,
    ...archiveFacetMeta[type],
    facets: index.facetsByType.get(type) ?? [],
  }));
}

export function getFacetDetail(index: ArchiveIndex, type: ArchiveFacetType, id: string) {
  const facet = index.facetsByKey.get(facetLookupKey(type, id));
  if (!facet) return null;

  const docs = facet.docIds
    .map((docId) => index.docsById.get(docId))
    .filter((doc): doc is ArchiveDoc => Boolean(doc));

  const cooccurrences = new Map<string, { facet: ArchiveFacet; count: number; score: number }>();
  for (const doc of docs) {
    for (const candidate of facetsForDoc(index, doc)) {
      if (candidate.type === facet.type && candidate.id === facet.id) continue;
      const key = facetLookupKey(candidate.type, candidate.id);
      const current = cooccurrences.get(key) ?? { facet: candidate, count: 0, score: 0 };
      current.count += 1;
      current.score += candidate.weight;
      cooccurrences.set(key, current);
    }
  }

  return {
    facet,
    docs,
    cooccurrences: Array.from(cooccurrences.values()).sort(
      (a, b) => b.count - a.count || b.score - a.score || a.facet.name.localeCompare(b.facet.name, 'ko'),
    ),
  };
}

export function buildGraphPayload(index: ArchiveIndex) {
  return {
    generatedAt: new Date().toISOString(),
    docs: index.docs.map((doc) => ({
      id: doc.id,
      title: doc.title,
      author: doc.author,
      date: doc.date,
      week: doc.week,
      weekLabel: doc.weekLabel,
      href: docHref(doc.slug),
      facets: archiveFacetTypes.flatMap((type) =>
        doc.facets[type].map((value) => ({
          type,
          id: entityId(value),
          key: entityKey(value),
          name: value,
          weight: archiveFacetMeta[type].weight,
        })),
      ),
    })),
    facets: index.facets.map((facet) => ({
      type: facet.type,
      id: facet.id,
      key: facet.key,
      name: facet.name,
      label: facet.label,
      group: facet.group,
      count: facet.count,
      weight: facet.weight,
      href: entityHref(facet.type, facet.id),
      broad: facet.count >= Math.max(12, Math.ceil(index.docs.length * 0.35)),
      docIds: facet.docIds,
    })),
    facetTypes: archiveFacetTypes.map((type) => ({
      type,
      ...archiveFacetMeta[type],
    })),
  };
}

function facetsForDoc(index: ArchiveIndex, doc: ArchiveDoc) {
  const facets: ArchiveFacet[] = [];
  for (const type of archiveFacetTypes) {
    for (const value of doc.facets[type]) {
      const facet = index.facetsByKey.get(facetLookupKey(type, entityId(value)));
      if (facet) facets.push(facet);
    }
  }
  return facets;
}

async function buildArchiveIndex(): Promise<ArchiveIndex> {
  const entries = await getCollection('docs');
  const docs = entries
    .map((entry) => {
      const slug = normalizeDocSlug(entry.id);
      if (!isParticipantDoc(slug)) return null;
      return buildArchiveDoc(slug, entry.data as RawDocData);
    })
    .filter((doc): doc is ArchiveDoc => Boolean(doc))
    .sort((a, b) => a.date.localeCompare(b.date) || (a.week ?? 0) - (b.week ?? 0) || a.title.localeCompare(b.title, 'ko'));

  const docsById = new Map(docs.map((doc) => [doc.id, doc]));
  const facetRecords = new Map<string, ArchiveFacet>();

  for (const doc of docs) {
    for (const type of archiveFacetTypes) {
      for (const value of doc.facets[type]) {
        const id = entityId(value);
        const key = facetLookupKey(type, id);
        const existing = facetRecords.get(key);
        if (existing) {
          if (!existing.docIds.includes(doc.id)) existing.docIds.push(doc.id);
          continue;
        }

        const meta = archiveFacetMeta[type];
        facetRecords.set(key, {
          type,
          id,
          key: entityKey(value),
          name: value,
          label: meta.label,
          group: meta.group,
          description: meta.description,
          count: 0,
          weight: meta.weight,
          docIds: [doc.id],
        });
      }
    }
  }

  const facets = Array.from(facetRecords.values())
    .map((facet) => ({ ...facet, count: facet.docIds.length }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name, 'ko'));

  const facetsByType = new Map<ArchiveFacetType, ArchiveFacet[]>();
  for (const type of archiveFacetTypes) {
    facetsByType.set(
      type,
      facets.filter((facet) => facet.type === type),
    );
  }

  const facetsByKey = new Map(facets.map((facet) => [facetLookupKey(facet.type, facet.id), facet]));

  return { docs, facets, docsById, facetsByType, facetsByKey };
}

function buildArchiveDoc(slug: string, data: RawDocData): ArchiveDoc {
  const entities = data.entities ?? {};
  const facets: Record<ArchiveFacetType, string[]> = {
    countries: normalizeList(entities.countries),
    regions: normalizeList(entities.regions),
    organizations: normalizeList(entities.organizations),
    companies: normalizeList(entities.companies),
    people: normalizeList(entities.people),
    indicators: normalizeList(entities.indicators),
    topics: normalizeList(data.related?.topics),
    tags: normalizeList(data.tags),
    keywords: normalizeList(data.keywords),
  };

  return {
    id: slug,
    slug,
    title: data.title ?? slug,
    description: data.description ?? '',
    author: data.author ?? '',
    date: dateToString(data.date),
    generation: data.generation ?? null,
    week: data.week ?? null,
    weekLabel: data.week ? `${data.week}주차` : '',
    sourceTitle: data.source?.title ?? '',
    publication: data.source?.publication ?? '',
    facets,
  };
}

function isParticipantDoc(slug: string) {
  return /^gen-\d+\/week-\d{2}-\d{4}-\d{2}-\d{2}\/.+/u.test(slug) && !slug.split('/').includes('images');
}

function normalizeDocSlug(id: string) {
  return id
    .replace(/^src\/content\/docs\//u, '')
    .replace(/\.(md|mdx)$/u, '')
    .replace(/\/index$/u, '');
}

function normalizeList(values: string[] | undefined) {
  const seen = new Set<string>();
  const normalized: string[] = [];
  for (const value of values ?? []) {
    const clean = value?.toString().normalize('NFKC').replace(/\s+/gu, ' ').trim();
    if (!clean) continue;
    const key = entityKey(clean);
    if (seen.has(key)) continue;
    seen.add(key);
    normalized.push(clean);
  }
  return normalized;
}

function dateToString(value: string | Date | undefined) {
  if (!value) return '';
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  return value;
}

export function entityKey(value: string) {
  return value.normalize('NFKC').replace(/\s+/gu, ' ').trim().toLocaleLowerCase('ko-KR');
}

export function entityId(value: string) {
  const key = entityKey(value);
  return (
    key
      .replace(/[^\p{Letter}\p{Number}]+/gu, '-')
      .replace(/^-+|-+$/gu, '')
      .replace(/-{2,}/gu, '-') || 'item'
  );
}

function facetLookupKey(type: ArchiveFacetType, id: string) {
  return `${type}:${id}`;
}
