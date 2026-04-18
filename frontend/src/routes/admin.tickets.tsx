import { createFileRoute, Link } from "@tanstack/react-router";
import { AppShell } from "@/components/AppShell";
import { StatusBadge, PriorityBadge } from "@/components/StatusBadge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useEffect, useState, useMemo } from "react";
import { fetchApi } from "@/lib/api";
import { Search, Download, Filter as FilterIcon, MoreVertical, Settings2 } from "lucide-react";

export const Route = createFileRoute("/admin/tickets")({
  head: () => ({
    meta: [
      { title: "All Tickets — AutoIT.Bot Admin" },
      { name: "description", content: "Manage, assign, and track all IT support requests across the organization." },
    ],
  }),
  component: AllTickets,
});

function AllTickets() {
  const [user, setUser] = useState({ name: "Loading...", subtitle: "Loading..." });
  const [allTickets, setAllTickets] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [priorityFilter, setPriorityFilter] = useState("all");
  const [categoryFilter, setCategoryFilter] = useState("all");

  useEffect(() => {
    fetchApi("/auth/me").then(u => {
      if (u.role === "User") {
        window.location.replace("/dashboard");
      } else {
        setUser({ name: u.name, subtitle: u.title || "Admin" });
      }
    }).catch(() => {});
    fetchApi("/tickets/all").then(res => setAllTickets(res.tickets)).catch(() => {});
  }, []);

  const filteredTickets = useMemo(() => {
    return allTickets.filter(t => {
      const matchSearch = !searchQuery || t.id.toLowerCase().includes(searchQuery.toLowerCase()) || t.subject.toLowerCase().includes(searchQuery.toLowerCase()) || t.category.toLowerCase().includes(searchQuery.toLowerCase());
      const matchStatus = statusFilter === "all" || t.status === statusFilter;
      const matchPriority = priorityFilter === "all" || t.priority.includes(priorityFilter);
      const matchCategory = categoryFilter === "all" || t.category === categoryFilter;
      return matchSearch && matchStatus && matchPriority && matchCategory;
    });
  }, [allTickets, searchQuery, statusFilter, priorityFilter, categoryFilter]);

  return (
    <AppShell variant="admin" user={user}>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Ticket Management</h1>
          <p className="text-sm text-muted-foreground">
            Manage, assign, and track all IT support requests across the organization.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input 
              placeholder="Search tickets, requesters..." 
              className="h-10 w-72 rounded-xl pl-9" 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <Button variant="outline" className="rounded-xl">
            <Download className="mr-1 h-4 w-4" /> Export CSV
          </Button>
        </div>
      </div>

      <section className="rounded-2xl border border-border/60 bg-card shadow-soft">
        <div className="flex flex-wrap items-center gap-2 border-b border-border/60 p-4">
          <span className="inline-flex items-center gap-1 rounded-lg bg-muted/60 px-3 py-1.5 text-xs font-medium">
            <FilterIcon className="h-3.5 w-3.5" /> Filters:
          </span>
          <Filter label="Status" value={statusFilter} onChange={setStatusFilter} options={["Open", "In Progress", "Pending User", "Pending Approval", "Resolved"]} />
          <Filter label="Priority" value={priorityFilter} onChange={setPriorityFilter} options={["CRITICAL", "HIGH", "MEDIUM", "LOW"]} />
          <Filter label="Category" value={categoryFilter} onChange={setCategoryFilter} options={["Hardware", "Software", "Network", "Access", "Infrastructure", "Escalated"]} />
          <button onClick={() => { setSearchQuery(""); setStatusFilter("all"); setPriorityFilter("all"); setCategoryFilter("all"); }} className="ml-auto text-xs font-medium text-muted-foreground hover:text-foreground">
            Clear All
          </button>
        </div>

        <div className="flex items-center gap-2 border-b border-border/60 px-4 py-2 text-xs text-muted-foreground">
          <span>Showing 1-{filteredTickets.length} of {filteredTickets.length}</span>
          <Button variant="outline" size="sm" className="ml-auto h-7 rounded-lg">‹</Button>
          <Button variant="outline" size="sm" className="h-7 rounded-lg">›</Button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-muted/40 text-left text-xs uppercase tracking-wider text-muted-foreground">
                <th className="px-5 py-3"><Checkbox /></th>
                <th className="px-5 py-3 font-medium">Ticket ID</th>
                <th className="px-5 py-3 font-medium">Subject & Requester</th>
                <th className="px-5 py-3 font-medium">Status</th>
                <th className="px-5 py-3 font-medium">Priority</th>
                <th className="px-5 py-3 font-medium">Assignee</th>
                <th className="px-5 py-3 font-medium">SLA</th>
                <th className="px-5 py-3"><Settings2 className="h-4 w-4" /></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60">
              {filteredTickets.map((t) => (
                <tr key={t.id} className="transition hover:bg-muted/30">
                  <td className="px-5 py-4"><Checkbox /></td>
                  <td className="px-5 py-4 font-mono text-xs font-medium">
                    <Link to="/tickets/$ticketId" params={{ ticketId: t.id }} className="hover:text-brand-700">
                      #{t.id}
                    </Link>
                  </td>
                  <td className="px-5 py-4">
                    <div className="font-medium">{t.subject}</div>
                    <div className="mt-0.5 flex items-center gap-1.5 text-xs text-muted-foreground">
                      <Avatar className="h-4 w-4">
                        <AvatarFallback className="bg-gradient-brand text-[8px] text-primary-foreground">
                          {t.user_id ? t.user_id.slice(-2) : "U"}
                        </AvatarFallback>
                      </Avatar>
                      {t.user_id}
                    </div>
                  </td>
                  <td className="px-5 py-4"><StatusBadge status={t.status} /></td>
                  <td className="px-5 py-4"><PriorityBadge priority={t.priority} /></td>
                  <td className="px-5 py-4">
                    {t.assignee ? (
                      <div className="flex items-center gap-1.5 text-xs">
                        <Avatar className="h-5 w-5">
                          <AvatarFallback className="bg-gradient-brand text-[8px] text-primary-foreground">
                            {t.assignee.name?.split(" ").map((n: string) => n[0]).join("") || "B"}
                          </AvatarFallback>
                        </Avatar>
                        {t.assignee.name?.split(" ")[0] || "Auto"}
                      </div>
                    ) : (
                      <span className="text-xs text-muted-foreground line-through">Unassigned</span>
                    )}
                  </td>
                  <td className="px-5 py-4">
                    <SlaCell ticket={t} />
                  </td>
                  <td className="px-5 py-4">
                    <Button variant="ghost" size="icon" className="h-7 w-7">
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </AppShell>
  );
}

function Filter({ label, value, onChange, options }: { label: string, value: string, onChange: (v: string) => void, options: string[] }) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="h-8 w-auto gap-1 rounded-lg bg-card text-xs">
        <SelectValue placeholder={label} />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="all">All {label}</SelectItem>
        {options.map(opt => <SelectItem key={opt} value={opt}>{opt}</SelectItem>)}
      </SelectContent>
    </Select>
  );
}

function SlaCell({ ticket }: { ticket: (typeof tickets)[number] }) {
  if (ticket.status === "Resolved") {
    return <span className="text-xs font-medium text-status-resolved-foreground">Met (2m)</span>;
  }
  const remaining = ticket.sla_remaining_min ?? 135;
  const target = ticket.sla_target_min ?? 480;
  const pct = Math.max(0, Math.min(100, (remaining / target) * 100));
  const critical = pct < 25;
  const label = remaining < 60 ? `${remaining}m remaining` : `${Math.floor(remaining / 60)}h ${remaining % 60}m`;
  return (
    <div className="space-y-1">
      <div className={`text-xs font-medium ${critical ? "text-status-critical-foreground" : "text-foreground"}`}>
        {critical && "● "}{label}
      </div>
      <div className="h-1 w-24 overflow-hidden rounded-full bg-muted">
        <div
          className={`h-full ${critical ? "bg-status-critical-foreground" : "bg-brand-700"}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
