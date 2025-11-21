import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { useRouter } from 'next/navigation';

export interface Workspace {
  id: string;
  name: string;
  coreMission: string | null;
  createdAt: string;
  updatedAt: string;
  members: Array<{
    id: string;
    role: string;
    user: {
      id: string;
      email: string;
      name: string | null;
      avatarUrl: string | null;
    };
  }>;
  _count?: {
    objectives: number;
    tasks: number;
    strategyNodes?: number;
  };
}

export interface CreateWorkspaceData {
  name: string;
  coreMission?: string;
}

export interface UpdateWorkspaceData {
  name?: string;
  coreMission?: string;
}

export interface InviteMemberData {
  email: string;
  role?: string;
}

export function useWorkspaces() {
  return useQuery({
    queryKey: ['workspaces'],
    queryFn: async () => {
      return apiClient.get<Workspace[]>('/workspaces');
    },
  });
}

export function useWorkspace(id: string) {
  return useQuery({
    queryKey: ['workspace', id],
    queryFn: async () => {
      return apiClient.get<Workspace>(`/workspaces/${id}`);
    },
    enabled: !!id,
  });
}

export function useCreateWorkspace() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: async (data: CreateWorkspaceData) => {
      return apiClient.post<Workspace>('/workspaces', data);
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
      router.push(`/workspaces/${data.id}`);
    },
  });
}

export function useUpdateWorkspace() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      id,
      data,
    }: {
      id: string;
      data: UpdateWorkspaceData;
    }) => {
      return apiClient.patch<Workspace>(`/workspaces/${id}`, data);
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
      queryClient.invalidateQueries({ queryKey: ['workspace', data.id] });
    },
  });
}

export function useDeleteWorkspace() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: async (id: string) => {
      return apiClient.delete(`/workspaces/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
      router.push('/dashboard');
    },
  });
}

export function useInviteMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      workspaceId,
      data,
    }: {
      workspaceId: string;
      data: InviteMemberData;
    }) => {
      return apiClient.post(`/workspaces/${workspaceId}/members`, data);
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['workspace', variables.workspaceId] });
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    },
  });
}

export function useUpdateMemberRole() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      workspaceId,
      memberId,
      role,
    }: {
      workspaceId: string;
      memberId: string;
      role: string;
    }) => {
      return apiClient.patch(
        `/workspaces/${workspaceId}/members/${memberId}/role`,
        { role },
      );
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['workspace', variables.workspaceId] });
    },
  });
}

export function useRemoveMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      workspaceId,
      memberId,
    }: {
      workspaceId: string;
      memberId: string;
    }) => {
      return apiClient.delete(
        `/workspaces/${workspaceId}/members/${memberId}`,
      );
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['workspace', variables.workspaceId] });
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    },
  });
}

