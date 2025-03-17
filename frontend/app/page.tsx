import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import Link from 'next/link'
import { BadgeCheck, TrendingUp, LineChart, Zap, ShieldCheck, Users } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="container mx-auto px-6 py-16 max-w-6xl">
        {/* Hero section */}
        <section className="space-y-8 py-12 md:py-20">
          <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full mx-auto">
            <Zap size={16} />
            <span className="text-sm font-medium">Бесплатный пробный период 14 дней</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-gray-900 max-w-3xl mx-auto text-center leading-tight">
            Увеличьте прибыль с помощью умного ценообразования
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto text-center leading-relaxed">
            Price Elastic анализирует ваши данные и помогает принимать решения, которые увеличивают продажи до 30%
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
            <Link href="/dashboard">
              <Button size="lg" className="text-lg px-8 py-6 w-full sm:w-auto">
                Попробовать бесплатно
              </Button>
            </Link>
            <Link href="#demo">
              <Button variant="outline" size="lg" className="text-lg px-8 py-6 w-full sm:w-auto">
                Посмотреть демо
              </Button>
            </Link>
          </div>
          <div className="flex justify-center items-center gap-8 pt-8 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <BadgeCheck size={16} className="text-primary" />
              <span>Без карты</span>
            </div>
            <div className="flex items-center gap-2">
              <BadgeCheck size={16} className="text-primary" />
              <span>Простая интеграция</span>
            </div>
            <div className="flex items-center gap-2">
              <BadgeCheck size={16} className="text-primary" />
              <span>Поддержка 24/7</span>
            </div>
          </div>
        </section>

        {/* Stats section */}
        <section className="py-16 md:py-24 border-y border-gray-200">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary mb-2">500+</div>
              <div className="text-sm text-gray-600">Активных клиентов</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary mb-2">25%</div>
              <div className="text-sm text-gray-600">Средний рост прибыли</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary mb-2">1M+</div>
              <div className="text-sm text-gray-600">Проанализировано SKU</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary mb-2">99.9%</div>
              <div className="text-sm text-gray-600">Точность анализа</div>
            </div>
          </div>
        </section>

        {/* Features section */}
        <section className="py-16 md:py-24">
          <h2 className="text-3xl md:text-4xl font-semibold text-center mb-4 text-gray-900">
            Возможности системы
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-2xl mx-auto">
            Все необходимые инструменты для оптимизации ценообразования в одном месте
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12">
            <Card className="p-8 hover:shadow-lg transition-shadow">
              <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <LineChart className="text-primary" size={24} />
              </div>
              <h3 className="text-xl font-semibold mb-4 text-gray-900">
                Анализ эластичности
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Автоматически рассчитываем оптимальные цены на основе исторических данных о продажах
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  Расчет по категориям
                </li>
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  Сезонные тренды
                </li>
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  Конкурентный анализ
                </li>
              </ul>
            </Card>
            
            <Card className="p-8 hover:shadow-lg transition-shadow">
              <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <TrendingUp className="text-primary" size={24} />
              </div>
              <h3 className="text-xl font-semibold mb-4 text-gray-900">
                Оценка акций
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Анализируем эффективность промо-акций и прогнозируем их влияние на продажи
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  ROI промо-акций
                </li>
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  Сравнение кампаний
                </li>
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  Рекомендации по скидкам
                </li>
              </ul>
            </Card>

            <Card className="p-8 hover:shadow-lg transition-shadow">
              <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <ShieldCheck className="text-primary" size={24} />
              </div>
              <h3 className="text-xl font-semibold mb-4 text-gray-900">
                Прогнозирование
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Предсказываем изменения в продажах при корректировке цен с точностью до 95%
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  ML-модели
                </li>
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  Сценарный анализ
                </li>
                <li className="flex items-center gap-2 text-sm text-gray-600">
                  <BadgeCheck size={16} className="text-primary" />
                  Авторекомендации
                </li>
              </ul>
            </Card>
          </div>
        </section>

        {/* Benefits section */}
        <section className="py-16 md:py-24 bg-gray-50 -mx-6 px-6">
          <h2 className="text-3xl md:text-4xl font-semibold text-center mb-4 text-gray-900">
            Кому подойдет Price Elastic?
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-2xl mx-auto">
            Наше решение создано для бизнесов, которые хотят принимать data-driven решения
          </p>
          <div className="grid md:grid-cols-2 gap-12 md:gap-16">
            <div className="bg-white p-8 rounded-xl shadow-sm">
              <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <Users className="text-primary" size={24} />
              </div>
              <h3 className="text-2xl font-semibold text-gray-900 mb-6">
                Для владельцев бизнеса
              </h3>
              <ul className="space-y-4 text-lg text-gray-600">
                <li className="flex items-start gap-3">
                  <span className="text-primary text-2xl">•</span>
                  Увеличение прибыли за счет оптимизации цен
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-primary text-2xl">•</span>
                  Снижение рисков при изменении ценовой политики
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-primary text-2xl">•</span>
                  Автоматизация процесса принятия решений
                </li>
              </ul>
              <div className="mt-8">
                <Link href="/dashboard">
                  <Button variant="outline" className="w-full">Начать использовать</Button>
                </Link>
              </div>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-sm">
              <div className="bg-primary/10 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <TrendingUp className="text-primary" size={24} />
              </div>
              <h3 className="text-2xl font-semibold text-gray-900 mb-6">
                Для маркетологов
              </h3>
              <ul className="space-y-4 text-lg text-gray-600">
                <li className="flex items-start gap-3">
                  <span className="text-primary text-2xl">•</span>
                  Оценка эффективности промо-акций
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-primary text-2xl">•</span>
                  Сегментация товаров по эластичности
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-primary text-2xl">•</span>
                  Данные для создания маркетинговой стратегии
                </li>
              </ul>
              <div className="mt-8">
                <Link href="/dashboard">
                  <Button variant="outline" className="w-full">Попробовать бесплатно</Button>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing section */}
        <section className="py-16 md:py-24">
          <h2 className="text-3xl md:text-4xl font-semibold text-center mb-4 text-gray-900">
            Тарифные планы
          </h2>
          <p className="text-xl text-gray-600 text-center mb-16 max-w-2xl mx-auto">
            Выберите план, который подходит именно вашему бизнесу
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="p-8">
              <h3 className="text-xl font-semibold mb-2">Бесплатный</h3>
              <div className="text-4xl font-bold mb-6">₽0</div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>До 5 SKU</span>
                </li>
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>Базовая аналитика</span>
                </li>
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>Email поддержка</span>
                </li>
              </ul>
              <Button variant="outline" className="w-full">Начать бесплатно</Button>
            </Card>

            <Card className="p-8 border-primary">
              <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm mb-4">
                Популярный выбор
              </div>
              <h3 className="text-xl font-semibold mb-2">Бизнес</h3>
              <div className="text-4xl font-bold mb-6">₽4,900</div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>До 1000 SKU</span>
                </li>
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>Расширенная аналитика</span>
                </li>
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>Приоритетная поддержка</span>
                </li>
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>API доступ</span>
                </li>
              </ul>
              <Button className="w-full">Выбрать план</Button>
            </Card>

            <Card className="p-8">
              <h3 className="text-xl font-semibold mb-2">Enterprise</h3>
              <div className="text-4xl font-bold mb-6">По запросу</div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>Безлимитное количество SKU</span>
                </li>
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>Индивидуальные интеграции</span>
                </li>
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>Выделенный менеджер</span>
                </li>
                <li className="flex items-center gap-2">
                  <BadgeCheck size={16} className="text-primary" />
                  <span>SLA</span>
                </li>
              </ul>
              <Button variant="outline" className="w-full">Связаться с нами</Button>
            </Card>
          </div>
        </section>

        {/* CTA section */}
        <section className="py-16 md:py-24 text-center bg-primary/5 -mx-6 px-6 rounded-3xl">
          <div className="max-w-3xl mx-auto space-y-8">
            <h2 className="text-3xl md:text-4xl font-semibold text-gray-900">
              Начните использовать Price Elastic сегодня
            </h2>
            <p className="text-xl text-gray-600">
              Попробуйте 14 дней бесплатно и убедитесь, как аналитика может улучшить ваши продажи
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
              <Link href="/dashboard">
                <Button size="lg" className="text-lg px-8 py-6 w-full sm:w-auto">
                  Попробовать бесплатно
                </Button>
              </Link>
              <Link href="#demo">
                <Button variant="outline" size="lg" className="text-lg px-8 py-6 w-full sm:w-auto">
                  Запросить демо
                </Button>
              </Link>
            </div>
            <p className="text-sm text-gray-500">
              Не требует ввода банковской карты • Отменить подписку можно в любой момент
            </p>
          </div>
        </section>
      </div>
    </main>
  )
}
