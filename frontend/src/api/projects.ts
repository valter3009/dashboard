import { apiClient } from './client'
import { Project, Organization } from '../types'

export const projectsApi = {
  // Organizations
  getOrganizations: async (): Promise<Organization[]> => {
    const response = await apiClient.get<Organization[]>('/organizations')
    return response.data
  },

  createOrganization: async (data: { name: string; description?: string }): Promise<Organization> => {
    const response = await apiClient.post<Organization>('/organizations', data)
    return response.data
  },

  // Projects
  getProjects: async (): Promise<Project[]> => {
    const response = await apiClient.get<Project[]>('/projects')
    return response.data
  },

  getProject: async (id: number): Promise<Project> => {
    const response = await apiClient.get<Project>(`/projects/${id}`)
    return response.data
  },

  createProject: async (data: {
    name: string
    key: string
    organization_id: number
    description?: string
  }): Promise<Project> => {
    const response = await apiClient.post<Project>('/projects', data)
    return response.data
  },

  updateProject: async (id: number, data: Partial<Project>): Promise<Project> => {
    const response = await apiClient.put<Project>(`/projects/${id}`, data)
    return response.data
  },

  deleteProject: async (id: number): Promise<void> => {
    await apiClient.delete(`/projects/${id}`)
  },
}
