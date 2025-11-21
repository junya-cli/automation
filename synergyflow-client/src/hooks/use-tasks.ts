import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export interface Task {
  id: string;
  workspaceId: string;
  strategyNodeId: string | null;
  title: string;
  description: string | null;
  assigneeId: string | null;
  status: string; // todo, in_progress, done
  dueDate: string | null;
  createdAt: string;
  updatedAt: string;
  assignee?: {
    id: string;
    email: string;
    name: string | null;
    avatarUrl: string | null;
  } | null;
  strategyNode?: {
    id: string;
    title: string;
  } | null;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  strategyNodeId?: string;
  assigneeId?: string;
  status?: string;
  dueDate?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  strategyNodeId?: string;
  assigneeId?: string;
  status?: string;
  dueDate?: string;
}

export function useTasks(workspaceId: string, strategyNodeId?: string) {
  return useQuery({
    queryKey: ['tasks', workspaceId, strategyNodeId],
    queryFn: async () => {
      const url = strategyNodeId
        ? `/workspaces/${workspaceId}/tasks?strategyNodeId=${strategyNodeId}`
        : `/workspaces/${workspaceId}/tasks`;
      return apiClient.get<Task[]>(url);
    },
    enabled: !!workspaceId,
  });
}

export function useTask(workspaceId: string, id: string) {
  return useQuery({
    queryKey: ['task', workspaceId, id],
    queryFn: async () => {
      return apiClient.get<Task>(`/workspaces/${workspaceId}/tasks/${id}`);
    },
    enabled: !!workspaceId && !!id,
  });
}

export function useCreateTask(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateTaskData) => {
      return apiClient.post<Task>(`/workspaces/${workspaceId}/tasks`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', workspaceId] });
    },
  });
}

export function useUpdateTask(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: UpdateTaskData }) => {
      return apiClient.patch<Task>(`/workspaces/${workspaceId}/tasks/${id}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', workspaceId] });
    },
  });
}

export function useDeleteTask(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      return apiClient.delete(`/workspaces/${workspaceId}/tasks/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', workspaceId] });
    },
  });
}

