'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useCreateWorkspace } from '@/hooks/use-workspaces';
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

const createWorkspaceSchema = z.object({
  name: z.string().min(1, 'ワークスペース名を入力してください'),
  coreMission: z.string().optional(),
});

type CreateWorkspaceFormValues = z.infer<typeof createWorkspaceSchema>;

export function CreateWorkspaceDialog() {
  const [open, setOpen] = useState(false);
  const createWorkspace = useCreateWorkspace();

  const form = useForm<CreateWorkspaceFormValues>({
    resolver: zodResolver(createWorkspaceSchema),
    defaultValues: {
      name: '',
      coreMission: '',
    },
  });

  const onSubmit = (data: CreateWorkspaceFormValues) => {
    createWorkspace.mutate(data, {
      onSuccess: () => {
        setOpen(false);
        form.reset();
      },
    });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>新しいワークスペースを作成</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>新しいワークスペースを作成</DialogTitle>
          <DialogDescription>
            チームやプロジェクトのワークスペースを作成します
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>ワークスペース名 *</FormLabel>
                  <FormControl>
                    <Input placeholder="例: プロジェクトA" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="coreMission"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>コアミッション（任意）</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="このワークスペースの最上位目標を入力してください"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {createWorkspace.error && (
              <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                {createWorkspace.error.message || '作成に失敗しました'}
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
              <Button type="submit" disabled={createWorkspace.isPending}>
                {createWorkspace.isPending ? '作成中...' : '作成'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}

