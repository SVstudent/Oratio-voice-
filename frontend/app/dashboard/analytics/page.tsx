"use client"

import { useState, useEffect } from "react"
import DashboardLayout from "@/components/dashboard-layout"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2 } from "lucide-react"
import { useAuth } from "@/lib/auth/auth-context"
import { getAnalyticsOverview, MOCK_ANALYTICS, type AnalyticsOverview } from "@/lib/api/analytics"
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts"

export default function AnalyticsPage() {
  const { user } = useAuth()
  const [data, setData] = useState<AnalyticsOverview | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setIsLoading(true)
        const result = await getAnalyticsOverview()
        setData(result)
      } catch {
        // Fall back to mock data for demo
        setData(MOCK_ANALYTICS)
      } finally {
        setIsLoading(false)
      }
    }

    if (user) {
      fetchAnalytics()
    }
  }, [user])

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-full">
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="h-8 w-8 animate-spin text-accent" />
            <p className="text-gray-500">Loading analytics...</p>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  const analytics = data || MOCK_ANALYTICS
  const sentimentColors = ["#22c55e", "#3b82f6", "#ef4444"]

  return (
    <DashboardLayout>
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="border-b border-blue-200/50 bg-blue-50/30 backdrop-blur-sm">
          <div className="p-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
                <p className="text-gray-500 mt-1">
                  Track outreach performance across all your agents and campaigns.
                </p>
              </div>
              <Badge variant="secondary" className="text-xs bg-purple-500/10 text-purple-400 border-purple-500/20">
                Powered by Datadog
              </Badge>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-8">
          <div className="max-w-7xl mx-auto space-y-8">
            {/* KPI Summary */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card className="bg-blue-50/50 border-blue-200/50 p-6">
                <p className="text-xs text-gray-500 mb-1">Total Calls</p>
                <p className="text-3xl font-bold text-gray-900">{analytics.total_calls.toLocaleString()}</p>
              </Card>
              <Card className="bg-blue-50/50 border-blue-200/50 p-6">
                <p className="text-xs text-gray-500 mb-1">Avg Duration</p>
                <p className="text-3xl font-bold text-gray-900">{analytics.avg_duration_seconds}s</p>
              </Card>
              <Card className="bg-blue-50/50 border-blue-200/50 p-6">
                <p className="text-xs text-gray-500 mb-1">Conversion Rate</p>
                <p className="text-3xl font-bold text-green-400">
                  {(analytics.avg_conversion_rate * 100).toFixed(1)}%
                </p>
              </Card>
              <Card className="bg-blue-50/50 border-blue-200/50 p-6">
                <p className="text-xs text-gray-500 mb-1">Active Agents</p>
                <p className="text-3xl font-bold text-accent">{analytics.total_agents}</p>
              </Card>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Calls Trend */}
              <Card className="bg-blue-50/50 border-blue-200/50 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Calls This Week</h3>
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={analytics.calls_trend}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
                    <YAxis stroke="#94a3b8" fontSize={12} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px" }}
                      labelStyle={{ color: "#1e293b" }}
                    />
                    <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Calls" />
                  </BarChart>
                </ResponsiveContainer>
              </Card>

              {/* Conversion Trend */}
              <Card className="bg-blue-50/50 border-blue-200/50 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Conversion Rate Trend</h3>
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={analytics.conversion_trend}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
                    <YAxis
                      stroke="#94a3b8"
                      fontSize={12}
                      tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                    />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px" }}
                      labelStyle={{ color: "#1e293b" }}
                      formatter={(value: number) => [`${(value * 100).toFixed(1)}%`, "Conversion"]}
                    />
                    <Line
                      type="monotone"
                      dataKey="rate"
                      stroke="#22c55e"
                      strokeWidth={2}
                      dot={{ fill: "#22c55e", r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Card>
            </div>

            {/* Bottom Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Top Performing Scripts */}
              <Card className="bg-blue-50/50 border-blue-200/50 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Performing Scripts</h3>
                <div className="space-y-4">
                  {analytics.top_performing_agents.map((agent, idx) => (
                    <div key={agent.agent_id} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="text-sm font-bold text-gray-400 w-6">#{idx + 1}</span>
                        <span className="text-sm text-gray-900">{agent.agent_name}</span>
                      </div>
                      <Badge
                        variant="secondary"
                        className={
                          idx === 0
                            ? "bg-green-500/10 text-green-400 border-green-500/20"
                            : "bg-neutral-500/10 text-gray-500 border-neutral-500/20"
                        }
                      >
                        {(agent.conversion_rate * 100).toFixed(1)}%
                      </Badge>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Sentiment Distribution */}
              <Card className="bg-blue-50/50 border-blue-200/50 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Sentiment Distribution</h3>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie
                      data={analytics.sentiment_distribution}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={85}
                      dataKey="value"
                      label={({ label, value }) => `${label} ${value}%`}
                    >
                      {analytics.sentiment_distribution.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={sentimentColors[index % sentimentColors.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px" }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
