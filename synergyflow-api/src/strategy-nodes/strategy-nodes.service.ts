import {
  Injectable,
  NotFoundException,
  ForbiddenException,
  BadRequestException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateStrategyNodeDto } from './dto/create-strategy-node.dto';
import { UpdateStrategyNodeDto } from './dto/update-strategy-node.dto';
import { ReorderNodesDto } from './dto/reorder-nodes.dto';

@Injectable()
export class StrategyNodesService {
  constructor(private prisma: PrismaService) {}

  async create(
    workspaceId: string,
    userId: string,
    createStrategyNodeDto: CreateStrategyNodeDto,
  ) {
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

    // 目標が指定されている場合、同じワークスペースに属しているかチェック
    if (createStrategyNodeDto.objectiveId) {
      const objective = await this.prisma.objective.findUnique({
        where: { id: createStrategyNodeDto.objectiveId },
      });

      if (!objective) {
        throw new NotFoundException('目標が見つかりません');
      }

      if (objective.workspaceId !== workspaceId) {
        throw new BadRequestException('目標は同じワークスペースに属している必要があります');
      }
    }

    // 親ノードが指定されている場合、同じワークスペースに属しているかチェック
    if (createStrategyNodeDto.parentId) {
      const parent = await this.prisma.strategyNode.findUnique({
        where: { id: createStrategyNodeDto.parentId },
      });

      if (!parent) {
        throw new NotFoundException('親ノードが見つかりません');
      }

      if (parent.workspaceId !== workspaceId) {
        throw new BadRequestException('親ノードは同じワークスペースに属している必要があります');
      }
    }

    // orderが指定されていない場合、最大値を取得して+1
    let order = createStrategyNodeDto.order;
    if (order === undefined) {
      const maxOrder = await this.prisma.strategyNode.findFirst({
        where: {
          workspaceId,
          parentId: createStrategyNodeDto.parentId || null,
        },
        orderBy: { order: 'desc' },
        select: { order: true },
      });
      order = maxOrder ? maxOrder.order + 1 : 0;
    }

    const node = await this.prisma.strategyNode.create({
      data: {
        workspaceId,
        objectiveId: createStrategyNodeDto.objectiveId || null,
        parentId: createStrategyNodeDto.parentId || null,
        title: createStrategyNodeDto.title,
        description: createStrategyNodeDto.description || null,
        order,
      },
      include: {
        objective: {
          select: {
            id: true,
            title: true,
          },
        },
        parent: {
          select: {
            id: true,
            title: true,
          },
        },
        children: {
          orderBy: { order: 'asc' },
          select: {
            id: true,
            title: true,
            order: true,
          },
        },
        _count: {
          select: {
            tasks: true,
          },
        },
      },
    });

    return node;
  }

  async findAll(workspaceId: string, userId: string, objectiveId?: string) {
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
    if (objectiveId) {
      where.objectiveId = objectiveId;
    }

    const nodes = await this.prisma.strategyNode.findMany({
      where,
      include: {
        objective: {
          select: {
            id: true,
            title: true,
          },
        },
        parent: {
          select: {
            id: true,
            title: true,
          },
        },
        children: {
          orderBy: { order: 'asc' },
          select: {
            id: true,
            title: true,
            order: true,
          },
        },
        _count: {
          select: {
            tasks: true,
          },
        },
      },
      orderBy: { order: 'asc' },
    });

    return nodes;
  }

  async findOne(id: string, userId: string) {
    const node = await this.prisma.strategyNode.findUnique({
      where: { id },
      include: {
        workspace: {
          select: {
            id: true,
            name: true,
          },
        },
        objective: {
          select: {
            id: true,
            title: true,
          },
        },
        parent: {
          select: {
            id: true,
            title: true,
          },
        },
        children: {
          orderBy: { order: 'asc' },
          include: {
            _count: {
              select: {
                tasks: true,
              },
            },
          },
        },
        tasks: {
          select: {
            id: true,
            title: true,
            status: true,
            assigneeId: true,
          },
        },
      },
    });

    if (!node) {
      throw new NotFoundException('戦略ノードが見つかりません');
    }

    // ワークスペースのメンバーかチェック
    const membership = await this.prisma.workspaceMember.findUnique({
      where: {
        workspaceId_userId: {
          workspaceId: node.workspaceId,
          userId,
        },
      },
    });

    if (!membership) {
      throw new ForbiddenException('この戦略ノードにアクセスする権限がありません');
    }

    return node;
  }

