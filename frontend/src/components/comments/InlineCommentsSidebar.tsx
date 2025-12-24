import React, { useMemo } from "react";
import { Comment } from "../../types/comments";

interface InlineCommentsSidebarProps {
  comments: Comment[];
  onSelectComment?: (comment: Comment) => void;
}

function selectionLabel(comment: Comment) {
  if (comment.selection?.textPreview) return comment.selection.textPreview;
  if (comment.selection?.blockId) return `Block ${comment.selection.blockId}`;
  return "Selected text";
}

export const InlineCommentsSidebar: React.FC<InlineCommentsSidebarProps> = ({
  comments,
  onSelectComment,
}) => {
  const grouped = useMemo(() => {
    const groups = new Map<string, Comment[]>();
    comments
      .filter((c) => c.selection)
      .forEach((comment) => {
        const key = `${comment.selection?.blockId || "page"}-${comment.selection?.startOffset ?? 0}-${comment.selection?.endOffset ?? 0}`;
        const existing = groups.get(key) ?? [];
        existing.push(comment);
        groups.set(key, existing);
      });
    return Array.from(groups.entries());
  }, [comments]);

  return (
    <aside className="inline-comments">
      <h4>Inline comments</h4>
      {grouped.length === 0 && <div className="inline-comments__empty">No inline comments</div>}
      <ul className="inline-comments__list">
        {grouped.map(([key, items]) => (
          <li key={key} className="inline-comments__group">
            <div className="inline-comments__reference">{selectionLabel(items[0])}</div>
            <ul>
              {items.map((comment) => (
                <li key={comment.id}>
                  <button
                    type="button"
                    className="inline-comments__comment"
                    onClick={() => onSelectComment?.(comment)}
                  >
                    <div className="inline-comments__comment-meta">
                      <span className="inline-comments__author">{comment.author.name}</span>
                      <span className="inline-comments__timestamp">{new Date(comment.createdAt).toLocaleString()}</span>
                    </div>
                    <div className="inline-comments__content">{comment.content}</div>
                  </button>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </aside>
  );
};
