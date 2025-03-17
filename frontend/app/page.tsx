import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="container mx-auto px-6 py-16 max-w-6xl">
        {/* Hero section */}
        <section className="space-y-8 py-12 md:py-20">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-gray-900 max-w-3xl mx-auto text-center leading-tight">
            Аналитика ценовой эластичности для вашего бизнеса
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto text-center leading-relaxed">
            Принимайте обоснованные решения о ценообразовании с помощью автоматизированного анализа данных
          </p>
          <div className="flex justify-center gap-6 pt-4">
            <Link href="/dashboard">
              <Button size="lg" className="text-lg px-8 py-6">
                Открыть дашборд
              </Button>
            </Link>
          </div>
        </section>

        {/* Features section */}
        <section className="py-16 md:py-24">
          <h2 className="text-3xl md:text-4xl font-semibold text-center mb-16 text-gray-900">
            Возможности системы
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12">
            <Card className="p-8 hover:shadow-lg transition-shadow">
              <h3 className="text-xl font-semibold mb-4 text-gray-900">
                Анализ эластичности
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Автоматический расчет коэффициента ценовой эластичности по различным товарам и категориям
              </p>
            </Card>
            
            <Card className="p-8 hover:shadow-lg transition-shadow">
              <h3 className="text-xl font-semibold mb-4 text-gray-900">
                Оценка акций
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Анализ эффективности маркетинговых мероприятий и их влияния на продажи
              </p>
            </Card>

            <Card className="p-8 hover:shadow-lg transition-shadow">
              <h3 className="text-xl font-semibold mb-4 text-gray-900">
                Прогнозирование
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Предсказание изменений объема продаж при корректировке цен
              </p>
            </Card>
          </div>
        </section>

        {/* Benefits section */}
        <section className="py-16 md:py-24">
          <h2 className="text-3xl md:text-4xl font-semibold text-center mb-16 text-gray-900">
            Преимущества
          </h2>
          <div className="grid md:grid-cols-2 gap-12 md:gap-16">
            <div className="space-y-6">
              <h3 className="text-2xl font-semibold text-gray-900">
                Для владельцев бизнеса
              </h3>
              <ul className="space-y-4 text-lg text-gray-600">
                <li className="flex items-start gap-3">
                  <span className="text-green-500 text-2xl">•</span>
                  Увеличение прибыли за счет оптимизации цен
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-500 text-2xl">•</span>
                  Снижение рисков при изменении ценовой политики
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-500 text-2xl">•</span>
                  Автоматизация процесса принятия решений
                </li>
              </ul>
            </div>

            <div className="space-y-6">
              <h3 className="text-2xl font-semibold text-gray-900">
                Для маркетологов
              </h3>
              <ul className="space-y-4 text-lg text-gray-600">
                <li className="flex items-start gap-3">
                  <span className="text-green-500 text-2xl">•</span>
                  Оценка эффективности промо-акций
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-500 text-2xl">•</span>
                  Сегментация товаров по эластичности
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-500 text-2xl">•</span>
                  Данные для создания маркетинговой стратегии
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* CTA section */}
        <section className="py-16 md:py-24 text-center">
          <div className="max-w-3xl mx-auto space-y-8">
            <h2 className="text-3xl md:text-4xl font-semibold text-gray-900">
              Начните использовать Price Elastic сегодня
            </h2>
            <p className="text-xl text-gray-600">
              Получите доступ к полному функционалу системы и принимайте более эффективные решения о ценообразовании
            </p>
            <div className="pt-4">
              <Link href="/dashboard">
                <Button size="lg" className="text-lg px-8 py-6">
                  Попробовать бесплатно
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}