  async update(id: string, userId: string, updateStrategyNodeDto: UpdateStrategyNodeDto) {
    const node = await this.findOne(id, userId);

    // 親ノードの変更がある場合、検証
    if (updateStrategyNodeDto.parentId !== undefined) {
      if (updateStrategyNodeDto.parentId) {
        const parent = await this.prisma.strategyNode.findUnique({
          where: { id: updateStrategyNodeDto.parentId },
        });

        if (!parent) {
          throw new NotFoundException('親ノードが見つかりません');
        }

        if (parent.workspaceId !== node.workspaceId) {
          throw new BadRequestException('親ノードは同じワークスペースに属している必要があります');
        }

        // 循環参照を防ぐ（自分自身を親にできない）
        if (parent.id === id) {
          throw new BadRequestException('自分自身を親ノードにすることはできません');
        }
      }
    }

    // 目標の変更がある場合、検証
    if (updateStrategyNodeDto.objectiveId !== undefined) {
      if (updateStrategyNodeDto.objectiveId) {
        const objective = await this.prisma.objective.findUnique({
          where: { id: updateStrategyNodeDto.objectiveId },
        });

        if (!objective) {
          throw new NotFoundException('目標が見つかりません');
        }

        if (objective.workspaceId !== node.workspaceId) {
          throw new BadRequestException('目標は同じワークスペースに属している必要があります');
        }
      }
    }

    const updated = await this.prisma.strategyNode.update({
      where: { id },
      data: {
        title: updateStrategyNodeDto.title,
        description: updateStrategyNodeDto.description,
        objectiveId: updateStrategyNodeDto.objectiveId,
        parentId: updateStrategyNodeDto.parentId,
        order: updateStrategyNodeDto.order,
      },
      include: {
        objective: {
          select: {
            id: true,
            title: true,
          },
        },
        parent: {
          select: {
            id: true,
            title: true,
          },
        },
        children: {
          orderBy: { order: 'asc' },
          select: {
            id: true,
            title: true,
            order: true,
          },
        },
        _count: {
          select: {
            tasks: true,
          },
        },
      },
    });

    return updated;
  }

  async remove(id: string, userId: string) {
    await this.findOne(id, userId); // 権限チェック

    await this.prisma.strategyNode.delete({
      where: { id },
    });

    return { message: '戦略ノードを削除しました' };
  }

  async reorder(workspaceId: string, userId: string, reorderNodesDto: ReorderNodesDto) {
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

    // すべてのノードが同じワークスペースに属しているかチェック
    const nodeIds = reorderNodesDto.nodes.map((n) => n.id);
    const nodes = await this.prisma.strategyNode.findMany({
      where: {
        id: { in: nodeIds },
      },
    });

    if (nodes.length !== nodeIds.length) {
      throw new NotFoundException('一部のノードが見つかりません');
    }

    const invalidNodes = nodes.filter((n) => n.workspaceId !== workspaceId);
    if (invalidNodes.length > 0) {
      throw new ForbiddenException('すべてのノードは同じワークスペースに属している必要があります');
    }

    // トランザクションで一括更新
    await this.prisma.$transaction(
      reorderNodesDto.nodes.map((nodeOrder) =>
        this.prisma.strategyNode.update({
          where: { id: nodeOrder.id },
          data: {
            order: nodeOrder.order,
            parentId: nodeOrder.parentId || null,
          },
        }),
      ),
    );

    return { message: 'ノードの並び順を更新しました' };
  }
}

