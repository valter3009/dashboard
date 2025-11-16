import { create } from 'zustand'
import { User } from '../types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  setUser: (user: User | null) => void
  setTokens: (accessToken: string, refreshToken: string) => void
  clearAuth: () => void
  initAuth: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  setUser: (user) => set({ user, isAuthenticated: !!user }),

  setTokens: (accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
    set({ isAuthenticated: true })
  },

  clearAuth: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({ user: null, isAuthenticated: false })
  },

  initAuth: () => {
    const token = localStorage.getItem('access_token')
    set({ isAuthenticated: !!token })
  },
}))
