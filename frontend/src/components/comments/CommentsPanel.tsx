import React, { useEffect, useMemo, useState } from "react";
import { Comment, CreateCommentPayload } from "../../types/comments";
import { CommentForm } from "./CommentForm";
import { CommentsList } from "./CommentsList";
import { InlineCommentsSidebar } from "./InlineCommentsSidebar";
import { createComment, fetchComments, resolveComment } from "../../api/comments";
import { useInlineSelection } from "../../hooks/useInlineSelection";

interface CommentsPanelProps {
  pageId: string;
  contentContainerSelector?: string;
}

function buildTree(comments: Comment[]): Comment[] {
  const map = new Map<string, Comment & { replies: Comment[] }>();
  comments.forEach((c) => map.set(c.id, { ...c, replies: c.replies ?? [] }));
  const roots: Comment[] = [];

  map.forEach((comment) => {
    if (comment.parentId) {
      const parent = map.get(comment.parentId);
      if (parent) {
        parent.replies = parent.replies || [];
        parent.replies.push(comment);
      } else {
        roots.push(comment);
      }
    } else {
      roots.push(comment);
    }
  });

  return roots;
}

export const CommentsPanel: React.FC<CommentsPanelProps> = ({ pageId, contentContainerSelector }) => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const { selection, clearSelection, captureSelection } = useInlineSelection({
    contentContainerSelector,
  });

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const data = await fetchComments(pageId);
        setComments(data);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [pageId]);

  const thread = useMemo(() => buildTree(comments), [comments]);

  const addComment = async (content: string, parentId?: string) => {
    const payload: CreateCommentPayload = {
      content,
      pageId,
      parentId,
      selection: parentId ? undefined : selection || undefined,
    };
    const created = await createComment(payload);
    setComments((prev) => [...prev, created]);
    clearSelection();
  };

  const toggleResolve = async (commentId: string, resolved: boolean) => {
    const updated = await resolveComment(commentId, resolved);
    setComments((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
  };

  const scrollToSelection = (comment: Comment) => {
    if (!comment.selection) return;
    const { blockId } = comment.selection;
    if (blockId) {
      const target = document.querySelector(`[data-block-id="${blockId}"]`);
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "center" });
        target.classList.add("inline-comment--highlight");
        setTimeout(() => target.classList.remove("inline-comment--highlight"), 2000);
      }
    }
  };

  return (
    <div className="comments-panel">
      <div className="comments-panel__header">
        <h3>Comments</h3>
        {selection && (
          <div className="comments-panel__selection">
            Replying to selection: <em>{selection.textPreview || "selected text"}</em>
            <button type="button" onClick={clearSelection}>
              Clear
            </button>
          </div>
        )}
      </div>

      <CommentForm
        onSubmit={(value) => addComment(value)}
        placeholder={selection ? "Add a comment for the selected text" : "Add a comment"}
        submitLabel="Post comment"
      />

      {loading ? (
        <div>Loading comments…</div>
      ) : (
        <CommentsList comments={thread} onReply={(parentId, value) => addComment(value, parentId)} onResolve={toggleResolve} />
      )}

      <InlineCommentsSidebar
        comments={comments.filter((c) => c.selection)}
        onSelectComment={(comment) => {
          scrollToSelection(comment);
          captureSelection();
        }}
      />
    </div>
  );
};
