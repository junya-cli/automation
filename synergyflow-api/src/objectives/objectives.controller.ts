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
import { ObjectivesService } from './objectives.service';
import { CreateObjectiveDto } from './dto/create-objective.dto';
import { UpdateObjectiveDto } from './dto/update-objective.dto';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('workspaces/:workspaceId/objectives')
@UseGuards(JwtAuthGuard)
export class ObjectivesController {
  constructor(private readonly objectivesService: ObjectivesService) {}

  @Post()
  create(
    @Param('workspaceId') workspaceId: string,
    @Request() req,
    @Body() createObjectiveDto: CreateObjectiveDto,
  ) {
    return this.objectivesService.create(workspaceId, req.user.id, createObjectiveDto);
  }

  @Get()
  findAll(@Param('workspaceId') workspaceId: string, @Request() req) {
    return this.objectivesService.findAll(workspaceId, req.user.id);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @Request() req) {
    return this.objectivesService.findOne(id, req.user.id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Request() req,
    @Body() updateObjectiveDto: UpdateObjectiveDto,
  ) {
    return this.objectivesService.update(id, req.user.id, updateObjectiveDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string, @Request() req) {
    return this.objectivesService.remove(id, req.user.id);
  }
}

