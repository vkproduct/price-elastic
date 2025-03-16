import Link from "next/link"

export default function HomePage() {
  return (
    <div className="flex-1">
      <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center space-y-4 text-center">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                Price Elastic
              </h1>
              <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                Система анализа ценовой эластичности для принятия обоснованных
                решений о ценообразовании
              </p>
            </div>
            <div className="space-x-4">
              <Link
                className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                href="/dashboard"
              >
                Начать работу
              </Link>
              <Link
                className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                href="/analysis"
              >
                Попробовать демо
              </Link>
            </div>
          </div>
        </div>
      </section>
      <section className="w-full py-12 md:py-24 lg:py-32 bg-muted">
        <div className="container px-4 md:px-6">
          <div className="grid gap-6 lg:grid-cols-3 lg:gap-12">
            <div className="flex flex-col justify-center space-y-4">
              <div className="space-y-2">
                <h2 className="text-2xl font-bold tracking-tighter sm:text-3xl">
                  Анализ эластичности
                </h2>
                <p className="max-w-[600px] text-gray-500 md:text-base/relaxed lg:text-base/relaxed xl:text-base/relaxed dark:text-gray-400">
                  Автоматический расчет коэффициента ценовой эластичности по
                  различным товарам и категориям
                </p>
              </div>
            </div>
            <div className="flex flex-col justify-center space-y-4">
              <div className="space-y-2">
                <h2 className="text-2xl font-bold tracking-tighter sm:text-3xl">
                  Оценка акций
                </h2>
                <p className="max-w-[600px] text-gray-500 md:text-base/relaxed lg:text-base/relaxed xl:text-base/relaxed dark:text-gray-400">
                  Анализ эффективности маркетинговых мероприятий и их влияния на
                  продажи
                </p>
              </div>
            </div>
            <div className="flex flex-col justify-center space-y-4">
              <div className="space-y-2">
                <h2 className="text-2xl font-bold tracking-tighter sm:text-3xl">
                  Прогнозирование
                </h2>
                <p className="max-w-[600px] text-gray-500 md:text-base/relaxed lg:text-base/relaxed xl:text-base/relaxed dark:text-gray-400">
                  Предсказание изменений объема продаж при корректировке цен
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
