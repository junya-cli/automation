'use client';

import { useParams } from 'next/navigation';
import { AuthGuard } from '@/components/auth-guard';
import { useObjectiveWithWorkspace } from '@/hooks/use-objectives';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import Link from 'next/link';

export default function ObjectiveDetailPage() {
  const params = useParams();
  // URLパスが /workspaces/[id]/objectives/[objectiveId] なので
  const workspaceId = params.id as string;
  const objectiveId = params.objectiveId as string;
  const { data: objective, isLoading } = useObjectiveWithWorkspace(workspaceId, objectiveId);

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <p className="text-gray-600">読み込み中...</p>
        </div>
      </AuthGuard>
    );
  }

  if (!objective) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <p className="text-gray-600 mb-4">目標が見つかりません</p>
            <Link href={`/workspaces/${workspaceId}`}>
              <Button>ワークスペースに戻る</Button>
            </Link>
          </div>
        </div>
      </AuthGuard>
    );
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center gap-4">
                <Link href={`/workspaces/${workspaceId}`}>
                  <Button variant="ghost">← 戻る</Button>
                </Link>
                <h1 className="text-xl font-bold text-gray-900">{objective.title}</h1>
              </div>
            </div>
          </div>
        </header>
        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl">{objective.title}</CardTitle>
                  {objective.parent && (
                    <CardDescription className="mt-2">
                      親目標: {objective.parent.title}
                    </CardDescription>
                  )}
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-blue-600">{objective.progress}%</div>
                  <div className="text-sm text-gray-500">進捗率</div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold text-lg mb-4">Key Results</h3>
                  <div className="space-y-4">
                    {objective.keyResults.map((kr, idx) => {
                      const progress = (kr.current / kr.target) * 100;
                      return (
                        <div key={idx} className="border rounded-lg p-4">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-medium">{kr.name}</span>
                            <span className="text-sm text-gray-600">
                              {kr.current} / {kr.target} ({Math.round(progress)}%)
                            </span>
                          </div>
                          <Progress value={progress} className="h-3" />
                        </div>
                      );
                    })}
                  </div>
                </div>

                {objective.children && objective.children.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-lg mb-4">子目標</h3>
                    <div className="space-y-2">
                      {objective.children.map((child) => (
                        <Link
                          key={child.id}
                          href={`/workspaces/${workspaceId}/objectives/${child.id}`}
                        >
                          <Card className="hover:shadow-md transition-shadow cursor-pointer">
                            <CardContent className="p-4">
                              <div className="flex items-center justify-between">
                                <span className="font-medium">{child.title}</span>
                                <span className="text-sm text-gray-500">→</span>
                              </div>
                            </CardContent>
                          </Card>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                {objective.owner && (
                  <div>
                    <h3 className="font-semibold text-lg mb-2">担当者</h3>
                    <p className="text-gray-700">
                      {objective.owner.name || objective.owner.email}
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </main>
      </div>
    </AuthGuard>
  );
}

