import { defineCollection, z } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

const archiveMetadataSchema = z.object({
  author: z.string().optional(),
  date: z.union([z.string(), z.date()]).optional(),
  generation: z.number().optional(),
  week: z.number().optional(),
  tags: z.array(z.string()).default([]),
  keywords: z.array(z.string()).default([]),
  source: z
    .object({
      title: z.string().nullable().optional(),
      publication: z.string().nullable().optional(),
      publishedDate: z.union([z.string(), z.date()]).nullable().optional(),
      url: z.union([z.string().url(), z.literal('')]).nullable().optional(),
      section: z.string().nullable().optional(),
    })
    .optional(),
  entities: z
    .object({
      countries: z.array(z.string()).default([]),
      regions: z.array(z.string()).default([]),
      organizations: z.array(z.string()).default([]),
      companies: z.array(z.string()).default([]),
      people: z.array(z.string()).default([]),
      indicators: z.array(z.string()).default([]),
    })
    .optional(),
  related: z
    .object({
      topics: z.array(z.string()).default([]),
      pages: z.array(z.string()).default([]),
    })
    .optional(),
});

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({ extend: archiveMetadataSchema }),
  }),
};
