import { IsArray, ValidateNested, IsString, IsInt, Min } from 'class-validator';
import { Type } from 'class-transformer';

class NodeOrder {
  @IsString()
  id: string;

  @IsInt()
  @Min(0)
  order: number;

  @IsString()
  @IsOptional()
  parentId?: string;
}

export class ReorderNodesDto {
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => NodeOrder)
  nodes: NodeOrder[];
}

