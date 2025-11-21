import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api-client';
import { useAuthStore } from '@/store/auth-store';

interface SignupData {
  email: string;
  password: string;
  name?: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface AuthResponse {
  accessToken: string;
  user: {
    id: string;
    email: string;
    name: string | null;
    avatarUrl: string | null;
  };
}

export function useSignup() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  return useMutation({
    mutationFn: async (data: SignupData) => {
      return apiClient.post<AuthResponse>('/auth/signup', data);
    },
    onSuccess: (data) => {
      setAuth(data.user, data.accessToken);
      router.push('/dashboard');
    },
  });
}

export function useLogin() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  return useMutation({
    mutationFn: async (data: LoginData) => {
      return apiClient.post<AuthResponse>('/auth/login', data);
    },
    onSuccess: (data) => {
      setAuth(data.user, data.accessToken);
      router.push('/dashboard');
    },
  });
}

export function useLogout() {
  const router = useRouter();
  const clearAuth = useAuthStore((state) => state.clearAuth);
  const queryClient = useQueryClient();

  return () => {
    clearAuth();
    queryClient.clear();
    router.push('/login');
  };
}

export function useMe() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return useQuery({
    queryKey: ['me'],
    queryFn: async () => {
      return apiClient.get<AuthResponse['user']>('/auth/me');
    },
    enabled: isAuthenticated,
  });
}

