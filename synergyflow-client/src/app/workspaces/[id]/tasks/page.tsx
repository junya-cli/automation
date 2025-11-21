'use client';

import { useParams } from 'next/navigation';
import { AuthGuard } from '@/components/auth-guard';
import { useTasks, useUpdateTask, Task } from '@/hooks/use-tasks';
import { useWorkspace } from '@/hooks/use-workspaces';
import { useStrategyNodes } from '@/hooks/use-strategy-nodes';
import { CreateTaskDialog } from '@/components/task/create-task-dialog';
import { TaskDetailDialog } from '@/components/task/task-detail-dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import { useState } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
} from '@dnd-kit/core';
import {
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

const STATUSES = [
  { id: 'todo', label: '未着手', color: 'bg-gray-100' },
  { id: 'in_progress', label: '進行中', color: 'bg-blue-100' },
  { id: 'done', label: '完了', color: 'bg-green-100' },
];

function TaskCard({ task }: { task: Task }) {
  return (
    <Card className="mb-2 cursor-move hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <h4 className="font-medium mb-2">{task.title}</h4>
        {task.description && (
          <p className="text-sm text-gray-600 mb-2 line-clamp-2">{task.description}</p>
        )}
        {task.assignee && (
          <p className="text-xs text-gray-500 mb-1">
            担当: {task.assignee.name || task.assignee.email}
          </p>
        )}
        {task.dueDate && (
          <p className="text-xs text-gray-500">
            期限: {new Date(task.dueDate).toLocaleDateString('ja-JP')}
          </p>
        )}
        {task.strategyNode && (
          <p className="text-xs text-blue-600 mt-1">
            戦略: {task.strategyNode.title}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

function SortableTaskCard({ task }: { task: Task }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: task.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <TaskCard task={task} />
    </div>
  );
}

function DroppableColumn({
  status,
  tasks,
  onTaskClick,
}: {
  status: { id: string; label: string; color: string };
  tasks: Task[];
  onTaskClick: (task: Task) => void;
}) {
  const { setNodeRef } = useSortable({ id: status.id });

  return (
    <div ref={setNodeRef} className="flex-1 min-w-[300px]">
      <div className={`${status.color} p-3 rounded-t-lg`}>
        <h3 className="font-semibold">
          {status.label} ({tasks.length})
        </h3>
      </div>
      <div className="border border-t-0 rounded-b-lg p-4 min-h-[400px] bg-gray-50">
        <SortableContext
          items={tasks.map((t) => t.id)}
          strategy={verticalListSortingStrategy}
        >
          {tasks.map((task) => (
            <div key={task.id} onClick={() => onTaskClick(task)}>
              <SortableTaskCard task={task} />
            </div>
          ))}
        </SortableContext>
      </div>
    </div>
  );
}

export default function TasksPage() {
  const params = useParams();
  const workspaceId = params.id as string;
  const { data: tasks, isLoading } = useTasks(workspaceId);
  const { data: workspace } = useWorkspace(workspaceId);
  const { data: strategyNodes } = useStrategyNodes(workspaceId);
  const updateTask = useUpdateTask(workspaceId);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [activeId, setActiveId] = useState<string | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    }),
  );

  const tasksByStatus = {
    todo: tasks?.filter((t) => t.status === 'todo') || [],
    in_progress: tasks?.filter((t) => t.status === 'in_progress') || [],
    done: tasks?.filter((t) => t.status === 'done') || [],
  };

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveId(null);

    if (!over) {
      return;
    }

    const taskId = active.id as string;
    const overId = over.id as string;

    // タスクを別のタスクの上にドロップした場合は無視
    const task = tasks?.find((t) => t.id === overId);
    if (task) {
      return;
    }

    // ステータスカラムにドロップされた場合
    if (STATUSES.some((s) => s.id === overId)) {
      const currentTask = tasks?.find((t) => t.id === taskId);
      if (currentTask && currentTask.status !== overId) {
        updateTask.mutate({
          id: taskId,
          data: { status: overId },
        });
      }
    }
  };

  const activeTask = activeId ? tasks?.find((t) => t.id === activeId) : null;

  const members = workspace?.members.map((m) => m.user) || [];

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
                <h1 className="text-xl font-bold text-gray-900">タスクボード</h1>
              </div>
              <CreateTaskDialog
                workspaceId={workspaceId}
                members={members}
                strategyNodes={strategyNodes}
              />
            </div>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {isLoading ? (
            <p className="text-gray-600">読み込み中...</p>
          ) : (
            <DndContext
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragStart={handleDragStart}
              onDragEnd={handleDragEnd}
            >
              <div className="flex gap-4 overflow-x-auto">
                {STATUSES.map((status) => (
                  <SortableContext
                    key={status.id}
                    id={status.id}
                    items={tasksByStatus[status.id as keyof typeof tasksByStatus].map(
                      (t) => t.id,
                    )}
                    strategy={verticalListSortingStrategy}
                  >
                    <DroppableColumn
                      status={status}
                      tasks={tasksByStatus[status.id as keyof typeof tasksByStatus]}
                      onTaskClick={setSelectedTask}
                    />
                  </SortableContext>
                ))}
              </div>
              <DragOverlay>
                {activeTask ? <TaskCard task={activeTask} /> : null}
              </DragOverlay>
            </DndContext>
          )}
        </main>
        <TaskDetailDialog
          workspaceId={workspaceId}
          task={selectedTask}
          open={!!selectedTask}
          onOpenChange={(open) => !open && setSelectedTask(null)}
        />
      </div>
    </AuthGuard>
  );
}

