'use client';

import { IconSettings } from '@tabler/icons-react';
import type { Agent } from '@/lib/api/agents';
import { Card } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

interface AgentConfigCardProps {
  agent: Agent;
}

export function AgentConfigCard({ agent }: AgentConfigCardProps) {
  return (
    <Card className="bg-blue-50 border-blue-200">
      <div className="px-6 py-4">
        <div className="flex items-center gap-2 mb-4">
          <IconSettings className="h-5 w-5 text-accent" />
          <h2 className="text-lg font-semibold text-gray-900">Agent Configuration</h2>
        </div>

        <Separator className="bg-blue-100" />
        <div className="px-0 py-4 space-y-4">
          {/* Standard Operating Procedure */}
          <div>
            <p className="text-sm text-gray-400 mb-2">Standard Operating Procedure</p>
            <div className="text-sm text-gray-900 bg-white border border-blue-200 rounded-lg p-3 whitespace-pre-wrap break-words">
              {agent.sop}
            </div>
          </div>

          <Separator className="bg-blue-100" />

          {/* Knowledge Base Description */}
          <div>
            <p className="text-sm text-gray-400 mb-2">Knowledge Base Description</p>
            <div className="text-sm text-gray-900 bg-white border border-blue-200 rounded-lg p-3 whitespace-pre-wrap break-words">
              {agent.knowledge_base_description}
            </div>
          </div>

          <Separator className="bg-blue-100" />

          {/* Human Handoff Description */}
          <div>
            <p className="text-sm text-gray-400 mb-2">Human Handoff Description</p>
            <div className="text-sm text-gray-900 bg-white border border-blue-200 rounded-lg p-3 whitespace-pre-wrap break-words">
              {agent.human_handoff_description}
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}
