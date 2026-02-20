"use client"

import { useState, useEffect } from "react"
import DashboardLayout from "@/components/dashboard-layout"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { IconPlus, IconSearch, IconSpeakerphone } from "@tabler/icons-react"
import { Loader2 } from "lucide-react"
import Link from "next/link"
import { useAuth } from "@/lib/auth/auth-context"
import { listCampaigns, type Campaign } from "@/lib/api/campaigns"

// Mock campaigns for demo
const MOCK_CAMPAIGNS: Campaign[] = [
  {
    campaign_id: "1",
    user_id: "demo",
    campaign_name: "Q1 Enterprise Outreach",
    description: "Targeting VP-level decision makers at mid-market SaaS companies",
    agent_ids: ["a1", "a2", "a3"],
    status: "active",
    created_at: Date.now(),
    updated_at: Date.now(),
    metrics: { total_agents: 3, total_calls: 487, avg_conversion_rate: 0.24 },
  },
  {
    campaign_id: "2",
    user_id: "demo",
    campaign_name: "SMB Quick Pitch",
    description: "Short, direct scripts for small business owners",
    agent_ids: ["a4", "a5"],
    status: "active",
    created_at: Date.now(),
    updated_at: Date.now(),
    metrics: { total_agents: 2, total_calls: 312, avg_conversion_rate: 0.19 },
  },
  {
    campaign_id: "3",
    user_id: "demo",
    campaign_name: "Referral Follow-up",
    description: "Warm outreach scripts for referral-based leads",
    agent_ids: ["a6"],
    status: "paused",
    created_at: Date.now(),
    updated_at: Date.now(),
    metrics: { total_agents: 1, total_calls: 89, avg_conversion_rate: 0.35 },
  },
]

export default function CampaignsPage() {
  const { user } = useAuth()
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [searchQuery, setSearchQuery] = useState("")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        setIsLoading(true)
        const data = await listCampaigns()
        setCampaigns(data)
      } catch {
        // Fall back to mock data for demo
        setCampaigns(MOCK_CAMPAIGNS)
      } finally {
        setIsLoading(false)
      }
    }

    if (user) {
      fetchCampaigns()
    }
  }, [user])

  const filteredCampaigns = campaigns.filter((c) =>
    c.campaign_name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-500/10 text-green-400 border-green-500/20"
      case "paused":
        return "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
      case "completed":
        return "bg-neutral-500/10 text-gray-500 border-neutral-500/20"
      default:
        return "bg-neutral-500/10 text-gray-500 border-neutral-500/20"
    }
  }

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-full">
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="h-8 w-8 animate-spin text-accent" />
            <p className="text-gray-500">Loading campaigns...</p>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  if (campaigns.length === 0) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center h-full p-8">
          <div className="flex flex-col items-center max-w-md text-center space-y-4">
            <div className="h-24 w-24 rounded-2xl bg-blue-50/50 border-2 border-dashed border-blue-200 flex items-center justify-center">
              <IconSpeakerphone className="h-12 w-12 text-gray-500" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">No campaigns yet</h2>
            <p className="text-gray-500">
              Group your outreach agents into campaigns to compare script performance side by side.
            </p>
            <Link href="/dashboard/agents/create">
              <Button className="bg-accent hover:bg-accent/90 text-white shadow-lg shadow-accent/20">
                <IconPlus className="h-4 w-4 mr-2" />
                Create Your First Agent
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
                <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
                <p className="text-gray-500 mt-1">
                  Group and compare your outreach scripts by campaign.
                </p>
              </div>
              <Link href="/dashboard/agents/create">
                <Button className="bg-accent hover:bg-accent/90 text-white shadow-lg shadow-accent/20">
                  <IconPlus className="h-4 w-4 mr-2" />
                  Create Outreach Agent
                </Button>
              </Link>
            </div>

            <div className="mt-6 relative">
              <IconSearch className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <Input
                placeholder="Search campaigns..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-blue-50/50 border-blue-200/50 text-gray-900 placeholder:text-gray-400 focus:border-accent/50"
              />
            </div>
          </div>
        </div>

        {/* Campaigns Grid */}
        <div className="flex-1 overflow-auto p-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCampaigns.map((campaign) => (
              <Link
                key={campaign.campaign_id}
                href={`/dashboard/agents?campaign=${encodeURIComponent(campaign.campaign_name)}`}
              >
                <Card className="bg-blue-50/50 border-blue-200/50 p-6 hover:border-accent/50 hover:shadow-lg hover:shadow-accent/10 transition-all cursor-pointer h-full">
                  <div className="flex items-start gap-4">
                    <div className="h-12 w-12 rounded-xl bg-blue-100/50 flex items-center justify-center shrink-0">
                      <IconSpeakerphone className="h-6 w-6 text-accent" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900 truncate">{campaign.campaign_name}</h3>
                        <Badge variant="secondary" className={getStatusColor(campaign.status)}>
                          {campaign.status.toUpperCase()}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-500 line-clamp-2 mb-4">{campaign.description}</p>

                      {/* Metrics */}
                      <div className="flex items-center gap-4 text-xs text-gray-400">
                        <span>{campaign.metrics?.total_agents ?? 0} agents</span>
                        <span>{campaign.metrics?.total_calls ?? 0} calls</span>
                        <span className="text-green-400">
                          {campaign.metrics?.avg_conversion_rate
                            ? `${(campaign.metrics.avg_conversion_rate * 100).toFixed(1)}% conv.`
                            : "--"}
                        </span>
                      </div>
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
