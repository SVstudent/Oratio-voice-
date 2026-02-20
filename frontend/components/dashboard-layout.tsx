"use client"
import type React from "react"
import { IconRobot, IconDatabase, IconKey, IconLogout, IconSpeakerphone, IconChartBar } from "@tabler/icons-react"
import { cn } from "@/lib/utils"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { MicSparklesIcon } from "@/components/ui/mic-sparkles-icon"
import { useAuth } from "@/lib/auth/auth-context"
import dynamic from "next/dynamic"

const CopilotSidebarSafe = dynamic(
  () => import("@copilotkit/react-ui").then((mod) => mod.CopilotSidebar),
  { ssr: false }
)

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const { logout } = useAuth()
  
  const links = [
    {
      label: "Outreach Agents",
      href: "/dashboard/agents",
      icon: IconRobot,
    },
    {
      label: "Campaigns",
      href: "/dashboard/campaigns",
      icon: IconSpeakerphone,
    },
    {
      label: "Analytics",
      href: "/dashboard/analytics",
      icon: IconChartBar,
    },
    {
      label: "Knowledge Base",
      href: "/dashboard/knowledge-base",
      icon: IconDatabase,
    },
    {
      label: "API Keys",
      href: "/dashboard/api-keys",
      icon: IconKey,
    },
    {
      label: "Logout",
      href: "#",
      icon: IconLogout,
      action: logout,
    },
  ]

  const isActive = (href: string) => {
    if (href === "/dashboard/agents") {
      return pathname.startsWith("/dashboard/agents")
    }
    if (href === "/dashboard/campaigns") {
      return pathname.startsWith("/dashboard/campaigns")
    }
    if (href === "/dashboard/analytics") {
      return pathname.startsWith("/dashboard/analytics")
    }
    return pathname === href
  }

  return (
    <div className="flex w-full h-screen overflow-hidden bg-white">
      {/* Compact Sidebar */}
      <aside className="w-16 bg-blue-50/50 border-r border-blue-200/50 flex flex-col items-center py-6 gap-6 shrink-0 relative z-10">
        {/* Logo */}
        <Link href="/dashboard/agents" className="group">
          <div className="h-10 w-10 shrink-0 rounded-xl bg-accent flex items-center justify-center relative transition-transform hover:scale-105">
            <MicSparklesIcon size={40} className="text-white" />
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="flex flex-col gap-3 flex-1">
          {links.map((link, idx) => {
            const Icon = link.icon
            const active = isActive(link.href)
            
            if (link.action) {
              // For logout button
              return (
                <button
                  key={idx}
                  onClick={link.action}
                  className={cn(
                    "h-10 w-10 rounded-xl flex items-center justify-center transition-all group relative",
                    "text-gray-500 hover:text-blue-600 hover:bg-blue-100/50"
                  )}
                  title={link.label}
                >
                  <Icon className="h-5 w-5 shrink-0" />
                  {/* Tooltip */}
                  <span className="absolute left-14 px-2 py-1 bg-blue-100 text-gray-900 text-xs rounded-md whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity">
                    {link.label}
                  </span>
                </button>
              )
            }
            
            return (
              <Link
                key={idx}
                href={link.href}
                className={cn(
                  "h-10 w-10 rounded-xl flex items-center justify-center transition-all group relative",
                  active
                    ? "bg-accent text-white"
                    : "text-gray-500 hover:text-blue-600 hover:bg-blue-100/50"
                )}
                title={link.label}
              >
                <Icon className="h-5 w-5 shrink-0" />
                {/* Tooltip */}
                <span className="absolute left-14 px-2 py-1 bg-blue-100 text-gray-900 text-xs rounded-md whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity">
                  {link.label}
                </span>
              </Link>
            )
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex flex-1 overflow-auto relative z-0">
        <div className="flex h-full w-full flex-1 flex-col bg-white">{children}</div>
      </main>

      {/* CopilotKit AI Sidebar — only renders when CopilotKit is configured */}
      {process.env.NEXT_PUBLIC_COPILOTKIT_API_KEY && (
        <CopilotSidebarSafe
          defaultOpen={false}
          labels={{
            title: "Script Copilot",
            initial: "I can help you optimize your cold outreach scripts. Try asking me to:\n\n- Review a script and suggest improvements\n- Write objection handling for pricing concerns\n- Create a new opener for a specific audience\n- Analyze what makes a script convert better",
          }}
          className="z-50"
        />
      )}
    </div>
  )
}

