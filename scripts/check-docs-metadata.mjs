import fs from 'node:fs';
import path from 'node:path';

const repoRoot = process.cwd();
const docsRoot = path.join(repoRoot, 'src/content/docs');
const astroConfigPath = path.join(repoRoot, 'astro.config.mjs');

const markdownExtensions = new Set(['.md', '.mdx']);

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) return walk(fullPath);
    return [fullPath];
  });
}

function toPosix(filePath) {
  return filePath.split(path.sep).join('/');
}

function relativeToRepo(filePath) {
  return toPosix(path.relative(repoRoot, filePath));
}

function getFrontmatter(source) {
  source = source.replace(/^\uFEFF/u, '');

  if (!source.startsWith('---\n')) return null;

  const end = source.indexOf('\n---', 4);
  if (end === -1) return null;

  return source.slice(4, end);
}

function getScalar(frontmatter, key) {
  const match = frontmatter.match(new RegExp(`^${key}:\\s*(.+)$`, 'm'));
  if (!match) return null;

  return match[1].trim().replace(/^['"]|['"]$/g, '');
}

function slugForDoc(filePath) {
  let relative = toPosix(path.relative(docsRoot, filePath));
  relative = relative.replace(/\.(md|mdx)$/u, '');
  return relative.endsWith('/index') ? relative.slice(0, -'/index'.length) : relative;
}

function isInsideImagesDirectory(filePath) {
  return toPosix(path.relative(docsRoot, filePath)).split('/').includes('images');
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function hasSlugInSidebar(configSource, slug) {
  const pattern = new RegExp(`slug:\\s*['"]${escapeRegExp(slug)}['"]`);
  return pattern.test(configSource);
}

function formatSuggestedSidebar(frontmatter, filePath) {
  const title = getScalar(frontmatter ?? '', 'title');
  const author = getScalar(frontmatter ?? '', 'author');
  const slug = path.basename(path.dirname(filePath));
  const label = author || title?.split(' - ')[0] || slug;

  return ['sidebar:', `  label: ${label}`, '  order: 1'].join('\n');
}

function findWeeklyDocInfo(filePath) {
  const relative = toPosix(path.relative(docsRoot, filePath));
  const match = relative.match(/^(gen-\d+\/week-\d{2}-\d{4}-\d{2}-\d{2})\/(.+)\/index\.(md|mdx)$/u);
  if (!match) return null;

  return {
    weekPath: match[1],
    docPathInsideWeek: match[2],
    weekIndexPath: path.join(docsRoot, match[1], 'index.md'),
  };
}

function hasWeekIndexLink(weekIndexSource, docPathInsideWeek) {
  const escaped = escapeRegExp(docPathInsideWeek);
  return new RegExp(`\\]\\(\\./${escaped}/\\)`).test(weekIndexSource);
}

const docs = walk(docsRoot).filter((filePath) => markdownExtensions.has(path.extname(filePath)));
const astroConfig = fs.readFileSync(astroConfigPath, 'utf8');

const missingSidebar = [];
const missingWeekIndexEntries = [];
const missingStarlightSidebarEntries = [];

for (const docPath of docs) {
  const relative = relativeToRepo(docPath);
  const source = fs.readFileSync(docPath, 'utf8');
  const frontmatter = getFrontmatter(source);
  const isRootIndex = relative === 'src/content/docs/index.md';
  const isImageDirectoryFile = isInsideImagesDirectory(docPath);

  if (!isRootIndex && !isImageDirectoryFile && !/^sidebar:\s*$/m.test(frontmatter ?? '')) {
    missingSidebar.push({
      path: relative,
      suggestion: formatSuggestedSidebar(frontmatter, docPath),
    });
  }

  const weeklyInfo = isImageDirectoryFile ? null : findWeeklyDocInfo(docPath);
  if (weeklyInfo) {
    const weekIndexRelative = relativeToRepo(weeklyInfo.weekIndexPath);
    const weekIndexSource = fs.existsSync(weeklyInfo.weekIndexPath)
      ? fs.readFileSync(weeklyInfo.weekIndexPath, 'utf8')
      : '';

    if (!hasWeekIndexLink(weekIndexSource, weeklyInfo.docPathInsideWeek)) {
      missingWeekIndexEntries.push({
        path: relative,
        weekIndexPath: weekIndexRelative,
        expectedLink: `./${weeklyInfo.docPathInsideWeek}/`,
      });
    }

    const slug = slugForDoc(docPath);
    if (!hasSlugInSidebar(astroConfig, slug)) {
      missingStarlightSidebarEntries.push({
        path: relative,
        slug,
      });
    }
  }
}

if (
  missingSidebar.length === 0 &&
  missingWeekIndexEntries.length === 0 &&
  missingStarlightSidebarEntries.length === 0
) {
  console.log('Docs metadata check passed.');
  process.exit(0);
}

console.error('\nDocs metadata check failed.\n');
console.error('새 문서를 추가할 때 누락되기 쉬운 항목이 있습니다. 자동 수정은 하지 않았습니다.');
console.error('아래 경고를 그대로 반영한 뒤 다시 `pnpm docs:check`를 실행하세요.\n');

if (missingSidebar.length > 0) {
  console.error('Missing frontmatter `sidebar`:');
  for (const item of missingSidebar) {
    console.error(`- ${item.path}`);
    console.error('  Add this inside the frontmatter:');
    for (const line of item.suggestion.split('\n')) {
      console.error(`    ${line}`);
    }
  }
  console.error('');
}

if (missingWeekIndexEntries.length > 0) {
  console.error('Missing weekly index entry:');
  for (const item of missingWeekIndexEntries) {
    console.error(`- ${item.path}`);
    console.error(`  Update: ${item.weekIndexPath}`);
    console.error(`  Add a row in the 발표 순서 table with link: [문서 보기](${item.expectedLink})`);
  }
  console.error('');
}

if (missingStarlightSidebarEntries.length > 0) {
  console.error('Missing Starlight sidebar entry in astro.config.mjs:');
  for (const item of missingStarlightSidebarEntries) {
    console.error(`- ${item.path}`);
    console.error(`  Add a sidebar item with slug: '${item.slug}'`);
  }
  console.error('');
}

console.error('Pre-commit/CI hint: 이 메시지는 AI 코딩 도구가 후속 수정에 그대로 사용할 수 있도록 파일 경로와 기대값을 포함합니다.');
process.exit(1);
