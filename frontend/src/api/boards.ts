import { apiClient } from './client'

export interface Board {
  id: number
  name: string
  description?: string
  project_id: number
  is_default: boolean
  created_at: string
  updated_at: string
}

export interface Column {
  id: number
  name: string
  position: number
  wip_limit?: number
  board_id: number
  created_at: string
  updated_at: string
}

export interface BoardWithColumns extends Board {
  columns: Column[]
}

export interface BoardCreate {
  name: string
  description?: string
  project_id: number
  is_default?: boolean
}

export interface ColumnCreate {
  name: string
  position: number
  board_id: number
  wip_limit?: number
}

export const boardsApi = {
  getProjectBoards: async (projectId: number): Promise<Board[]> => {
    const response = await apiClient.get(`/api/v1/boards/project/${projectId}`)
    return response.data
  },

  getBoard: async (boardId: number): Promise<BoardWithColumns> => {
    const response = await apiClient.get(`/api/v1/boards/${boardId}`)
    return response.data
  },

  createBoard: async (data: BoardCreate): Promise<Board> => {
    const response = await apiClient.post('/api/v1/boards/', data)
    return response.data
  },

  updateBoard: async (boardId: number, data: Partial<Board>): Promise<Board> => {
    const response = await apiClient.patch(`/api/v1/boards/${boardId}`, data)
    return response.data
  },

  deleteBoard: async (boardId: number): Promise<void> => {
    await apiClient.delete(`/api/v1/boards/${boardId}`)
  },

  createColumn: async (data: ColumnCreate): Promise<Column> => {
    const response = await apiClient.post('/api/v1/boards/columns', data)
    return response.data
  },

  updateColumn: async (columnId: number, data: Partial<Column>): Promise<Column> => {
    const response = await apiClient.patch(`/api/v1/boards/columns/${columnId}`, data)
    return response.data
  },

  deleteColumn: async (columnId: number): Promise<void> => {
    await apiClient.delete(`/api/v1/boards/columns/${columnId}`)
  },
}
