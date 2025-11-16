import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Plus } from 'lucide-react'
import { Button } from '../components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Input } from '../components/ui/Input'
import { Label } from '../components/ui/Label'
import { boardsApi } from '../api/boards'

export default function BoardViewPage() {
  const { boardId } = useParams<{ boardId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  
  const [showColumnForm, setShowColumnForm] = useState(false)
  const [newColumnName, setNewColumnName] = useState('')

  const { data: board, isLoading } = useQuery({
    queryKey: ['board', boardId],
    queryFn: () => boardsApi.getBoard(Number(boardId)),
    enabled: !!boardId,
  })

  const createColumnMutation = useMutation({
    mutationFn: boardsApi.createColumn,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['board', boardId] })
      setShowColumnForm(false)
      setNewColumnName('')
    },
  })

  const handleCreateColumn = (e: React.FormEvent) => {
    e.preventDefault()
    if (boardId && newColumnName) {
      const maxPosition = board?.columns.length || 0
      createColumnMutation.mutate({
        name: newColumnName,
        position: maxPosition,
        board_id: Number(boardId),
      })
    }
  }

  if (isLoading) {
    return <div>Загрузка...</div>
  }

  if (!board) {
    return <div>Доска не найдена</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(-1)}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Назад
          </Button>
          <div>
            <h1 className="text-3xl font-bold">{board.name}</h1>
            {board.description && (
              <p className="text-gray-500 mt-1">{board.description}</p>
            )}
          </div>
        </div>
      </div>

      {/* Kanban Board */}
      <div className="flex space-x-4 overflow-x-auto pb-4">
        {/* Columns */}
        {board.columns.map((column) => (
          <div
            key={column.id}
            className="flex-shrink-0 w-80"
          >
            <Card>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base">{column.name}</CardTitle>
                  {column.wip_limit && (
                    <span className="text-xs text-gray-500">
                      Лимит: {column.wip_limit}
                    </span>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Tasks will go here */}
                <div className="text-sm text-gray-400 text-center py-8">
                  Пока нет задач
                </div>
                
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Добавить задачу
                </Button>
              </CardContent>
            </Card>
          </div>
        ))}

        {/* Add Column Button */}
        <div className="flex-shrink-0 w-80">
          {showColumnForm ? (
            <Card>
              <CardContent className="pt-6">
                <form onSubmit={handleCreateColumn} className="space-y-3">
                  <div className="space-y-2">
                    <Label htmlFor="columnName">Название колонки</Label>
                    <Input
                      id="columnName"
                      placeholder="Новая колонка"
                      value={newColumnName}
                      onChange={(e) => setNewColumnName(e.target.value)}
                      required
                      autoFocus
                    />
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      type="submit"
                      size="sm"
                      disabled={createColumnMutation.isPending}
                    >
                      Добавить
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowColumnForm(false)}
                    >
                      Отмена
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          ) : (
            <Button
              variant="outline"
              className="w-full h-full min-h-[100px]"
              onClick={() => setShowColumnForm(true)}
            >
              <Plus className="h-5 w-5 mr-2" />
              Добавить колонку
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
