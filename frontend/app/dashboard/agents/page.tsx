"use client"

import DashboardLayout from "@/components/dashboard-layout"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { IconPlus, IconRobot, IconSearch } from "@tabler/icons-react"
import { Input } from "@/components/ui/input"
import Link from "next/link"
import { useState, useEffect } from "react"
import { listAgents, type Agent } from "@/lib/api/agents"
import { useAuth } from "@/lib/auth/auth-context"
import { Loader2 } from "lucide-react"

export default function AgentsPage() {
  const { user } = useAuth()
  const [agents, setAgents] = useState<Agent[]>([])
  const [searchQuery, setSearchQuery] = useState("")
  const [campaignFilter, setCampaignFilter] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        setIsLoading(true)
        setError(null)
        const data = await listAgents()
        setAgents(data)
      } catch (err) {
        console.error("Failed to fetch agents:", err)
        setError("Failed to load agents. Please try again.")
      } finally {
        setIsLoading(false)
      }
    }

    if (user) {
      fetchAgents()
    }
  }, [user])

  const campaigns = [...new Set(agents.map(a => a.campaign_name).filter(Boolean))]

  const filteredAgents = agents.filter((agent) => {
    const matchesSearch = agent.agent_name.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCampaign = !campaignFilter || agent.campaign_name === campaignFilter
    return matchesSearch && matchesCampaign
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-500/10 text-green-400 border-green-500/20"
      case "creating":
        return "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
      case "failed":
        return "bg-red-500/10 text-red-400 border-red-500/20"
      default:
        return "bg-neutral-500/10 text-gray-500 border-neutral-500/20"
    }
  }

  const getModeLabel = (mode: string) => {
    return mode === "voice" ? "Voice" : "Conversational"
  }

  // Loading state
  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-full">
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="h-8 w-8 animate-spin text-accent" />
            <p className="text-gray-500">Loading agents...</p>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  // Error state
  if (error) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-full">
          <div className="flex flex-col items-center gap-4 max-w-md text-center">
            <div className="h-16 w-16 rounded-full bg-red-500/10 flex items-center justify-center">
              <span className="text-2xl">⚠️</span>
            </div>
            <h2 className="text-xl font-semibold text-gray-900">Error Loading Agents</h2>
            <p className="text-gray-500">{error}</p>
            <Button onClick={() => window.location.reload()} className="bg-accent hover:bg-accent/90">
              Retry
            </Button>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  // Empty state
  if (agents.length === 0) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center h-full p-8">
          <div className="flex flex-col items-center max-w-md text-center space-y-4">
            <div className="h-24 w-24 rounded-2xl bg-blue-50/50 border-2 border-dashed border-blue-200 flex items-center justify-center">
              <IconRobot className="h-12 w-12 text-gray-500" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">No outreach agents yet</h2>
            <p className="text-gray-500">
              Create your first outreach agent to start testing cold call scripts with AI.
            </p>
            <Link href="/dashboard/agents/create">
              <Button className="bg-accent hover:bg-accent/90 text-white shadow-lg shadow-accent/20">
                <IconPlus className="h-4 w-4 mr-2" />
                Create Your First Outreach Agent
              </Button>
            </Link>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="border-b border-blue-200/50 bg-blue-50/30 backdrop-blur-sm">
          <div className="p-8">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Outreach Agents</h1>
                <p className="text-gray-500 mt-1">
                  Test and optimize your cold outreach scripts with AI-powered voice agents.
                </p>
              </div>
              <Link href="/dashboard/agents/create">
                <Button className="bg-accent hover:bg-accent/90 text-white shadow-lg shadow-accent/20">
                  <IconPlus className="h-4 w-4 mr-2" />
                  Create Outreach Agent
                </Button>
              </Link>
            </div>

            {/* Search & Filter */}
            <div className="mt-6 flex gap-3">
              <div className="relative flex-1">
                <IconSearch className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                <Input
                  placeholder="Search outreach agents..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 bg-blue-50/50 border-blue-200/50 text-gray-900 placeholder:text-gray-400 focus:border-accent/50"
                />
              </div>
              {campaigns.length > 0 && (
                <select
                  value={campaignFilter}
                  onChange={(e) => setCampaignFilter(e.target.value)}
                  className="bg-blue-50/50 border border-blue-200/50 text-gray-900 rounded-md px-3 py-2 text-sm focus:border-accent/50 outline-none"
                >
                  <option value="">All Campaigns</option>
                  {campaigns.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              )}
            </div>
          </div>
        </div>

        {/* Agents Grid */}
        <div className="flex-1 overflow-auto p-8">
          {filteredAgents.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64">
              <IconSearch className="h-12 w-12 text-gray-500 mb-4" />
              <p className="text-gray-500">No agents found matching "{searchQuery}"</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredAgents.map((agent) => (
                <Card
                  key={agent.agent_id}
                  className="bg-blue-50/50 border-blue-200/50 p-6 hover:border-accent/50 hover:shadow-lg hover:shadow-accent/10 transition-all"
                >
                  <div className="flex items-start gap-4">
                    <div className="h-12 w-12 rounded-xl bg-blue-100/50 flex items-center justify-center shrink-0">
                      <IconRobot className="h-6 w-6 text-accent" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900 truncate">{agent.agent_name}</h3>
                        <Badge variant="secondary" className={getStatusColor(agent.status)}>
                          {agent.status.toUpperCase()}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-500 line-clamp-2 mb-3">
                        {agent.knowledge_base_description || agent.sop || "No description provided"}
                      </p>
                      {/* Outreach Metrics */}
                      <div className="flex items-center gap-4 text-xs text-gray-400 mb-4">
                        <span>{agent.metrics?.total_calls ?? 0} calls</span>
                        <span>{agent.metrics?.avg_duration_seconds ? `${Math.round(agent.metrics.avg_duration_seconds)}s avg` : "--"}</span>
                        <span>{agent.metrics?.conversion_rate ? `${(agent.metrics.conversion_rate * 100).toFixed(1)}%` : "--"}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">
                          {getModeLabel(agent.agent_type)}
                        </span>
                        <Link href={`/dashboard/agents/${agent.agent_id}`}>
                          <Button size="sm" className="bg-blue-100/50 hover:bg-neutral-700 text-gray-900">
                            View Details
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}

              {/* Create New Agent Card */}
              <Link href="/dashboard/agents/create">
                <Card className="bg-blue-50/30 border-2 border-dashed border-blue-200 hover:border-accent/50 hover:bg-blue-50/50 transition-all p-6 h-full flex items-center justify-center cursor-pointer group">
                  <div className="text-center">
                    <div className="h-12 w-12 rounded-xl bg-blue-100/50 group-hover:bg-accent/10 flex items-center justify-center mx-auto mb-3 transition-colors">
                      <IconPlus className="h-6 w-6 text-gray-500 group-hover:text-accent transition-colors" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">Create Outreach Agent</h3>
                    <p className="text-sm text-gray-500">Deploy a new cold outreach script as an AI agent.</p>
                  </div>
                </Card>
              </Link>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  )
}
