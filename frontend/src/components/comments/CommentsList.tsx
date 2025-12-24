import React, { useMemo, useState } from "react";
import { Comment } from "../../types/comments";
import { CommentForm } from "./CommentForm";

interface CommentsListProps {
  comments: Comment[];
  onReply: (parentId: string, content: string) => Promise<void> | void;
  onResolve?: (commentId: string, resolved: boolean) => Promise<void> | void;
}

const formatDate = (value: string) => new Date(value).toLocaleString();

const CommentItem: React.FC<{
  comment: Comment;
  onReply: (parentId: string, content: string) => Promise<void> | void;
  onResolve?: (commentId: string, resolved: boolean) => Promise<void> | void;
  depth?: number;
}> = ({ comment, onReply, onResolve, depth = 0 }) => {
  const [isReplying, setReplying] = useState(false);
  const handleReply = async (content: string) => {
    await onReply(comment.id, content);
    setReplying(false);
  };

  return (
    <li className="comment-item" data-comment-id={comment.id} style={{ marginLeft: depth * 12 }}>
      <div className="comment-item__header">
        <div className="comment-item__author">{comment.author.name}</div>
        <div className="comment-item__meta">
          <span className="comment-item__timestamp">{formatDate(comment.createdAt)}</span>
          {comment.resolved && <span className="comment-item__status">Resolved</span>}
        </div>
      </div>
      <div className="comment-item__body">{comment.content}</div>
      <div className="comment-item__actions">
        <button onClick={() => setReplying((v) => !v)}>Reply</button>
        {onResolve && (
          <button onClick={() => onResolve(comment.id, !comment.resolved)}>
            {comment.resolved ? "Reopen" : "Mark resolved"}
          </button>
        )}
      </div>
      {isReplying && (
        <CommentForm
          onSubmit={handleReply}
          placeholder="Reply to this comment"
          submitLabel="Reply"
        />
      )}
      {comment.replies && comment.replies.length > 0 && (
        <ul className="comment-thread">
          {comment.replies.map((reply) => (
            <CommentItem
              key={reply.id}
              comment={reply}
              onReply={onReply}
              onResolve={onResolve}
              depth={depth + 1}
            />
          ))}
        </ul>
      )}
    </li>
  );
};

export const CommentsList: React.FC<CommentsListProps> = ({ comments, onReply, onResolve }) => {
  const sorted = useMemo(
    () =>
      [...comments].sort(
        (a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      ),
    [comments]
  );

  return (
    <ul className="comments-list">
      {sorted.map((comment) => (
        <CommentItem key={comment.id} comment={comment} onReply={onReply} onResolve={onResolve} />
      ))}
    </ul>
  );
};
