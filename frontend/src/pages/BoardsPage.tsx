import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import { Plus, ArrowLeft, Kanban } from 'lucide-react'
import { Button } from '../components/ui/Button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card'
import { Input } from '../components/ui/Input'
import { Label } from '../components/ui/Label'
import { boardsApi } from '../api/boards'

export default function BoardsPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  })

  const { data: boards, isLoading } = useQuery({
    queryKey: ['boards', projectId],
    queryFn: () => boardsApi.getProjectBoards(Number(projectId)),
    enabled: !!projectId,
  })

  const createBoardMutation = useMutation({
    mutationFn: boardsApi.createBoard,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['boards', projectId] })
      setShowCreateForm(false)
      setFormData({ name: '', description: '' })
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (projectId) {
      createBoardMutation.mutate({
        ...formData,
        project_id: Number(projectId),
      })
    }
  }

  if (isLoading) {
    return <div>Загрузка...</div>
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/projects')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Назад к проектам
          </Button>
        </div>
      </div>

      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Доски</h1>
          <p className="text-gray-500 mt-2">Управляйте досками Kanban</p>
        </div>
        <Button onClick={() => setShowCreateForm(!showCreateForm)}>
          <Plus className="h-4 w-4 mr-2" />
          Новая доска
        </Button>
      </div>

      {showCreateForm && (
        <Card>
          <CardHeader>
            <CardTitle>Создать новую доску</CardTitle>
            <CardDescription>Добавьте доску для управления задачами</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Название доски</Label>
                <Input
                  id="name"
                  placeholder="Спринт 1"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="description">Описание</Label>
                <Input
                  id="description"
                  placeholder="Описание доски"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>
              <div className="flex space-x-2">
                <Button type="submit" disabled={createBoardMutation.isPending}>
                  {createBoardMutation.isPending ? 'Создание...' : 'Создать доску'}
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

      {/* Boards Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {boards && boards.length > 0 ? (
          boards.map((board) => (
            <Card
              key={board.id}
              className="hover:shadow-md transition-shadow cursor-pointer"
              onClick={() => navigate(`/boards/${board.id}`)}
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2">
                    <Kanban className="h-5 w-5 text-primary" />
                    <CardTitle>{board.name}</CardTitle>
                  </div>
                  {board.is_default && (
                    <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                      По умолчанию
                    </span>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 line-clamp-2">
                  {board.description || 'Нет описания'}
                </p>
              </CardContent>
            </Card>
          ))
        ) : (
          <Card className="col-span-full">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <h3 className="text-lg font-medium text-gray-900">Пока нет досок</h3>
              <p className="text-sm text-gray-500 mt-2">
                Создайте доску для начала работы с задачами
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
