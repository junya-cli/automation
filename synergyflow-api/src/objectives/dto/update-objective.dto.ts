import { IsString, IsOptional, IsArray, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';
import { KeyResultDto } from './key-result.dto';

export class UpdateObjectiveDto {
  @IsString()
  @IsOptional()
  title?: string;

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => KeyResultDto)
  @IsOptional()
  keyResults?: KeyResultDto[];

  @IsString()
  @IsOptional()
  parentId?: string;
}

