import { get } from './client';

export interface AnalyticsOverview {
  total_calls: number;
  avg_duration_seconds: number;
  avg_conversion_rate: number;
  total_agents: number;
  calls_trend: { date: string; count: number }[];
  conversion_trend: { date: string; rate: number }[];
  top_performing_agents: { agent_id: string; agent_name: string; conversion_rate: number }[];
  sentiment_distribution: { label: string; value: number }[];
}

export async function getAnalyticsOverview(): Promise<AnalyticsOverview> {
  return get<AnalyticsOverview>('/api/v1/analytics/overview');
}

// Mock data for demo/development when backend is not ready
export const MOCK_ANALYTICS: AnalyticsOverview = {
  total_calls: 1247,
  avg_duration_seconds: 94,
  avg_conversion_rate: 0.23,
  total_agents: 8,
  calls_trend: [
    { date: "Mon", count: 145 },
    { date: "Tue", count: 198 },
    { date: "Wed", count: 176 },
    { date: "Thu", count: 221 },
    { date: "Fri", count: 189 },
    { date: "Sat", count: 134 },
    { date: "Sun", count: 184 },
  ],
  conversion_trend: [
    { date: "Mon", rate: 0.18 },
    { date: "Tue", rate: 0.22 },
    { date: "Wed", rate: 0.19 },
    { date: "Thu", rate: 0.28 },
    { date: "Fri", rate: 0.25 },
    { date: "Sat", rate: 0.21 },
    { date: "Sun", rate: 0.24 },
  ],
  top_performing_agents: [
    { agent_id: "1", agent_name: "Q1 Enterprise Opener", conversion_rate: 0.31 },
    { agent_id: "2", agent_name: "Value-First Script", conversion_rate: 0.27 },
    { agent_id: "3", agent_name: "Pain Point Approach", conversion_rate: 0.24 },
    { agent_id: "4", agent_name: "Referral Ask Script", conversion_rate: 0.19 },
  ],
  sentiment_distribution: [
    { label: "Positive", value: 45 },
    { label: "Neutral", value: 35 },
    { label: "Negative", value: 20 },
  ],
};
