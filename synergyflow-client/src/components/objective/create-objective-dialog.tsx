'use client';

import { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useCreateObjective, KeyResult } from '@/hooks/use-objectives';
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
import { Plus, X } from 'lucide-react';

const createObjectiveSchema = z.object({
  title: z.string().min(1, '目標タイトルを入力してください'),
  keyResults: z
    .array(
      z.object({
        name: z.string().min(1, 'Key Result名を入力してください'),
        current: z.number().min(0, '現在値は0以上で入力してください'),
        target: z.number().min(1, '目標値は1以上で入力してください'),
      }),
    )
    .min(1, '少なくとも1つのKey Resultが必要です'),
});

type CreateObjectiveFormValues = z.infer<typeof createObjectiveSchema>;

interface CreateObjectiveDialogProps {
  workspaceId: string;
  parentId?: string;
}

export function CreateObjectiveDialog({
  workspaceId,
  parentId,
}: CreateObjectiveDialogProps) {
  const [open, setOpen] = useState(false);
  const createObjective = useCreateObjective(workspaceId);

  const form = useForm<CreateObjectiveFormValues>({
    resolver: zodResolver(createObjectiveSchema),
    defaultValues: {
      title: '',
      keyResults: [{ name: '', current: 0, target: 100 }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'keyResults',
  });

  const onSubmit = (data: CreateObjectiveFormValues) => {
    createObjective.mutate(
      {
        ...data,
        parentId,
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
          目標を追加
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>新しい目標を作成</DialogTitle>
          <DialogDescription>
            OKR（Objectives & Key Results）を設定します
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>目標タイトル *</FormLabel>
                  <FormControl>
                    <Input placeholder="例: 売上を50%向上させる" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <FormLabel>Key Results *</FormLabel>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => append({ name: '', current: 0, target: 100 })}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  追加
                </Button>
              </div>

              {fields.map((field, index) => (
                <div key={field.id} className="border p-4 rounded-md space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Key Result {index + 1}</span>
                    {fields.length > 1 && (
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => remove(index)}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                  <FormField
                    control={form.control}
                    name={`keyResults.${index}.name`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>名称</FormLabel>
                        <FormControl>
                          <Input placeholder="例: 新規顧客を100名獲得" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <div className="grid grid-cols-2 gap-3">
                    <FormField
                      control={form.control}
                      name={`keyResults.${index}.current`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>現在値</FormLabel>
                          <FormControl>
                            <Input
                              type="number"
                              {...field}
                              onChange={(e) => field.onChange(Number(e.target.value))}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name={`keyResults.${index}.target`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>目標値</FormLabel>
                          <FormControl>
                            <Input
                              type="number"
                              {...field}
                              onChange={(e) => field.onChange(Number(e.target.value))}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                </div>
              ))}
            </div>

            {createObjective.error && (
              <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                {createObjective.error.message || '作成に失敗しました'}
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
              <Button type="submit" disabled={createObjective.isPending}>
                {createObjective.isPending ? '作成中...' : '作成'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}

