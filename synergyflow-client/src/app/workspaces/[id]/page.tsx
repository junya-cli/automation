'use client';

import { useParams } from 'next/navigation';
import { AuthGuard } from '@/components/auth-guard';
import { useAuthStore } from '@/store/auth-store';
import { useWorkspace, useInviteMember } from '@/hooks/use-workspaces';
import { useObjectives } from '@/hooks/use-objectives';
import { CreateObjectiveDialog } from '@/components/objective/create-objective-dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useState } from 'react';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Progress } from '@/components/ui/progress';

const inviteMemberSchema = z.object({
  email: z.string().email('有効なメールアドレスを入力してください'),
  role: z.enum(['admin', 'member']).default('member'),
});

type InviteMemberFormValues = z.infer<typeof inviteMemberSchema>;

export default function WorkspaceDetailPage() {
  const params = useParams();
  const workspaceId = params.id as string;
  const { data: workspace, isLoading } = useWorkspace(workspaceId);
  const { data: objectives, isLoading: objectivesLoading } = useObjectives(workspaceId);
  const user = useAuthStore((state) => state.user);
  const inviteMember = useInviteMember();
  const [showInviteForm, setShowInviteForm] = useState(false);

  const form = useForm<InviteMemberFormValues>({
    resolver: zodResolver(inviteMemberSchema),
    defaultValues: {
      email: '',
      role: 'member',
    },
  });

  const onSubmit = (data: InviteMemberFormValues) => {
    inviteMember.mutate(
      { workspaceId, data },
      {
        onSuccess: () => {
          form.reset();
          setShowInviteForm(false);
        },
      },
    );
  };

  const currentUserMember = workspace?.members.find((m) => m.user.id === user?.id);
  const isAdmin = currentUserMember?.role === 'admin';

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <p className="text-gray-600">読み込み中...</p>
        </div>
      </AuthGuard>
    );
  }

  if (!workspace) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <p className="text-gray-600 mb-4">ワークスペースが見つかりません</p>
            <Link href="/dashboard">
              <Button>ダッシュボードに戻る</Button>
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
                <Link href="/dashboard">
                  <Button variant="ghost">← 戻る</Button>
                </Link>
                <h1 className="text-xl font-bold text-gray-900">{workspace.name}</h1>
              </div>
              <div className="flex items-center gap-2">
                <Link href={`/workspaces/${workspaceId}/dashboard`}>
                  <Button variant="outline" size="sm">ダッシュボード</Button>
                </Link>
                <Link href={`/workspaces/${workspaceId}/strategy`}>
                  <Button variant="outline" size="sm">戦略プランナー</Button>
                </Link>
                <Link href={`/workspaces/${workspaceId}/tasks`}>
                  <Button variant="outline" size="sm">タスクボード</Button>
                </Link>
              </div>
            </div>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">ワークスペース詳細</h2>
            {workspace.coreMission && (
              <p className="text-gray-600">{workspace.coreMission}</p>
            )}
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>メンバー</CardTitle>
                <CardDescription>
                  ワークスペースのメンバーを管理
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {isAdmin && (
                  <div>
                    {!showInviteForm ? (
                      <Button onClick={() => setShowInviteForm(true)}>
                        メンバーを招待
                      </Button>
                    ) : (
                      <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                          <FormField
                            control={form.control}
                            name="email"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>メールアドレス</FormLabel>
                                <FormControl>
                                  <Input type="email" placeholder="example@email.com" {...field} />
                                </FormControl>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          <FormField
                            control={form.control}
                            name="role"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>ロール</FormLabel>
                                <Select
                                  onValueChange={field.onChange}
                                  defaultValue={field.value}
                                >
                                  <FormControl>
                                    <SelectTrigger>
                                      <SelectValue placeholder="ロールを選択" />
                                    </SelectTrigger>
                                  </FormControl>
                                  <SelectContent>
                                    <SelectItem value="member">メンバー</SelectItem>
                                    <SelectItem value="admin">管理者</SelectItem>
                                  </SelectContent>
                                </Select>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          {inviteMember.error && (
                            <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                              {inviteMember.error.message || '招待に失敗しました'}
                            </div>
                          )}
                          <div className="flex gap-2">
                            <Button
                              type="button"
                              variant="outline"
                              onClick={() => {
                                setShowInviteForm(false);
                                form.reset();
                              }}
                            >
                              キャンセル
                            </Button>
                            <Button type="submit" disabled={inviteMember.isPending}>
                              {inviteMember.isPending ? '招待中...' : '招待'}
                            </Button>
                          </div>
                        </form>
                      </Form>
                    )}
                  </div>
                )}
                <div className="space-y-2">
                  {workspace.members.map((member) => (
                    <div
                      key={member.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
                    >
                      <div>
                        <p className="font-medium">
                          {member.user.name || member.user.email}
                        </p>
                        <p className="text-sm text-gray-600">{member.user.email}</p>
                      </div>
                      <span className="text-sm px-2 py-1 bg-blue-100 text-blue-800 rounded">
                        {member.role === 'admin' ? '管理者' : 'メンバー'}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>統計</CardTitle>
                <CardDescription>
                  ワークスペースの活動状況
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {workspace._count && (
                    <>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-600">目標数</span>
                        <span className="text-2xl font-bold">{workspace._count.objectives}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-600">タスク数</span>
                        <span className="text-2xl font-bold">{workspace._count.tasks}</span>
                      </div>
                      {workspace._count.strategyNodes !== undefined && (
                        <div className="flex items-center justify-between">
                          <span className="text-gray-600">戦略ノード数</span>
                          <span className="text-2xl font-bold">
                            {workspace._count.strategyNodes}
                          </span>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="mt-6">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>目標（OKR）</CardTitle>
                  <CardDescription>
                    ワークスペースの目標を管理
                  </CardDescription>
                </div>
                <CreateObjectiveDialog workspaceId={workspaceId} />
              </div>
            </CardHeader>
            <CardContent>
              {objectivesLoading ? (
                <p className="text-gray-600">読み込み中...</p>
              ) : objectives && objectives.length > 0 ? (
                <div className="space-y-4">
                  {objectives.map((objective) => (
                    <Link
                      key={objective.id}
                      href={`/workspaces/${workspaceId}/objectives/${objective.id}`}
                    >
                      <Card className="hover:shadow-md transition-shadow cursor-pointer">
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h3 className="font-semibold text-lg mb-2">{objective.title}</h3>
                              {objective.parent && (
                                <p className="text-sm text-gray-500 mb-2">
                                  親目標: {objective.parent.title}
                                </p>
                              )}
                              <div className="space-y-2">
                                {objective.keyResults.map((kr, idx) => (
                                  <div key={idx} className="text-sm">
                                    <div className="flex items-center justify-between mb-1">
                                      <span className="text-gray-700">{kr.name}</span>
                                      <span className="text-gray-600">
                                        {kr.current} / {kr.target}
                                      </span>
                                    </div>
                                    <Progress
                                      value={(kr.current / kr.target) * 100}
                                      className="h-2"
                                    />
                                  </div>
                                ))}
                              </div>
                            </div>
                            <div className="ml-4 text-right">
                              <div className="text-2xl font-bold text-blue-600">
                                {objective.progress}%
                              </div>
                              <div className="text-xs text-gray-500">進捗率</div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-600">
                  <p>目標がありません</p>
                  <div className="mt-4">
                    <CreateObjectiveDialog workspaceId={workspaceId} />
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </main>
      </div>
    </AuthGuard>
  );
}

