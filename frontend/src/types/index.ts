export interface User {
  id: number
  email: string
  username: string
  first_name?: string
  last_name?: string
  avatar_url?: string
  is_active: boolean
  is_verified: boolean
  timezone: string
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  first_name?: string
  last_name?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface Organization {
  id: number
  name: string
  description?: string
  logo_url?: string
  owner_id: number
  created_at: string
  updated_at: string
}

export interface Project {
  id: number
  organization_id: number
  name: string
  key: string
  description?: string
  status: 'active' | 'archived' | 'on_hold'
  start_date?: string
  end_date?: string
  budget?: number
  owner_id?: number
  created_at: string
  updated_at: string
}

export interface Board {
  id: number
  project_id: number
  name: string
  description?: string
  position: number
  created_at: string
  updated_at: string
}

export interface Task {
  id: number
  project_id: number
  board_id: number
  column_id?: number
  title: string
  description?: string
  task_number: number
  priority: 'low' | 'medium' | 'high' | 'critical'
  status: 'new' | 'active' | 'on_hold' | 'done'
  type: 'task' | 'bug' | 'feature' | 'epic'
  story_points?: number
  estimated_hours?: number
  actual_hours: number
  start_date?: string
  due_date?: string
  completed_at?: string
  position: number
  creator_id?: number
  created_at: string
  updated_at: string
}
