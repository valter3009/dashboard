import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card'
import { authApi } from '../api/auth'
import { useAuthStore } from '../store/authStore'
import { LayoutDashboard, FolderKanban, CheckSquare, Clock } from 'lucide-react'

export default function DashboardPage() {
  const { user, setUser } = useAuthStore()

  const { data: currentUser } = useQuery({
    queryKey: ['currentUser'],
    queryFn: authApi.getCurrentUser,
  })

  useEffect(() => {
    if (currentUser) {
      setUser(currentUser)
    }
  }, [currentUser, setUser])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Панель управления</h1>
        <p className="text-gray-500 mt-2">
          С возвращением, {user?.first_name || user?.username}!
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Всего проектов</CardTitle>
            <FolderKanban className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">Пока нет проектов</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Активные задачи</CardTitle>
            <CheckSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">Назначено вам</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Завершено</CardTitle>
            <CheckSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">На этой неделе</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Отслежено времени</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0ч</div>
            <p className="text-xs text-muted-foreground">На этой неделе</p>
          </CardContent>
        </Card>
      </div>

      {/* Getting Started */}
      <Card>
        <CardHeader>
          <CardTitle>Начало работы</CardTitle>
          <CardDescription>Начните эффективно управлять проектами</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-start space-x-4">
            <div className="bg-primary/10 p-2 rounded-md">
              <FolderKanban className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-medium">Создайте первый проект</h3>
              <p className="text-sm text-gray-500">
                Перейдите на страницу Проекты и создайте новый проект
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="bg-primary/10 p-2 rounded-md">
              <LayoutDashboard className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-medium">Настройте доску</h3>
              <p className="text-sm text-gray-500">
                Создайте колонки и организуйте рабочий процесс
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="bg-primary/10 p-2 rounded-md">
              <CheckSquare className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-medium">Добавьте задачи</h3>
              <p className="text-sm text-gray-500">
                Начните добавлять задачи и назначайте их членам команды
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
