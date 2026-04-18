import { cn } from "@/lib/utils";
import type { TicketStatus, TicketPriority } from "@/lib/types";

const statusStyles: Record<TicketStatus, string> = {
  Open: "bg-status-open text-status-open-foreground",
  "In Progress": "bg-status-progress text-status-progress-foreground",
  "Pending User": "bg-status-warning text-status-warning-foreground",
  "Pending Approval": "bg-status-warning text-status-warning-foreground",
  Resolved: "bg-status-resolved text-status-resolved-foreground",
  "On Hold": "bg-muted text-muted-foreground",
};

const priorityStyles: Record<TicketPriority, string> = {
  Critical: "bg-status-critical text-status-critical-foreground",
  High: "bg-status-warning text-status-warning-foreground",
  Normal: "bg-status-progress text-status-progress-foreground",
  Medium: "bg-status-progress text-status-progress-foreground",
  Low: "bg-muted text-muted-foreground",
};

export function StatusBadge({ status, className }: { status: TicketStatus; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium",
        statusStyles[status],
        className,
      )}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current opacity-70" />
      {status}
    </span>
  );
}

export function PriorityBadge({
  priority,
  className,
}: {
  priority: TicketPriority;
  className?: string;
}) {
  const dot = priority === "Critical" ? "▲" : priority === "High" ? "↑" : priority === "Low" ? "↓" : "—";
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium",
        priorityStyles[priority],
        className,
      )}
    >
      <span className="text-[10px]">{dot}</span>
      {priority}
    </span>
  );
}
