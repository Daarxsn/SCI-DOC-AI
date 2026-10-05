import type { InputHTMLAttributes } from "react";

type TextFieldProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  hint?: string;
};

export function TextField({ label, hint, id, className = "", ...props }: TextFieldProps) {
  const inputId = id ?? label.toLowerCase().replace(/[^a-z0-9]+/g, "-");

  return (
    <label className={["ui-field", className].filter(Boolean).join(" ")} htmlFor={inputId}>
      <span className="ui-field__label">{label}</span>
      <input className="ui-input" id={inputId} {...props} />
      {hint ? <span className="ui-field__hint">{hint}</span> : null}
    </label>
  );
}
