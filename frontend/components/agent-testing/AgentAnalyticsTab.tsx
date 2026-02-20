"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { Agent } from "@/lib/api/agents"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts"

const mockCallHistory = [
  { date: "Mon", calls: 12, conversions: 3 },
  { date: "Tue", calls: 19, conversions: 5 },
  { date: "Wed", calls: 15, conversions: 4 },
  { date: "Thu", calls: 22, conversions: 7 },
  { date: "Fri", calls: 18, conversions: 5 },
  { date: "Sat", calls: 9, conversions: 2 },
  { date: "Sun", calls: 14, conversions: 4 },
]

const mockSentiment = [
  { name: "Positive", value: 45, color: "#22c55e" },
  { name: "Neutral", value: 35, color: "#3b82f6" },
  { name: "Negative", value: 20, color: "#ef4444" },
]

interface AgentAnalyticsTabProps {
  agent: Agent
}

export default function AgentAnalyticsTab({ agent }: AgentAnalyticsTabProps) {
  const metrics = agent.metrics

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="bg-blue-50 border-blue-200 p-4">
          <p className="text-xs text-gray-500">Total Calls</p>
          <p className="text-2xl font-bold text-gray-900">{metrics?.total_calls ?? 109}</p>
        </Card>
        <Card className="bg-blue-50 border-blue-200 p-4">
          <p className="text-xs text-gray-500">Avg Duration</p>
          <p className="text-2xl font-bold text-gray-900">
            {metrics?.avg_duration_seconds ? `${Math.round(metrics.avg_duration_seconds)}s` : "87s"}
          </p>
        </Card>
        <Card className="bg-blue-50 border-blue-200 p-4">
          <p className="text-xs text-gray-500">Conversion Rate</p>
          <p className="text-2xl font-bold text-green-400">
            {metrics?.conversion_rate ? `${(metrics.conversion_rate * 100).toFixed(1)}%` : "27.5%"}
          </p>
        </Card>
        <Card className="bg-blue-50 border-blue-200 p-4">
          <p className="text-xs text-gray-500">Sentiment Score</p>
          <p className="text-2xl font-bold text-blue-400">
            {metrics?.sentiment_score ? `${(metrics.sentiment_score * 100).toFixed(0)}%` : "72%"}
          </p>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Call History */}
        <Card className="bg-blue-50 border-blue-200 p-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-4">Call History</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={mockCallHistory}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip
                contentStyle={{ backgroundColor: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px" }}
                labelStyle={{ color: "#1e293b" }}
              />
              <Bar dataKey="calls" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Calls" />
              <Bar dataKey="conversions" fill="#22c55e" radius={[4, 4, 0, 0]} name="Conversions" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Sentiment Distribution */}
        <Card className="bg-blue-50 border-blue-200 p-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-4">Sentiment Distribution</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={mockSentiment}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={80}
                dataKey="value"
                label={({ name, value }) => `${name} ${value}%`}
              >
                {mockSentiment.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px" }}
              />
            </PieChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Powered by Datadog */}
      <div className="flex items-center justify-center pt-2">
        <Badge variant="secondary" className="text-xs bg-purple-500/10 text-purple-400 border-purple-500/20">
          Powered by Datadog
        </Badge>
      </div>
    </div>
  )
}
