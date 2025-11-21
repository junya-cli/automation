import { IsString, IsOptional, IsInt, Min } from 'class-validator';

export class UpdateStrategyNodeDto {
  @IsString()
  @IsOptional()
  title?: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsString()
  @IsOptional()
  objectiveId?: string;

  @IsString()
  @IsOptional()
  parentId?: string;

  @IsInt()
  @Min(0)
  @IsOptional()
  order?: number;
}

