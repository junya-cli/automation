import { Injectable, ForbiddenException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class DashboardService {
  constructor(private prisma: PrismaService) {}

  async getDashboardData(workspaceId: string, userId: string) {
    // ワークスペースのメンバーかチェック
    const membership = await this.prisma.workspaceMember.findUnique({
      where: {
        workspaceId_userId: {
          workspaceId,
          userId,
        },
      },
    });

    if (!membership) {
      throw new ForbiddenException('このワークスペースにアクセスする権限がありません');
    }

    // 目標の統計
    const objectives = await this.prisma.objective.findMany({
      where: { workspaceId },
      select: {
        id: true,
        title: true,
        keyResults: true,
        ownerId: true,
        createdAt: true,
      },
    });

    // 各目標の進捗率を計算
    const objectivesWithProgress = objectives.map((obj) => {
      const keyResults = obj.keyResults as Array<{
        name: string;
        current: number;
        target: number;
      }>;
      const progress =
        keyResults.length > 0
          ? Math.round(
              keyResults.reduce((sum, kr) => {
                if (kr.target === 0) return sum;
                const p = Math.min((kr.current / kr.target) * 100, 100);
                return sum + p;
              }, 0) / keyResults.length,
            )
          : 0;
      return {
        ...obj,
        progress,
      };
    });

    const averageProgress =
      objectivesWithProgress.length > 0
        ? Math.round(
            objectivesWithProgress.reduce((sum, obj) => sum + obj.progress, 0) /
              objectivesWithProgress.length,
          )
        : 0;

    // タスクの統計
    const tasks = await this.prisma.task.findMany({
      where: { workspaceId },
      select: {
        id: true,
        status: true,
        assigneeId: true,
        createdAt: true,
        dueDate: true,
      },
    });

    const taskStats = {
      total: tasks.length,
      todo: tasks.filter((t) => t.status === 'todo').length,
      inProgress: tasks.filter((t) => t.status === 'in_progress').length,
      done: tasks.filter((t) => t.status === 'done').length,
    };

    // 期限切れタスク
    const now = new Date();
    const overdueTasks = tasks.filter(
      (t) => t.dueDate && new Date(t.dueDate) < now && t.status !== 'done',
    ).length;

    // メンバー別のタスク数
    const memberTaskCounts = await this.prisma.task.groupBy({
      by: ['assigneeId'],
      where: {
        workspaceId,
        assigneeId: { not: null },
      },
      _count: {
        id: true,
      },
    });

    const members = await this.prisma.workspaceMember.findMany({
      where: { workspaceId },
      include: {
        user: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
      },
    });

    const memberStats = members.map((member) => {
      const taskCount = memberTaskCounts.find(
        (m) => m.assigneeId === member.userId,
      )?._count.id || 0;
      const doneCount = tasks.filter(
        (t) => t.assigneeId === member.userId && t.status === 'done',
      ).length;
      return {
        userId: member.userId,
        user: member.user,
        totalTasks: taskCount,
        completedTasks: doneCount,
        completionRate: taskCount > 0 ? Math.round((doneCount / taskCount) * 100) : 0,
      };
    });

    // 最近の活動（直近7日間）
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    const recentTasks = await this.prisma.task.findMany({
      where: {
        workspaceId,
        createdAt: {
          gte: sevenDaysAgo,
        },
      },
      select: {
        id: true,
        title: true,
        status: true,
        createdAt: true,
      },
      orderBy: {
        createdAt: 'desc',
      },
      take: 10,
    });

    // 戦略ノードの統計
    const strategyNodes = await this.prisma.strategyNode.findMany({
      where: { workspaceId },
      select: {
        id: true,
        _count: {
          select: {
            tasks: true,
          },
        },
      },
    });

    const strategyNodeStats = {
      total: strategyNodes.length,
      withTasks: strategyNodes.filter((n) => n._count.tasks > 0).length,
    };

    return {
      objectives: {
        total: objectives.length,
        averageProgress,
        byProgress: {
          high: objectivesWithProgress.filter((o) => o.progress >= 80).length,
          medium: objectivesWithProgress.filter(
            (o) => o.progress >= 50 && o.progress < 80,
          ).length,
          low: objectivesWithProgress.filter((o) => o.progress < 50).length,
        },
        list: objectivesWithProgress.slice(0, 5), // 上位5件
      },
      tasks: {
        ...taskStats,
        overdue: overdueTasks,
        completionRate:
          taskStats.total > 0
            ? Math.round((taskStats.done / taskStats.total) * 100)
            : 0,
      },
      members: memberStats,
      recentActivity: recentTasks,
      strategyNodes: strategyNodeStats,
    };
  }
}

