import { IsNotEmpty, IsString, IsOptional, IsArray, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';
import { KeyResultDto } from './key-result.dto';

export class CreateObjectiveDto {
  @IsString()
  @IsNotEmpty()
  title: string;

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => KeyResultDto)
  keyResults: KeyResultDto[];

  @IsString()
  @IsOptional()
  parentId?: string;

  @IsString()
  @IsOptional()
  ownerId?: string; // 個人目標の場合
}

