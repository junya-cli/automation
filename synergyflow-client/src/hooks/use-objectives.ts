import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export interface KeyResult {
  name: string;
  current: number;
  target: number;
}

export interface Objective {
  id: string;
  workspaceId: string;
  ownerId: string | null;
  parentId: string | null;
  title: string;
  keyResults: KeyResult[];
  progress: number;
  createdAt: string;
  updatedAt: string;
  owner?: {
    id: string;
    email: string;
    name: string | null;
    avatarUrl: string | null;
  } | null;
  parent?: {
    id: string;
    title: string;
  } | null;
  children?: Array<{
    id: string;
    title: string;
    owner?: {
      id: string;
      email: string;
      name: string | null;
      avatarUrl: string | null;
    } | null;
  }>;
  _count?: {
    strategyNodes: number;
  };
}

export interface CreateObjectiveData {
  title: string;
  keyResults: KeyResult[];
  parentId?: string;
  ownerId?: string;
}

export interface UpdateObjectiveData {
  title?: string;
  keyResults?: KeyResult[];
  parentId?: string;
}

export function useObjectives(workspaceId: string) {
  return useQuery({
    queryKey: ['objectives', workspaceId],
    queryFn: async () => {
      return apiClient.get<Objective[]>(`/workspaces/${workspaceId}/objectives`);
    },
    enabled: !!workspaceId,
  });
}

export function useObjective(id: string) {
  return useQuery({
    queryKey: ['objective', id],
    queryFn: async () => {
      // まずworkspaceIdを取得する必要があるが、簡略化のため
      // 実際の実装ではworkspaceIdも必要
      throw new Error('useObjective requires workspaceId');
    },
    enabled: false,
  });
}

export function useObjectiveWithWorkspace(workspaceId: string, id: string) {
  return useQuery({
    queryKey: ['objective', workspaceId, id],
    queryFn: async () => {
      return apiClient.get<Objective>(`/workspaces/${workspaceId}/objectives/${id}`);
    },
    enabled: !!workspaceId && !!id,
  });
}

export function useCreateObjective(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateObjectiveData) => {
      return apiClient.post<Objective>(`/workspaces/${workspaceId}/objectives`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['objectives', workspaceId] });
    },
  });
}

export function useUpdateObjective(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: UpdateObjectiveData }) => {
      return apiClient.patch<Objective>(
        `/workspaces/${workspaceId}/objectives/${id}`,
        data,
      );
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['objectives', workspaceId] });
      queryClient.invalidateQueries({ queryKey: ['objective', workspaceId, variables.id] });
    },
  });
}

export function useDeleteObjective(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      return apiClient.delete(`/workspaces/${workspaceId}/objectives/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['objectives', workspaceId] });
    },
  });
}

