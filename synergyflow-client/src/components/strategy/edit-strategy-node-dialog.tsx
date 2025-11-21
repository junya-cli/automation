'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useUpdateStrategyNode, StrategyNode } from '@/hooks/use-strategy-nodes';
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

const editStrategyNodeSchema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  description: z.string().optional(),
});

type EditStrategyNodeFormValues = z.infer<typeof editStrategyNodeSchema>;

interface EditStrategyNodeDialogProps {
  workspaceId: string;
  node: StrategyNode | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  objectives?: Array<{ id: string; title: string }>;
}

export function EditStrategyNodeDialog({
  workspaceId,
  node,
  open,
  onOpenChange,
  objectives,
}: EditStrategyNodeDialogProps) {
  const updateStrategyNode = useUpdateStrategyNode(workspaceId);
  const form = useForm<EditStrategyNodeFormValues>({
    resolver: zodResolver(editStrategyNodeSchema),
    defaultValues: {
      title: '',
      description: '',
    },
  });

  useEffect(() => {
    if (node) {
      form.reset({
        title: node.title,
        description: node.description || '',
      });
    }
  }, [node, form]);

  const onSubmit = (data: EditStrategyNodeFormValues) => {
    if (!node) return;

    updateStrategyNode.mutate(
      {
        id: node.id,
        data,
      },
      {
        onSuccess: () => {
          onOpenChange(false);
        },
      },
    );
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>戦略ノードを編集</DialogTitle>
          <DialogDescription>
            戦略ノードの情報を更新します
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
            {updateStrategyNode.error && (
              <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                {updateStrategyNode.error.message || '更新に失敗しました'}
              </div>
            )}
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => onOpenChange(false)}
              >
                キャンセル
              </Button>
              <Button type="submit" disabled={updateStrategyNode.isPending}>
                {updateStrategyNode.isPending ? '更新中...' : '更新'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}

