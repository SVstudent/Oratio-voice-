import { get, post, del } from './client';

export interface Campaign {
  campaign_id: string;
  user_id: string;
  campaign_name: string;
  description: string;
  agent_ids: string[];
  status: 'active' | 'paused' | 'completed';
  created_at: number;
  updated_at: number;
  metrics?: {
    total_agents: number;
    total_calls: number;
    avg_conversion_rate: number;
  };
}

export interface CreateCampaignData {
  campaign_name: string;
  description: string;
}

export async function listCampaigns(): Promise<Campaign[]> {
  return get<Campaign[]>('/api/v1/campaigns');
}

export async function getCampaign(campaignId: string): Promise<Campaign> {
  return get<Campaign>(`/api/v1/campaigns/${campaignId}`);
}

export async function createCampaign(data: CreateCampaignData): Promise<Campaign> {
  return post<Campaign>('/api/v1/campaigns', data);
}

export async function deleteCampaign(campaignId: string): Promise<{ message: string }> {
  return del<{ message: string }>(`/api/v1/campaigns/${campaignId}`);
}
