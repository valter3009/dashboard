import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { Plus, Kanban } from 'lucide-react'
import { Button } from '../components/ui/Button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card'
import { Input } from '../components/ui/Input'
import { Label } from '../components/ui/Label'
import { projectsApi } from '../api/projects'
import { formatDate } from '../lib/utils'

export default function ProjectsPage() {
  const navigate = useNavigate()
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    name: '',
    key: '',
    description: '',
  })

  const queryClient = useQueryClient()

  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: projectsApi.getProjects,
  })

  const { data: organizations } = useQuery({
    queryKey: ['organizations'],
    queryFn: projectsApi.getOrganizations,
  })

  const createProjectMutation = useMutation({
    mutationFn: projectsApi.createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setShowCreateForm(false)
      setFormData({ name: '', key: '', description: '' })
      setError('')
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Не удалось создать проект')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!organizations || organizations.length === 0) {
      alert('Ошибка: У вас нет организации. Пожалуйста, обратитесь к администратору.')
      return
    }
    createProjectMutation.mutate({
      ...formData,
      organization_id: organizations[0].id,
    })
  }

  if (isLoading) {
    return <div>Загрузка...</div>
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Проекты</h1>
          <p className="text-gray-500 mt-2">Управляйте вашими проектами и командами</p>
        </div>
        <Button onClick={() => setShowCreateForm(!showCreateForm)}>
          <Plus className="h-4 w-4 mr-2" />
          Новый проект
        </Button>
      </div>

      {showCreateForm && (
        <Card>
          <CardHeader>
            <CardTitle>Создать новый проект</CardTitle>
            <CardDescription>Добавьте новый проект в рабочее пространство</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Название проекта</Label>
                  <Input
                    id="name"
                    placeholder="Мой проект"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="key">Ключ проекта</Label>
                  <Input
                    id="key"
                    placeholder="МП"
                    value={formData.key}
                    onChange={(e) =>
                      setFormData({ ...formData, key: e.target.value.toUpperCase() })
                    }
                    required
                    maxLength={10}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="description">Описание</Label>
                <Input
                  id="description"
                  placeholder="Описание проекта"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>
              <div className="flex space-x-2">
                <Button type="submit" disabled={createProjectMutation.isPending}>
                  {createProjectMutation.isPending ? 'Создание...' : 'Создать проект'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowCreateForm(false)}
                >
                  Отмена
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Projects Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {projects && projects.length > 0 ? (
          projects.map((project) => (
            <Card key={project.id} className="hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle>{project.name}</CardTitle>
                    <CardDescription className="mt-1">{project.key}</CardDescription>
                  </div>
                  <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                    {project.status}
                  </span>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-gray-600 line-clamp-2">
                  {project.description || 'Нет описания'}
                </p>
                <p className="text-xs text-gray-400">
                  Создан {formatDate(project.created_at)}
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full mt-2"
                  onClick={() => navigate(`/projects/${project.id}/boards`)}
                >
                  <Kanban className="h-4 w-4 mr-2" />
                  Открыть доски
                </Button>
              </CardContent>
            </Card>
          ))
        ) : (
          <Card className="col-span-full">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <h3 className="text-lg font-medium text-gray-900">Пока нет проектов</h3>
              <p className="text-sm text-gray-500 mt-2">
                Начните с создания вашего первого проекта
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
