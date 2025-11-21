import { IsString, IsOptional, IsDateString } from 'class-validator';

export class UpdateTaskDto {
  @IsString()
  @IsOptional()
  title?: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsString()
  @IsOptional()
  strategyNodeId?: string;

  @IsString()
  @IsOptional()
  assigneeId?: string;

  @IsString()
  @IsOptional()
  status?: string; // todo, in_progress, done

  @IsDateString()
  @IsOptional()
  dueDate?: string;
}

