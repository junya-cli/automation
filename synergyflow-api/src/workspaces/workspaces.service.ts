import {
  Injectable,
  NotFoundException,
  ForbiddenException,
  ConflictException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateWorkspaceDto } from './dto/create-workspace.dto';
import { UpdateWorkspaceDto } from './dto/update-workspace.dto';
import { InviteMemberDto } from './dto/invite-member.dto';
import { UpdateMemberRoleDto } from './dto/update-member-role.dto';

@Injectable()
export class WorkspacesService {
  constructor(private prisma: PrismaService) {}

  async create(userId: string, createWorkspaceDto: CreateWorkspaceDto) {
    // ワークスペースを作成
    const workspace = await this.prisma.workspace.create({
      data: {
        name: createWorkspaceDto.name,
        coreMission: createWorkspaceDto.coreMission || null,
        members: {
          create: {
            userId,
            role: 'admin', // 作成者は自動的に管理者
          },
        },
      },
      include: {
        members: {
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
        },
      },
    });

    return workspace;
  }

  async findAll(userId: string) {
    // ユーザーが所属しているワークスペースを取得
    const workspaces = await this.prisma.workspace.findMany({
      where: {
        members: {
          some: {
            userId,
          },
        },
      },
      include: {
        members: {
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
        },
        _count: {
          select: {
            objectives: true,
            tasks: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    return workspaces;
  }

  async findOne(id: string, userId: string) {
    const workspace = await this.prisma.workspace.findUnique({
      where: { id },
      include: {
        members: {
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
        },
        _count: {
          select: {
            objectives: true,
            tasks: true,
            strategyNodes: true,
          },
        },
      },
    });

    if (!workspace) {
      throw new NotFoundException('ワークスペースが見つかりません');
    }

    // ユーザーがメンバーかチェック
    const isMember = workspace.members.some((m) => m.userId === userId);
    if (!isMember) {
      throw new ForbiddenException('このワークスペースにアクセスする権限がありません');
    }

    return workspace;
  }

  async update(id: string, userId: string, updateWorkspaceDto: UpdateWorkspaceDto) {
    // ワークスペースの存在確認と権限チェック
    const workspace = await this.findOne(id, userId);

    // 管理者のみ更新可能
    const member = workspace.members.find((m) => m.userId === userId);
    if (member?.role !== 'admin') {
      throw new ForbiddenException('ワークスペースを更新する権限がありません');
    }

    const updated = await this.prisma.workspace.update({
      where: { id },
      data: updateWorkspaceDto,
      include: {
        members: {
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
        },
      },
    });

    return updated;
  }

  async remove(id: string, userId: string) {
    // ワークスペースの存在確認と権限チェック
    const workspace = await this.findOne(id, userId);

    // 管理者のみ削除可能
    const member = workspace.members.find((m) => m.userId === userId);
    if (member?.role !== 'admin') {
      throw new ForbiddenException('ワークスペースを削除する権限がありません');
    }

    await this.prisma.workspace.delete({
      where: { id },
    });

    return { message: 'ワークスペースを削除しました' };
  }

  async inviteMember(
    workspaceId: string,
    userId: string,
    inviteMemberDto: InviteMemberDto,
  ) {
    // ワークスペースの存在確認と権限チェック
    const workspace = await this.findOne(workspaceId, userId);

    // 管理者のみ招待可能
    const member = workspace.members.find((m) => m.userId === userId);
    if (member?.role !== 'admin') {
      throw new ForbiddenException('メンバーを招待する権限がありません');
    }

    // ユーザーを検索
    const user = await this.prisma.user.findUnique({
      where: { email: inviteMemberDto.email },
    });

    if (!user) {
      throw new NotFoundException('このメールアドレスのユーザーが見つかりません');
    }

    // 既にメンバーかチェック
    const existingMember = await this.prisma.workspaceMember.findUnique({
      where: {
        workspaceId_userId: {
          workspaceId,
          userId: user.id,
        },
      },
    });

    if (existingMember) {
      throw new ConflictException('このユーザーは既にメンバーです');
    }

    // メンバーを追加
    const newMember = await this.prisma.workspaceMember.create({
      data: {
        workspaceId,
        userId: user.id,
        role: inviteMemberDto.role || 'member',
      },
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

    return newMember;
  }

  async updateMemberRole(
    workspaceId: string,
    memberId: string,
    userId: string,
    updateMemberRoleDto: UpdateMemberRoleDto,
  ) {
    // ワークスペースの存在確認と権限チェック
    const workspace = await this.findOne(workspaceId, userId);

    // 管理者のみロール変更可能
    const member = workspace.members.find((m) => m.userId === userId);
    if (member?.role !== 'admin') {
      throw new ForbiddenException('メンバーのロールを変更する権限がありません');
    }

    // メンバーを更新
    const updated = await this.prisma.workspaceMember.update({
      where: { id: memberId },
      data: { role: updateMemberRoleDto.role },
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

    return updated;
  }

  async removeMember(workspaceId: string, memberId: string, userId: string) {
    // ワークスペースの存在確認と権限チェック
    const workspace = await this.findOne(workspaceId, userId);

    // 管理者のみメンバー削除可能
    const member = workspace.members.find((m) => m.userId === userId);
    if (member?.role !== 'admin') {
      throw new ForbiddenException('メンバーを削除する権限がありません');
    }

    // 自分自身は削除できない
    const targetMember = workspace.members.find((m) => m.id === memberId);
    if (targetMember?.userId === userId) {
      throw new ForbiddenException('自分自身を削除することはできません');
    }

    await this.prisma.workspaceMember.delete({
      where: { id: memberId },
    });

    return { message: 'メンバーを削除しました' };
  }
}

