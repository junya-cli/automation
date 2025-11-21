'use client';

import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useUpdateTask, useDeleteTask, Task } from '@/hooks/use-tasks';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
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

const editTaskSchema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  description: z.string().optional(),
  status: z.enum(['todo', 'in_progress', 'done']),
  dueDate: z.string().optional(),
});

type EditTaskFormValues = z.infer<typeof editTaskSchema>;

interface TaskDetailDialogProps {
  workspaceId: string;
  task: Task | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function TaskDetailDialog({
  workspaceId,
  task,
  open,
  onOpenChange,
}: TaskDetailDialogProps) {
  const updateTask = useUpdateTask(workspaceId);
  const deleteTask = useDeleteTask(workspaceId);
  const form = useForm<EditTaskFormValues>({
    resolver: zodResolver(editTaskSchema),
    defaultValues: {
      title: '',
      description: '',
      status: 'todo',
      dueDate: '',
    },
  });

  useEffect(() => {
    if (task) {
      form.reset({
        title: task.title,
        description: task.description || '',
        status: task.status as 'todo' | 'in_progress' | 'done',
        dueDate: task.dueDate ? task.dueDate.split('T')[0] : '',
      });
    }
  }, [task, form]);

  const onSubmit = (data: EditTaskFormValues) => {
    if (!task) return;

    updateTask.mutate(
      {
        id: task.id,
        data: {
          ...data,
          dueDate: data.dueDate || undefined,
        },
      },
      {
        onSuccess: () => {
          onOpenChange(false);
        },
      },
    );
  };

  const handleDelete = () => {
    if (!task) return;
    if (confirm('このタスクを削除しますか？')) {
      deleteTask.mutate(task.id, {
        onSuccess: () => {
          onOpenChange(false);
        },
      });
    }
  };

  if (!task) return null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>タスクの詳細</DialogTitle>
          <DialogDescription>
            タスクの情報を編集します
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
                    <Input {...field} />
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
                  <FormLabel>説明</FormLabel>
                  <FormControl>
                    <Textarea {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="status"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>ステータス</FormLabel>
                  <FormControl>
                    <select
                      {...field}
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    >
                      <option value="todo">未着手</option>
                      <option value="in_progress">進行中</option>
                      <option value="done">完了</option>
                    </select>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="dueDate"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>期限</FormLabel>
                  <FormControl>
                    <Input type="date" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {task.assignee && (
              <div>
                <FormLabel>担当者</FormLabel>
                <p className="text-sm text-gray-700 mt-1">
                  {task.assignee.name || task.assignee.email}
                </p>
              </div>
            )}
            {task.strategyNode && (
              <div>
                <FormLabel>関連する戦略ノード</FormLabel>
                <p className="text-sm text-gray-700 mt-1">{task.strategyNode.title}</p>
              </div>
            )}
            {updateTask.error && (
              <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                {updateTask.error.message || '更新に失敗しました'}
              </div>
            )}
            <DialogFooter className="flex justify-between">
              <Button
                type="button"
                variant="destructive"
                onClick={handleDelete}
                disabled={deleteTask.isPending}
              >
                {deleteTask.isPending ? '削除中...' : '削除'}
              </Button>
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => onOpenChange(false)}
                >
                  キャンセル
                </Button>
                <Button type="submit" disabled={updateTask.isPending}>
                  {updateTask.isPending ? '更新中...' : '更新'}
                </Button>
              </div>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}

