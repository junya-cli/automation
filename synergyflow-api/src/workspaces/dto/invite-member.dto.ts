import { IsEmail, IsNotEmpty, IsString, IsOptional } from 'class-validator';

export class InviteMemberDto {
  @IsEmail()
  @IsNotEmpty()
  email: string;

  @IsString()
  @IsOptional()
  role?: string; // admin or member
}

