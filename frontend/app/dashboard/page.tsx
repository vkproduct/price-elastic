import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Дашборд</h2>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Средняя эластичность</CardTitle>
            <CardDescription>По всем товарам</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">-1.2</div>
            <p className="text-xs text-muted-foreground">
              +20.1% с прошлого месяца
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Активные акции</CardTitle>
            <CardDescription>Текущие промо-кампании</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">
              +2 новых акции за неделю
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Товары в анализе</CardTitle>
            <CardDescription>Отслеживаемые SKU</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2,350</div>
            <p className="text-xs text-muted-foreground">
              +180 новых товаров
            </p>
          </CardContent>
        </Card>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Динамика эластичности</CardTitle>
            <CardDescription>
              Изменение показателя за последние 30 дней
            </CardDescription>
          </CardHeader>
          <CardContent>
            {/* График будет добавлен позже */}
            <div className="h-[200px] bg-muted rounded-md"></div>
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Топ категорий</CardTitle>
            <CardDescription>
              По эффективности промо-акций
            </CardDescription>
          </CardHeader>
          <CardContent>
            {/* Таблица будет добавлена позже */}
            <div className="h-[200px] bg-muted rounded-md"></div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 