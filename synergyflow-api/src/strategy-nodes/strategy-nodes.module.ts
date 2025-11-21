import { Module } from '@nestjs/common';
import { StrategyNodesService } from './strategy-nodes.service';
import { StrategyNodesController } from './strategy-nodes.controller';

@Module({
  controllers: [StrategyNodesController],
  providers: [StrategyNodesService],
  exports: [StrategyNodesService],
})
export class StrategyNodesModule {}

