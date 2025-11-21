'use client';

import { AuthGuard } from '@/components/auth-guard';
import { useAuthStore } from '@/store/auth-store';
import { useLogout } from '@/hooks/use-auth';
import { useWorkspaces } from '@/hooks/use-workspaces';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CreateWorkspaceDialog } from '@/components/workspace/create-workspace-dialog';
import Link from 'next/link';

export default function DashboardPage() {
  const user = useAuthStore((state) => state.user);
  const logout = useLogout();
  const { data: workspaces, isLoading } = useWorkspaces();

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <h1 className="text-xl font-bold text-gray-900">SynergyFlow</h1>
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-700">
                  {user?.name || user?.email}
                </span>
                <Button variant="outline" onClick={logout}>
                  ログアウト
                </Button>
              </div>
            </div>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8 flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">ワークスペース</h2>
              <p className="text-gray-600 mt-2">
                チームやプロジェクトのワークスペースを管理
              </p>
            </div>
            <CreateWorkspaceDialog />
          </div>

          {isLoading ? (
            <div className="text-center py-12">
              <p className="text-gray-600">読み込み中...</p>
            </div>
          ) : workspaces && workspaces.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {workspaces.map((workspace) => (
                <Link key={workspace.id} href={`/workspaces/${workspace.id}`}>
                  <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                    <CardHeader>
                      <CardTitle>{workspace.name}</CardTitle>
                      {workspace.coreMission && (
                        <CardDescription className="line-clamp-2">
                          {workspace.coreMission}
                        </CardDescription>
                      )}
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2 text-sm text-gray-600">
                        <div className="flex items-center justify-between">
                          <span>メンバー数</span>
                          <span className="font-medium">{workspace.members.length}</span>
                        </div>
                        {workspace._count && (
                          <>
                            <div className="flex items-center justify-between">
                              <span>目標数</span>
                              <span className="font-medium">{workspace._count.objectives}</span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span>タスク数</span>
                              <span className="font-medium">{workspace._count.tasks}</span>
                            </div>
                          </>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-gray-600 mb-4">
                  ワークスペースがありません
                </p>
                <CreateWorkspaceDialog />
              </CardContent>
            </Card>
          )}
        </main>
      </div>
    </AuthGuard>
  );
}
