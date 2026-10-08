import { Fragment, ReactNode } from 'react';

function renderInline(text: string, key: string): ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts
    .filter((p) => p.length > 0)
    .map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return (
          <strong key={`${key}-${i}`} className="font-semibold text-slate-900 dark:text-white">
            {part.slice(2, -2)}
          </strong>
        );
      }
      return <Fragment key={`${key}-${i}`}>{part}</Fragment>;
    });
}

export default function MarkdownLite({
  text,
  className = '',
}: {
  text?: string | null;
  className?: string;
}) {
  if (!text || !text.trim()) {
    return <p className="text-sm text-slate-500 dark:text-slate-400">No content yet.</p>;
  }

  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const nodes: ReactNode[] = [];
  let buffer: string[] = [];
  let bufferStart = 0;

  const flush = () => {
    if (!buffer.length) return;
    const content = buffer.join('\n');
    nodes.push(
      <p
        key={`p-${bufferStart}`}
        className="whitespace-pre-line text-sm leading-7 text-slate-600 dark:text-slate-300"
      >
        {renderInline(content, `p-${bufferStart}`)}
      </p>
    );
    buffer = [];
  };

  lines.forEach((line, index) => {
    const heading = /^(#{1,4})\s+(.*)$/.exec(line);
    if (heading) {
      flush();
      nodes.push(
        <h3
          key={`h-${index}`}
          className="mt-4 text-base font-bold text-slate-900 first:mt-0 dark:text-white"
        >
          {renderInline(heading[2], `h-${index}`)}
        </h3>
      );
      return;
    }
    if (!line.trim()) {
      flush();
      return;
    }
    if (!buffer.length) bufferStart = index;
    buffer.push(line);
  });
  flush();

  return <div className={`space-y-3 ${className}`}>{nodes}</div>;
}
