import React, { FormEvent, useState } from "react";

interface CommentFormProps {
  initialValue?: string;
  onSubmit: (value: string) => Promise<void> | void;
  placeholder?: string;
  submitLabel?: string;
}

export const CommentForm: React.FC<CommentFormProps> = ({
  initialValue = "",
  onSubmit,
  placeholder = "Add a comment...",
  submitLabel = "Comment",
}) => {
  const [value, setValue] = useState(initialValue);
  const [isSubmitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!value.trim()) return;
    setSubmitting(true);
    try {
      await onSubmit(value.trim());
      setValue("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="comment-form">
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        rows={3}
        disabled={isSubmitting}
        className="comment-form__textarea"
      />
      <div className="comment-form__actions">
        <button type="submit" disabled={isSubmitting || !value.trim()}>
          {isSubmitting ? "Posting..." : submitLabel}
        </button>
      </div>
    </form>
  );
};
