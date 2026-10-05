import type { HTMLAttributes, PropsWithChildren } from "react";

type CardProps = PropsWithChildren<HTMLAttributes<HTMLDivElement>> & {
  interactive?: boolean;
};

export function Card({ children, interactive = false, className = "", ...props }: CardProps) {
  return (
    <div
      className={["ui-card", interactive ? "ui-card--interactive" : "", className]
        .filter(Boolean)
        .join(" ")}
      {...props}
    >
      {children}
    </div>
  );
}
