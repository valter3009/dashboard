import { apiClient } from './client'

export type TaskPriority = 'low' | 'medium' | 'high' | 'critical'
export type TaskStatus = 'new' | 'active' | 'on_hold' | 'done'
export type TaskType = 'task' | 'bug' | 'feature' | 'epic'

export interface Task {
  id: number
  project_id: number
  board_id: number
  column_id?: number
  title: string
  description?: string
  task_number: number
  priority: TaskPriority
  status: TaskStatus
  type: TaskType
  story_points?: number
  estimated_hours?: number
  actual_hours: number
  position: number
  start_date?: string
  due_date?: string
  completed_at?: string
  creator_id?: number
  parent_task_id?: number
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  project_id: number
  board_id: number
  column_id?: number
  title: string
  description?: string
  priority?: TaskPriority
  type?: TaskType
  story_points?: number
  estimated_hours?: number
  start_date?: string
  due_date?: string
  parent_task_id?: number
  assignee_ids?: number[]
}

export interface TaskUpdate {
  title?: string
  description?: string
  priority?: TaskPriority
  status?: TaskStatus
  type?: TaskType
  story_points?: number
  estimated_hours?: number
  start_date?: string
  due_date?: string
  column_id?: number
  position?: number
}

export interface TaskFilters {
  project_id?: number
  board_id?: number
  column_id?: number
  status?: TaskStatus
  priority?: TaskPriority
  assignee_id?: number
}

export const tasksApi = {
  getTasks: async (filters?: TaskFilters): Promise<Task[]> => {
    const params = new URLSearchParams()
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, String(value))
        }
      })
    }
    const response = await apiClient.get(`/tasks${params.toString() ? `?${params}` : ''}`)
    return response.data
  },

  getTask: async (taskId: number): Promise<Task> => {
    const response = await apiClient.get(`/tasks/${taskId}`)
    return response.data
  },

  createTask: async (data: TaskCreate): Promise<Task> => {
    const response = await apiClient.post('/tasks/', data)
    return response.data
  },

  updateTask: async (taskId: number, data: TaskUpdate): Promise<Task> => {
    const response = await apiClient.patch(`/tasks/${taskId}`, data)
    return response.data
  },

  deleteTask: async (taskId: number): Promise<void> => {
    await apiClient.delete(`/tasks/${taskId}`)
  },
}
