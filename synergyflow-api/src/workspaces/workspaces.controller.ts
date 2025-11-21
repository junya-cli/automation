import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  UseGuards,
  Request,
} from '@nestjs/common';
import { WorkspacesService } from './workspaces.service';
import { CreateWorkspaceDto } from './dto/create-workspace.dto';
import { UpdateWorkspaceDto } from './dto/update-workspace.dto';
import { InviteMemberDto } from './dto/invite-member.dto';
import { UpdateMemberRoleDto } from './dto/update-member-role.dto';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('workspaces')
@UseGuards(JwtAuthGuard)
export class WorkspacesController {
  constructor(private readonly workspacesService: WorkspacesService) {}

  @Post()
  create(@Request() req, @Body() createWorkspaceDto: CreateWorkspaceDto) {
    return this.workspacesService.create(req.user.id, createWorkspaceDto);
  }

  @Get()
  findAll(@Request() req) {
    return this.workspacesService.findAll(req.user.id);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @Request() req) {
    return this.workspacesService.findOne(id, req.user.id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Request() req,
    @Body() updateWorkspaceDto: UpdateWorkspaceDto,
  ) {
    return this.workspacesService.update(id, req.user.id, updateWorkspaceDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string, @Request() req) {
    return this.workspacesService.remove(id, req.user.id);
  }

  @Post(':id/members')
  inviteMember(
    @Param('id') workspaceId: string,
    @Request() req,
    @Body() inviteMemberDto: InviteMemberDto,
  ) {
    return this.workspacesService.inviteMember(
      workspaceId,
      req.user.id,
      inviteMemberDto,
    );
  }

  @Patch(':id/members/:memberId/role')
  updateMemberRole(
    @Param('id') workspaceId: string,
    @Param('memberId') memberId: string,
    @Request() req,
    @Body() updateMemberRoleDto: UpdateMemberRoleDto,
  ) {
    return this.workspacesService.updateMemberRole(
      workspaceId,
      memberId,
      req.user.id,
      updateMemberRoleDto,
    );
  }

  @Delete(':id/members/:memberId')
  removeMember(
    @Param('id') workspaceId: string,
    @Param('memberId') memberId: string,
    @Request() req,
  ) {
    return this.workspacesService.removeMember(workspaceId, memberId, req.user.id);
  }
}

