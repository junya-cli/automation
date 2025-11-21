'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useCreateStrategyNode } from '@/hooks/use-strategy-nodes';
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

const createStrategyNodeSchema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  description: z.string().optional(),
  objectiveId: z.string().optional(),
  parentId: z.string().optional(),
});

type CreateStrategyNodeFormValues = z.infer<typeof createStrategyNodeSchema>;

interface CreateStrategyNodeDialogProps {
  workspaceId: string;
  objectiveId?: string;
  parentId?: string;
  objectives?: Array<{ id: string; title: string }>;
}

export function CreateStrategyNodeDialog({
  workspaceId,
  objectiveId,
  parentId,
  objectives,
}: CreateStrategyNodeDialogProps) {
  const [open, setOpen] = useState(false);
  const createStrategyNode = useCreateStrategyNode(workspaceId);

  const form = useForm<CreateStrategyNodeFormValues>({
    resolver: zodResolver(createStrategyNodeSchema),
    defaultValues: {
      title: '',
      description: '',
      objectiveId: objectiveId || '',
      parentId: parentId || '',
    },
  });

  const onSubmit = (data: CreateStrategyNodeFormValues) => {
    createStrategyNode.mutate(
      {
        ...data,
        objectiveId: data.objectiveId || undefined,
        parentId: data.parentId || undefined,
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
          ノードを追加
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>新しい戦略ノードを作成</DialogTitle>
          <DialogDescription>
            目標達成のための戦略やイニシアチブを追加します
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
                    <Input placeholder="例: マーケティング戦略の策定" {...field} />
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
                    <Textarea
                      placeholder="戦略の詳細を入力してください"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {objectives && objectives.length > 0 && !objectiveId && (
              <FormField
                control={form.control}
                name="objectiveId"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>関連する目標（任意）</FormLabel>
                    <FormControl>
                      <select
                        {...field}
                        className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                      >
                        <option value="">選択なし</option>
                        {objectives.map((obj) => (
                          <option key={obj.id} value={obj.id}>
                            {obj.title}
                          </option>
                        ))}
                      </select>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}
            {createStrategyNode.error && (
              <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                {createStrategyNode.error.message || '作成に失敗しました'}
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
              <Button type="submit" disabled={createStrategyNode.isPending}>
                {createStrategyNode.isPending ? '作成中...' : '作成'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}

