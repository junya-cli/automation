'use client';

import { useParams } from 'next/navigation';
import { AuthGuard } from '@/components/auth-guard';
import { useDashboard } from '@/hooks/use-dashboard';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c'];

export default function DashboardPage() {
  const params = useParams();
  const workspaceId = params.id as string;
  const { data: dashboard, isLoading } = useDashboard(workspaceId);

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <p className="text-gray-600">読み込み中...</p>
        </div>
      </AuthGuard>
    );
  }

  if (!dashboard) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <p className="text-gray-600">データが見つかりません</p>
        </div>
      </AuthGuard>
    );
  }

  // 目標の進捗状況データ
  const objectiveProgressData = [
    { name: '高（80%以上）', value: dashboard.objectives.byProgress.high },
    { name: '中（50-79%）', value: dashboard.objectives.byProgress.medium },
    { name: '低（50%未満）', value: dashboard.objectives.byProgress.low },
  ];

  // タスクのステータスデータ
  const taskStatusData = [
    { name: '未着手', value: dashboard.tasks.todo },
    { name: '進行中', value: dashboard.tasks.inProgress },
    { name: '完了', value: dashboard.tasks.done },
  ];

  // メンバー別タスク完了率データ
  const memberCompletionData = dashboard.members
    .filter((m) => m.totalTasks > 0)
    .map((m) => ({
      name: m.user.name || m.user.email.split('@')[0],
      completionRate: m.completionRate,
      totalTasks: m.totalTasks,
      completedTasks: m.completedTasks,
    }))
    .sort((a, b) => b.completionRate - a.completionRate)
    .slice(0, 5);

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
                <h1 className="text-xl font-bold text-gray-900">ダッシュボード</h1>
              </div>
            </div>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* サマリーカード */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>目標数</CardDescription>
                <CardTitle className="text-3xl">{dashboard.objectives.total}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  平均進捗率: {dashboard.objectives.averageProgress}%
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>タスク数</CardDescription>
                <CardTitle className="text-3xl">{dashboard.tasks.total}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  完了率: {dashboard.tasks.completionRate}%
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>完了タスク</CardDescription>
                <CardTitle className="text-3xl">{dashboard.tasks.done}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  進行中: {dashboard.tasks.inProgress}
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>期限切れタスク</CardDescription>
                <CardTitle className="text-3xl text-red-600">
                  {dashboard.tasks.overdue}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">要対応</p>
              </CardContent>
            </Card>
          </div>

          {/* グラフセクション */}
          <div className="grid gap-6 md:grid-cols-2 mb-8">
            {/* 目標の進捗状況 */}
            <Card>
              <CardHeader>
                <CardTitle>目標の進捗状況</CardTitle>
                <CardDescription>目標の進捗率別の分布</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={objectiveProgressData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => {
                        const p = percent ?? 0;
                        return `${name}: ${(p * 100).toFixed(0)}%`;
                      }}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {objectiveProgressData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* タスクのステータス */}
            <Card>
              <CardHeader>
                <CardTitle>タスクのステータス</CardTitle>
                <CardDescription>タスクの状態別の分布</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={taskStatusData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => {
                        const p = percent ?? 0;
                        return `${name}: ${(p * 100).toFixed(0)}%`;
                      }}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {taskStatusData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* メンバー別パフォーマンス */}
          {memberCompletionData.length > 0 && (
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>メンバー別パフォーマンス</CardTitle>
                <CardDescription>タスク完了率（上位5名）</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={memberCompletionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="completionRate" fill="#8884d8" name="完了率 (%)" />
                    <Bar dataKey="totalTasks" fill="#82ca9d" name="総タスク数" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          )}

          {/* 最近の活動 */}
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>最近の活動</CardTitle>
                <CardDescription>直近7日間のタスク作成</CardDescription>
              </CardHeader>
              <CardContent>
                {dashboard.recentActivity.length > 0 ? (
                  <div className="space-y-3">
                    {dashboard.recentActivity.map((activity) => (
                      <div
                        key={activity.id}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
                      >
                        <div>
                          <p className="font-medium text-sm">{activity.title}</p>
                          <p className="text-xs text-gray-500">
                            {new Date(activity.createdAt).toLocaleDateString('ja-JP')}
                          </p>
                        </div>
                        <span
                          className={`text-xs px-2 py-1 rounded ${
                            activity.status === 'done'
                              ? 'bg-green-100 text-green-800'
                              : activity.status === 'in_progress'
                                ? 'bg-blue-100 text-blue-800'
                                : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {activity.status === 'done'
                            ? '完了'
                            : activity.status === 'in_progress'
                              ? '進行中'
                              : '未着手'}
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-600 text-sm">最近の活動はありません</p>
                )}
              </CardContent>
            </Card>

            {/* 目標一覧 */}
            <Card>
              <CardHeader>
                <CardTitle>目標一覧</CardTitle>
                <CardDescription>進捗率の高い目標（上位5件）</CardDescription>
              </CardHeader>
              <CardContent>
                {dashboard.objectives.list.length > 0 ? (
                  <div className="space-y-3">
                    {dashboard.objectives.list.map((objective) => (
                      <div
                        key={objective.id}
                        className="p-3 bg-gray-50 rounded-md"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <p className="font-medium text-sm">{objective.title}</p>
                          <span className="text-sm font-bold text-blue-600">
                            {objective.progress}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${objective.progress}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-600 text-sm">目標がありません</p>
                )}
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </AuthGuard>
  );
}

