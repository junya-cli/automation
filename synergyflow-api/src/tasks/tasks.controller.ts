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
import { TasksService } from './tasks.service';
import { CreateTaskDto } from './dto/create-task.dto';
import { UpdateTaskDto } from './dto/update-task.dto';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('workspaces/:workspaceId/tasks')
@UseGuards(JwtAuthGuard)
export class TasksController {
  constructor(private readonly tasksService: TasksService) {}

  @Post()
  create(
    @Param('workspaceId') workspaceId: string,
    @Request() req,
    @Body() createTaskDto: CreateTaskDto,
  ) {
    return this.tasksService.create(workspaceId, req.user.id, createTaskDto);
  }

  @Get()
  findAll(
    @Param('workspaceId') workspaceId: string,
    @Request() req,
    @Query('strategyNodeId') strategyNodeId?: string,
  ) {
    return this.tasksService.findAll(workspaceId, req.user.id, strategyNodeId);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @Request() req) {
    return this.tasksService.findOne(id, req.user.id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Request() req,
    @Body() updateTaskDto: UpdateTaskDto,
  ) {
    return this.tasksService.update(id, req.user.id, updateTaskDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string, @Request() req) {
    return this.tasksService.remove(id, req.user.id);
  }
}

