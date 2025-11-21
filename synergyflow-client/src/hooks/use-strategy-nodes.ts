import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export interface StrategyNode {
  id: string;
  workspaceId: string;
  objectiveId: string | null;
  title: string;
  description: string | null;
  parentId: string | null;
  order: number;
  createdAt: string;
  updatedAt: string;
  objective?: {
    id: string;
    title: string;
  } | null;
  parent?: {
    id: string;
    title: string;
  } | null;
  children?: Array<{
    id: string;
    title: string;
    order: number;
  }>;
  _count?: {
    tasks: number;
  };
}

export interface CreateStrategyNodeData {
  title: string;
  description?: string;
  objectiveId?: string;
  parentId?: string;
  order?: number;
}

export interface UpdateStrategyNodeData {
  title?: string;
  description?: string;
  objectiveId?: string;
  parentId?: string;
  order?: number;
}

export interface NodeOrder {
  id: string;
  order: number;
  parentId?: string;
}

export function useStrategyNodes(workspaceId: string, objectiveId?: string) {
  return useQuery({
    queryKey: ['strategy-nodes', workspaceId, objectiveId],
    queryFn: async () => {
      const url = objectiveId
        ? `/workspaces/${workspaceId}/strategy-nodes?objectiveId=${objectiveId}`
        : `/workspaces/${workspaceId}/strategy-nodes`;
      return apiClient.get<StrategyNode[]>(url);
    },
    enabled: !!workspaceId,
  });
}

export function useStrategyNode(workspaceId: string, id: string) {
  return useQuery({
    queryKey: ['strategy-node', workspaceId, id],
    queryFn: async () => {
      return apiClient.get<StrategyNode>(`/workspaces/${workspaceId}/strategy-nodes/${id}`);
    },
    enabled: !!workspaceId && !!id,
  });
}

export function useCreateStrategyNode(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateStrategyNodeData) => {
      return apiClient.post<StrategyNode>(
        `/workspaces/${workspaceId}/strategy-nodes`,
        data,
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['strategy-nodes', workspaceId] });
    },
  });
}

export function useUpdateStrategyNode(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: UpdateStrategyNodeData }) => {
      return apiClient.patch<StrategyNode>(
        `/workspaces/${workspaceId}/strategy-nodes/${id}`,
        data,
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['strategy-nodes', workspaceId] });
    },
  });
}

export function useDeleteStrategyNode(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      return apiClient.delete(`/workspaces/${workspaceId}/strategy-nodes/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['strategy-nodes', workspaceId] });
    },
  });
}

export function useReorderStrategyNodes(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (nodes: NodeOrder[]) => {
      return apiClient.post(`/workspaces/${workspaceId}/strategy-nodes/reorder`, { nodes });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['strategy-nodes', workspaceId] });
    },
  });
}

