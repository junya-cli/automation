import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  Query,
  UseGuards,
  Request,
} from '@nestjs/common';
import { StrategyNodesService } from './strategy-nodes.service';
import { CreateStrategyNodeDto } from './dto/create-strategy-node.dto';
import { UpdateStrategyNodeDto } from './dto/update-strategy-node.dto';
import { ReorderNodesDto } from './dto/reorder-nodes.dto';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('workspaces/:workspaceId/strategy-nodes')
@UseGuards(JwtAuthGuard)
export class StrategyNodesController {
  constructor(private readonly strategyNodesService: StrategyNodesService) {}

  @Post()
  create(
    @Param('workspaceId') workspaceId: string,
    @Request() req,
    @Body() createStrategyNodeDto: CreateStrategyNodeDto,
  ) {
    return this.strategyNodesService.create(workspaceId, req.user.id, createStrategyNodeDto);
  }

  @Get()
  findAll(
    @Param('workspaceId') workspaceId: string,
    @Request() req,
    @Query('objectiveId') objectiveId?: string,
  ) {
    return this.strategyNodesService.findAll(workspaceId, req.user.id, objectiveId);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @Request() req) {
    return this.strategyNodesService.findOne(id, req.user.id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Request() req,
    @Body() updateStrategyNodeDto: UpdateStrategyNodeDto,
  ) {
    return this.strategyNodesService.update(id, req.user.id, updateStrategyNodeDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string, @Request() req) {
    return this.strategyNodesService.remove(id, req.user.id);
  }

  @Post('reorder')
  reorder(
    @Param('workspaceId') workspaceId: string,
    @Request() req,
    @Body() reorderNodesDto: ReorderNodesDto,
  ) {
    return this.strategyNodesService.reorder(workspaceId, req.user.id, reorderNodesDto);
  }
}

