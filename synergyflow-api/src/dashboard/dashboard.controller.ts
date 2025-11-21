import { Controller, Get, Param, UseGuards, Request } from '@nestjs/common';
import { DashboardService } from './dashboard.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('workspaces/:workspaceId/dashboard')
@UseGuards(JwtAuthGuard)
export class DashboardController {
  constructor(private readonly dashboardService: DashboardService) {}

  @Get()
  getDashboardData(@Param('workspaceId') workspaceId: string, @Request() req) {
    return this.dashboardService.getDashboardData(workspaceId, req.user.id);
  }
}

