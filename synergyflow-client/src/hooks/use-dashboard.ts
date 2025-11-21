import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export interface DashboardData {
  objectives: {
    total: number;
    averageProgress: number;
    byProgress: {
      high: number;
      medium: number;
      low: number;
    };
    list: Array<{
      id: string;
      title: string;
      progress: number;
      ownerId: string | null;
      createdAt: string;
    }>;
  };
  tasks: {
    total: number;
    todo: number;
    inProgress: number;
    done: number;
    overdue: number;
    completionRate: number;
  };
  members: Array<{
    userId: string;
    user: {
      id: string;
      email: string;
      name: string | null;
      avatarUrl: string | null;
    };
    totalTasks: number;
    completedTasks: number;
    completionRate: number;
  }>;
  recentActivity: Array<{
    id: string;
    title: string;
    status: string;
    createdAt: string;
  }>;
  strategyNodes: {
    total: number;
    withTasks: number;
  };
}

export function useDashboard(workspaceId: string) {
  return useQuery({
    queryKey: ['dashboard', workspaceId],
    queryFn: async () => {
      return apiClient.get<DashboardData>(`/workspaces/${workspaceId}/dashboard`);
    },
    enabled: !!workspaceId,
    refetchInterval: 30000, // 30秒ごとに自動更新
  });
}

