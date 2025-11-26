import { useCallback, useEffect, useState } from "react";
import { InlineSelection } from "../types/comments";

interface UseInlineSelectionOptions {
  /** Selector that wraps the page content. */
  contentContainerSelector?: string;
  /** Called when a selection is captured. */
  onSelection?: (selection: InlineSelection) => void;
}

interface UseInlineSelectionResult {
  selection: InlineSelection | null;
  captureSelection: () => void;
  clearSelection: () => void;
}

/**
 * Captures the current browser text selection and converts it into a best-effort
 * InlineSelection shape that can be persisted with an inline comment.
 */
export function useInlineSelection({
  contentContainerSelector,
  onSelection,
}: UseInlineSelectionOptions = {}): UseInlineSelectionResult {
  const [selection, setSelection] = useState<InlineSelection | null>(null);

  const captureSelection = useCallback(() => {
    const sel = window.getSelection();
    if (!sel || sel.rangeCount === 0) return;
    const range = sel.getRangeAt(0);
    const container = contentContainerSelector
      ? document.querySelector(contentContainerSelector)
      : range.commonAncestorContainer?.parentElement;

    if (container && !container.contains(range.commonAncestorContainer)) {
      return;
    }

    const blockElement = range.startContainer instanceof Element
      ? range.startContainer.closest("[data-block-id]")
      : range.startContainer.parentElement?.closest("[data-block-id]");

    const blockId = blockElement?.getAttribute("data-block-id") || undefined;
    const text = range.toString();

    const nextSelection: InlineSelection = {
      blockId,
      startOffset: range.startOffset,
      endOffset: range.endOffset,
      textPreview: text.slice(0, 120),
    };

    setSelection(nextSelection);
    onSelection?.(nextSelection);
  }, [contentContainerSelector, onSelection]);

  const clearSelection = useCallback(() => setSelection(null), []);

  useEffect(() => {
    const handler = () => captureSelection();
    document.addEventListener("selectionchange", handler);
    return () => document.removeEventListener("selectionchange", handler);
  }, [captureSelection]);

  return { selection, captureSelection, clearSelection };
}
