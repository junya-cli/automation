'use client';

import { useParams } from 'next/navigation';
import { AuthGuard } from '@/components/auth-guard';
import { useStrategyNodes, useDeleteStrategyNode, StrategyNode } from '@/hooks/use-strategy-nodes';
import { useObjectives } from '@/hooks/use-objectives';
import { CreateStrategyNodeDialog } from '@/components/strategy/create-strategy-node-dialog';
import { EditStrategyNodeDialog } from '@/components/strategy/edit-strategy-node-dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import { useState } from 'react';
import { ChevronRight, ChevronDown } from 'lucide-react';

// ツリー構造に変換するヘルパー関数
function buildTree(nodes: any[]) {
  const nodeMap = new Map();
  const rootNodes: any[] = [];

  // すべてのノードをマップに追加
  nodes.forEach((node) => {
    nodeMap.set(node.id, { ...node, children: [] });
  });

  // 親子関係を構築
  nodes.forEach((node) => {
    const nodeWithChildren = nodeMap.get(node.id);
    if (node.parentId) {
      const parent = nodeMap.get(node.parentId);
      if (parent) {
        parent.children.push(nodeWithChildren);
      } else {
        rootNodes.push(nodeWithChildren);
      }
    } else {
      rootNodes.push(nodeWithChildren);
    }
  });

  // 子ノードをソート
  function sortChildren(node: any) {
    if (node.children.length > 0) {
      node.children.sort((a: any, b: any) => a.order - b.order);
      node.children.forEach(sortChildren);
    }
  }

  rootNodes.forEach(sortChildren);
  rootNodes.sort((a, b) => a.order - b.order);

  return rootNodes;
}

function TreeNode({
  node,
  level = 0,
  onDelete,
  onEdit,
}: {
  node: any;
  level?: number;
  onDelete: (id: string) => void;
  onEdit: (node: any) => void;
}) {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="ml-4">
      <div
        className="flex items-center gap-2 p-3 rounded-md hover:bg-gray-50 border border-gray-200 mb-2"
        style={{ marginLeft: `${level * 20}px` }}
      >
        {node.children && node.children.length > 0 && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1 hover:bg-gray-200 rounded"
          >
            {isExpanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </button>
        )}
        <div className="flex-1">
          <div className="font-medium">{node.title}</div>
          {node.description && (
            <div className="text-sm text-gray-600 mt-1">{node.description}</div>
          )}
          {node.objective && (
            <div className="text-xs text-blue-600 mt-1">
              目標: {node.objective.title}
            </div>
          )}
          {node._count && node._count.tasks > 0 && (
            <div className="text-xs text-gray-500 mt-1">
              タスク数: {node._count.tasks}
            </div>
          )}
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => onEdit(node)}>
            編集
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete(node.id)}
            className="text-red-600"
          >
            削除
          </Button>
        </div>
      </div>
      {isExpanded &&
        node.children &&
        node.children.length > 0 &&
        node.children.map((child: any) => (
          <TreeNode
            key={child.id}
            node={child}
            level={level + 1}
            onDelete={onDelete}
            onEdit={onEdit}
          />
        ))}
    </div>
  );
}

export default function StrategyPlannerPage() {
  const params = useParams();
  const workspaceId = params.id as string;
  const { data: nodes, isLoading } = useStrategyNodes(workspaceId);
  const { data: objectives } = useObjectives(workspaceId);
  const deleteStrategyNode = useDeleteStrategyNode(workspaceId);
  const [selectedObjectiveId, setSelectedObjectiveId] = useState<string>('');
  const [editingNode, setEditingNode] = useState<StrategyNode | null>(null);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);

  const filteredNodes = selectedObjectiveId
    ? nodes?.filter((node) => node.objectiveId === selectedObjectiveId)
    : nodes;

  const treeNodes = filteredNodes ? buildTree(filteredNodes) : [];

  const handleDelete = (id: string) => {
    if (confirm('このノードを削除しますか？子ノードもすべて削除されます。')) {
      deleteStrategyNode.mutate(id);
    }
  };

  const handleEdit = (node: StrategyNode) => {
    setEditingNode(node);
    setIsEditDialogOpen(true);
  };

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
                <h1 className="text-xl font-bold text-gray-900">戦略プランナー</h1>
              </div>
            </div>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>戦略プランナー</CardTitle>
                  <CardDescription>
                    目標達成のための戦略やイニシアチブをツリー構造で管理
                  </CardDescription>
                </div>
                <CreateStrategyNodeDialog
                  workspaceId={workspaceId}
                  objectives={objectives}
                />
              </div>
            </CardHeader>
            <CardContent>
              {objectives && objectives.length > 0 && (
                <div className="mb-4">
                  <label className="text-sm font-medium mb-2 block">目標でフィルター</label>
                  <select
                    value={selectedObjectiveId}
                    onChange={(e) => setSelectedObjectiveId(e.target.value)}
                    className="w-full max-w-xs rounded-md border border-input bg-background px-3 py-2 text-sm"
                  >
                    <option value="">すべての目標</option>
                    {objectives.map((obj) => (
                      <option key={obj.id} value={obj.id}>
                        {obj.title}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {isLoading ? (
                <p className="text-gray-600">読み込み中...</p>
              ) : treeNodes.length > 0 ? (
                <div className="space-y-2">
                  {treeNodes.map((node) => (
                    <TreeNode
                      key={node.id}
                      node={node}
                      onDelete={handleDelete}
                      onEdit={handleEdit}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-600">
                  <p>戦略ノードがありません</p>
                  <div className="mt-4">
                    <CreateStrategyNodeDialog
                      workspaceId={workspaceId}
                      objectives={objectives}
                    />
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </main>
        <EditStrategyNodeDialog
          workspaceId={workspaceId}
          node={editingNode}
          open={isEditDialogOpen}
          onOpenChange={setIsEditDialogOpen}
          objectives={objectives}
        />
      </div>
    </AuthGuard>
  );
}

