import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Plus, X } from 'lucide-react'
import { Button } from '../components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Input } from '../components/ui/Input'
import { Label } from '../components/ui/Label'
import { boardsApi } from '../api/boards'
import { tasksApi, Task } from '../api/tasks'

export default function BoardViewPage() {
  const { boardId } = useParams<{ boardId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const [showColumnForm, setShowColumnForm] = useState(false)
  const [newColumnName, setNewColumnName] = useState('')
  const [showTaskForm, setShowTaskForm] = useState<number | null>(null) // column_id
  const [newTaskTitle, setNewTaskTitle] = useState('')

  const { data: board, isLoading } = useQuery({
    queryKey: ['board', boardId],
    queryFn: () => boardsApi.getBoard(Number(boardId)),
    enabled: !!boardId,
  })

  const { data: tasks = [] } = useQuery({
    queryKey: ['tasks', boardId],
    queryFn: () => tasksApi.getTasks({ board_id: Number(boardId) }),
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

  const createTaskMutation = useMutation({
    mutationFn: tasksApi.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', boardId] })
      setShowTaskForm(null)
      setNewTaskTitle('')
    },
  })

  const deleteTaskMutation = useMutation({
    mutationFn: tasksApi.deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', boardId] })
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

  const handleCreateTask = (e: React.FormEvent, columnId: number) => {
    e.preventDefault()
    if (board && newTaskTitle) {
      createTaskMutation.mutate({
        project_id: board.project_id,
        board_id: Number(boardId),
        column_id: columnId,
        title: newTaskTitle,
      })
    }
  }

  const getColumnTasks = (columnId: number): Task[] => {
    return tasks.filter(task => task.column_id === columnId)
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
                {/* Tasks */}
                {getColumnTasks(column.id).map((task) => (
                  <Card key={task.id} className="hover:shadow-sm transition-shadow cursor-pointer group">
                    <CardContent className="p-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="text-sm font-medium">{task.title}</p>
                          <div className="flex items-center gap-2 mt-2">
                            <span className={`text-xs px-2 py-0.5 rounded ${
                              task.priority === 'critical' ? 'bg-red-100 text-red-700' :
                              task.priority === 'high' ? 'bg-orange-100 text-orange-700' :
                              task.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-gray-100 text-gray-700'
                            }`}>
                              {task.priority === 'critical' ? 'Критично' :
                               task.priority === 'high' ? 'Высокий' :
                               task.priority === 'medium' ? 'Средний' : 'Низкий'}
                            </span>
                            {task.type === 'bug' && (
                              <span className="text-xs px-2 py-0.5 rounded bg-red-50 text-red-600">
                                Баг
                              </span>
                            )}
                            {task.type === 'feature' && (
                              <span className="text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-600">
                                Фича
                              </span>
                            )}
                          </div>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            if (confirm('Удалить задачу?')) {
                              deleteTaskMutation.mutate(task.id)
                            }
                          }}
                          className="opacity-0 group-hover:opacity-100 transition-opacity ml-2"
                        >
                          <X className="h-4 w-4 text-gray-400 hover:text-red-600" />
                        </button>
                      </div>
                    </CardContent>
                  </Card>
                ))}

                {getColumnTasks(column.id).length === 0 && showTaskForm !== column.id && (
                  <div className="text-sm text-gray-400 text-center py-4">
                    Пока нет задач
                  </div>
                )}

                {/* Add Task Form */}
                {showTaskForm === column.id ? (
                  <form onSubmit={(e) => handleCreateTask(e, column.id)} className="space-y-2">
                    <Input
                      placeholder="Название задачи"
                      value={newTaskTitle}
                      onChange={(e) => setNewTaskTitle(e.target.value)}
                      required
                      autoFocus
                    />
                    <div className="flex space-x-2">
                      <Button type="submit" size="sm" disabled={createTaskMutation.isPending}>
                        Добавить
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setShowTaskForm(null)
                          setNewTaskTitle('')
                        }}
                      >
                        Отмена
                      </Button>
                    </div>
                  </form>
                ) : (
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full"
                    onClick={() => setShowTaskForm(column.id)}
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Добавить задачу
                  </Button>
                )}
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
