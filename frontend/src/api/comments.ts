import { Comment, CreateCommentPayload, UpdateCommentPayload } from "../types/comments";

const API_PREFIX = "/api/v1";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchComments(pageId: string): Promise<Comment[]> {
  const response = await fetch(`${API_PREFIX}/comments?page_id=${encodeURIComponent(pageId)}`);
  return handleResponse<Comment[]>(response);
}

export async function createComment(payload: CreateCommentPayload): Promise<Comment> {
  const response = await fetch(`${API_PREFIX}/comments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<Comment>(response);
}

export async function updateComment(
  commentId: string,
  payload: UpdateCommentPayload
): Promise<Comment> {
  const response = await fetch(`${API_PREFIX}/comments/${commentId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<Comment>(response);
}

export async function resolveComment(commentId: string, resolved = true): Promise<Comment> {
  return updateComment(commentId, { resolved });
}
