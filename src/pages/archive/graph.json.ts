import { buildGraphPayload, getArchiveIndex } from '../../lib/archive-index';

export const prerender = true;

export async function GET() {
  const index = await getArchiveIndex();
  return new Response(JSON.stringify(buildGraphPayload(index)), {
    headers: {
      'content-type': 'application/json; charset=utf-8',
    },
  });
}
