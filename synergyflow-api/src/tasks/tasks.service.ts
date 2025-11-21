import {
  Injectable,
  NotFoundException,
  ForbiddenException,
  BadRequestException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateTaskDto } from './dto/create-task.dto';
import { UpdateTaskDto } from './dto/update-task.dto';

@Injectable()
export class TasksService {
  constructor(private prisma: PrismaService) {}

  async create(workspaceId: string, userId: string, createTaskDto: CreateTaskDto) {
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

    // 戦略ノードが指定されている場合、同じワークスペースに属しているかチェック
    if (createTaskDto.strategyNodeId) {
      const strategyNode = await this.prisma.strategyNode.findUnique({
        where: { id: createTaskDto.strategyNodeId },
      });

      if (!strategyNode) {
        throw new NotFoundException('戦略ノードが見つかりません');
      }

      if (strategyNode.workspaceId !== workspaceId) {
        throw new BadRequestException('戦略ノードは同じワークスペースに属している必要があります');
      }
    }

    // 担当者が指定されている場合、同じワークスペースのメンバーかチェック
    if (createTaskDto.assigneeId) {
      const assigneeMembership = await this.prisma.workspaceMember.findUnique({
        where: {
          workspaceId_userId: {
            workspaceId,
            userId: createTaskDto.assigneeId,
          },
        },
      });

      if (!assigneeMembership) {
        throw new BadRequestException('担当者は同じワークスペースのメンバーである必要があります');
      }
    }

    const task = await this.prisma.task.create({
      data: {
        workspaceId,
        strategyNodeId: createTaskDto.strategyNodeId || null,
        assigneeId: createTaskDto.assigneeId || null,
        title: createTaskDto.title,
        description: createTaskDto.description || null,
        status: createTaskDto.status || 'todo',
        dueDate: createTaskDto.dueDate ? new Date(createTaskDto.dueDate) : null,
      },
      include: {
        assignee: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
        strategyNode: {
          select: {
            id: true,
            title: true,
          },
        },
      },
    });

    return task;
  }

  async findAll(workspaceId: string, userId: string, strategyNodeId?: string) {
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

    const where: any = { workspaceId };
    if (strategyNodeId) {
      where.strategyNodeId = strategyNodeId;
    }

    const tasks = await this.prisma.task.findMany({
      where,
      include: {
        assignee: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
        strategyNode: {
          select: {
            id: true,
            title: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    return tasks;
  }

  async findOne(id: string, userId: string) {
    const task = await this.prisma.task.findUnique({
      where: { id },
      include: {
        workspace: {
          select: {
            id: true,
            name: true,
          },
        },
        assignee: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
        strategyNode: {
          select: {
            id: true,
            title: true,
          },
        },
      },
    });

    if (!task) {
      throw new NotFoundException('タスクが見つかりません');
    }

    // ワークスペースのメンバーかチェック
    const membership = await this.prisma.workspaceMember.findUnique({
      where: {
        workspaceId_userId: {
          workspaceId: task.workspaceId,
          userId,
        },
      },
    });

    if (!membership) {
      throw new ForbiddenException('このタスクにアクセスする権限がありません');
    }

    return task;
  }

  async update(id: string, userId: string, updateTaskDto: UpdateTaskDto) {
    const task = await this.findOne(id, userId);

    // 戦略ノードの変更がある場合、検証
    if (updateTaskDto.strategyNodeId !== undefined) {
      if (updateTaskDto.strategyNodeId) {
        const strategyNode = await this.prisma.strategyNode.findUnique({
          where: { id: updateTaskDto.strategyNodeId },
        });

        if (!strategyNode) {
          throw new NotFoundException('戦略ノードが見つかりません');
        }

        if (strategyNode.workspaceId !== task.workspaceId) {
          throw new BadRequestException('戦略ノードは同じワークスペースに属している必要があります');
        }
      }
    }

    // 担当者の変更がある場合、検証
    if (updateTaskDto.assigneeId !== undefined) {
      if (updateTaskDto.assigneeId) {
        const assigneeMembership = await this.prisma.workspaceMember.findUnique({
          where: {
            workspaceId_userId: {
              workspaceId: task.workspaceId,
              userId: updateTaskDto.assigneeId,
            },
          },
        });

        if (!assigneeMembership) {
          throw new BadRequestException('担当者は同じワークスペースのメンバーである必要があります');
        }
      }
    }

    const updated = await this.prisma.task.update({
      where: { id },
      data: {
        title: updateTaskDto.title,
        description: updateTaskDto.description,
        strategyNodeId: updateTaskDto.strategyNodeId,
        assigneeId: updateTaskDto.assigneeId,
        status: updateTaskDto.status,
        dueDate: updateTaskDto.dueDate ? new Date(updateTaskDto.dueDate) : undefined,
      },
      include: {
        assignee: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
        strategyNode: {
          select: {
            id: true,
            title: true,
          },
        },
      },
    });

    return updated;
  }

  async remove(id: string, userId: string) {
    await this.findOne(id, userId); // 権限チェック

    await this.prisma.task.delete({
      where: { id },
    });

    return { message: 'タスクを削除しました' };
  }
}

