'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useCreateTask } from '@/hooks/use-tasks';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Textarea } from '@/components/ui/textarea';
import { Plus } from 'lucide-react';

const createTaskSchema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  description: z.string().optional(),
  strategyNodeId: z.string().optional(),
  assigneeId: z.string().optional(),
  status: z.enum(['todo', 'in_progress', 'done']).default('todo'),
  dueDate: z.string().optional(),
});

type CreateTaskFormValues = z.infer<typeof createTaskSchema>;

interface CreateTaskDialogProps {
  workspaceId: string;
  strategyNodeId?: string;
  members?: Array<{ id: string; email: string; name: string | null }>;
  strategyNodes?: Array<{ id: string; title: string }>;
}

export function CreateTaskDialog({
  workspaceId,
  strategyNodeId,
  members,
  strategyNodes,
}: CreateTaskDialogProps) {
  const [open, setOpen] = useState(false);
  const createTask = useCreateTask(workspaceId);

  const form = useForm<CreateTaskFormValues>({
    resolver: zodResolver(createTaskSchema),
    defaultValues: {
      title: '',
      description: '',
      strategyNodeId: strategyNodeId || '',
      assigneeId: '',
      status: 'todo',
      dueDate: '',
    },
  });

  const onSubmit = (data: CreateTaskFormValues) => {
    createTask.mutate(
      {
        ...data,
        strategyNodeId: data.strategyNodeId || undefined,
        assigneeId: data.assigneeId || undefined,
        dueDate: data.dueDate || undefined,
      },
      {
        onSuccess: () => {
          setOpen(false);
          form.reset();
        },
      },
    );
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <Plus className="h-4 w-4 mr-2" />
          タスクを追加
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>新しいタスクを作成</DialogTitle>
          <DialogDescription>
            タスクの詳細を入力してください
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>タイトル *</FormLabel>
                  <FormControl>
                    <Input placeholder="例: マーケティング資料を作成" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>説明（任意）</FormLabel>
                  <FormControl>
                    <Textarea placeholder="タスクの詳細を入力してください" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {strategyNodes && strategyNodes.length > 0 && !strategyNodeId && (
              <FormField
                control={form.control}
                name="strategyNodeId"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>関連する戦略ノード（任意）</FormLabel>
                    <FormControl>
                      <select
                        {...field}
                        className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                      >
                        <option value="">選択なし</option>
                        {strategyNodes.map((node) => (
                          <option key={node.id} value={node.id}>
                            {node.title}
                          </option>
                        ))}
                      </select>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}
            {members && members.length > 0 && (
              <FormField
                control={form.control}
                name="assigneeId"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>担当者（任意）</FormLabel>
                    <FormControl>
                      <select
                        {...field}
                        className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                      >
                        <option value="">選択なし</option>
                        {members.map((member) => (
                          <option key={member.id} value={member.id}>
                            {member.name || member.email}
                          </option>
                        ))}
                      </select>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}
            <FormField
              control={form.control}
              name="dueDate"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>期限（任意）</FormLabel>
                  <FormControl>
                    <Input type="date" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {createTask.error && (
              <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                {createTask.error.message || '作成に失敗しました'}
              </div>
            )}
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setOpen(false)}
              >
                キャンセル
              </Button>
              <Button type="submit" disabled={createTask.isPending}>
                {createTask.isPending ? '作成中...' : '作成'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}

