import type { PropsWithChildren } from "react";

type BadgeTone = "neutral" | "success" | "warning" | "danger" | "info";

type BadgeProps = PropsWithChildren<{
  tone?: BadgeTone;
  className?: string;
}>;

export function Badge({ children, tone = "neutral", className = "" }: BadgeProps) {
  return (
    <span className={["ui-badge", `ui-badge--${tone}`, className].filter(Boolean).join(" ")}>
      {children}
    </span>
  );
}
