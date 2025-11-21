import {
  Injectable,
  NotFoundException,
  ForbiddenException,
  BadRequestException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateObjectiveDto } from './dto/create-objective.dto';
import { UpdateObjectiveDto } from './dto/update-objective.dto';

@Injectable()
export class ObjectivesService {
  constructor(private prisma: PrismaService) {}

  // Key Resultsの進捗率を計算
  private calculateProgress(keyResults: any[]): number {
    if (!keyResults || keyResults.length === 0) return 0;

    const totalProgress = keyResults.reduce((sum, kr) => {
      if (kr.target === 0) return sum;
      const progress = Math.min((kr.current / kr.target) * 100, 100);
      return sum + progress;
    }, 0);

    return Math.round(totalProgress / keyResults.length);
  }

  async create(workspaceId: string, userId: string, createObjectiveDto: CreateObjectiveDto) {
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

    // 親目標が存在し、同じワークスペースに属しているかチェック
    if (createObjectiveDto.parentId) {
      const parent = await this.prisma.objective.findUnique({
        where: { id: createObjectiveDto.parentId },
      });

      if (!parent) {
        throw new NotFoundException('親目標が見つかりません');
      }

      if (parent.workspaceId !== workspaceId) {
        throw new BadRequestException('親目標は同じワークスペースに属している必要があります');
      }
    }

    // 個人目標の場合、ownerIdを設定
    const ownerId = createObjectiveDto.ownerId || null;

    const objective = await this.prisma.objective.create({
      data: {
        workspaceId,
        ownerId,
        parentId: createObjectiveDto.parentId || null,
        title: createObjectiveDto.title,
        keyResults: createObjectiveDto.keyResults || [],
      },
      include: {
        owner: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
        parent: {
          select: {
            id: true,
            title: true,
          },
        },
        children: {
          select: {
            id: true,
            title: true,
          },
        },
        _count: {
          select: {
            strategyNodes: true,
          },
        },
      },
    });

    // 進捗率を計算して追加
    const progress = this.calculateProgress(objective.keyResults as any[]);

    return {
      ...objective,
      progress,
    };
  }

  async findAll(workspaceId: string, userId: string) {
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

    const objectives = await this.prisma.objective.findMany({
      where: {
        workspaceId,
      },
      include: {
        owner: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
        parent: {
          select: {
            id: true,
            title: true,
          },
        },
        children: {
          select: {
            id: true,
            title: true,
          },
        },
        _count: {
          select: {
            strategyNodes: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    // 各目標の進捗率を計算
    return objectives.map((obj) => ({
      ...obj,
      progress: this.calculateProgress(obj.keyResults as any[]),
    }));
  }

  async findOne(id: string, userId: string) {
    const objective = await this.prisma.objective.findUnique({
      where: { id },
      include: {
        workspace: {
          select: {
            id: true,
            name: true,
          },
        },
        owner: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
        parent: {
          select: {
            id: true,
            title: true,
          },
        },
        children: {
          include: {
            owner: {
              select: {
                id: true,
                email: true,
                name: true,
                avatarUrl: true,
              },
            },
          },
        },
        _count: {
          select: {
            strategyNodes: true,
          },
        },
      },
    });

    if (!objective) {
      throw new NotFoundException('目標が見つかりません');
    }

    // ワークスペースのメンバーかチェック
    const membership = await this.prisma.workspaceMember.findUnique({
      where: {
        workspaceId_userId: {
          workspaceId: objective.workspaceId,
          userId,
        },
      },
    });

    if (!membership) {
      throw new ForbiddenException('この目標にアクセスする権限がありません');
    }

    // 進捗率を計算して追加
    const progress = this.calculateProgress(objective.keyResults as any[]);

    return {
      ...objective,
      progress,
    };
  }

  async update(id: string, userId: string, updateObjectiveDto: UpdateObjectiveDto) {
    const objective = await this.findOne(id, userId);

    // 親目標の変更がある場合、検証
    if (updateObjectiveDto.parentId !== undefined) {
      if (updateObjectiveDto.parentId) {
        const parent = await this.prisma.objective.findUnique({
          where: { id: updateObjectiveDto.parentId },
        });

        if (!parent) {
          throw new NotFoundException('親目標が見つかりません');
        }

        if (parent.workspaceId !== objective.workspaceId) {
          throw new BadRequestException('親目標は同じワークスペースに属している必要があります');
        }

        // 循環参照を防ぐ（自分自身を親にできない）
        if (parent.id === id) {
          throw new BadRequestException('自分自身を親目標にすることはできません');
        }
      }
    }

    const updated = await this.prisma.objective.update({
      where: { id },
      data: {
        title: updateObjectiveDto.title,
        keyResults: updateObjectiveDto.keyResults,
        parentId: updateObjectiveDto.parentId,
      },
      include: {
        owner: {
          select: {
            id: true,
            email: true,
            name: true,
            avatarUrl: true,
          },
        },
        parent: {
          select: {
            id: true,
            title: true,
          },
        },
        children: {
          select: {
            id: true,
            title: true,
          },
        },
        _count: {
          select: {
            strategyNodes: true,
          },
        },
      },
    });

    // 進捗率を計算して追加
    const progress = this.calculateProgress(updated.keyResults as any[]);

    return {
      ...updated,
      progress,
    };
  }

  async remove(id: string, userId: string) {
    await this.findOne(id, userId); // 権限チェック

    await this.prisma.objective.delete({
      where: { id },
    });

    return { message: '目標を削除しました' };
  }
}

