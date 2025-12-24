export interface CommentAuthor {
  id: string;
  name: string;
}

export interface InlineSelection {
  /**
   * Best-effort representation of the selected text. Includes the block or element id and optional
   * character offsets to roughly map back to the original selection.
   */
  blockId?: string;
  startOffset?: number;
  endOffset?: number;
  textPreview?: string;
}

export interface Comment {
  id: string;
  pageId: string;
  parentId?: string | null;
  content: string;
  createdAt: string;
  resolved: boolean;
  author: CommentAuthor;
  selection?: InlineSelection;
  replies?: Comment[];
}

export interface CreateCommentPayload {
  pageId: string;
  content: string;
  parentId?: string;
  selection?: InlineSelection;
}

export interface UpdateCommentPayload {
  resolved?: boolean;
}
