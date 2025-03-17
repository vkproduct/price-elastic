"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { Heatmap } from "@/components/ui/heatmap"
import { PromotionsChart } from "@/components/ui/promotions-chart"
import { RecommendationsTable } from "@/components/ui/recommendations-table"
import { ArrowDown, ArrowUp, Loader2 } from "lucide-react"
import { fetchSalesData } from "@/lib/sheets"
import { calculateElasticity, analyzePromotions } from "@/lib/analytics"
import { Suspense } from 'react'

interface Recommendation {
  product: string
  currentPrice: number
  recommendedPrice: number
  potentialProfit: {
    absolute: number
    percentage: number
  }
  confidence: number
  priority: number
}

interface DashboardData {
  elasticityData: Array<{
    category: string
    elasticity: number
    currentPrice: number
    optimumPrice: number
    recommendedChange: number
  }>
  promotionsData: Array<{
    name: string
    salesIncrease: number
    averageCheck: number
    conversionRate: number
  }>
  recommendations: Recommendation[]
  metrics: {
    avgElasticity: number
    lostProfit: number
    potentialGrowth: number
    activePromotions: number
  }
}

function DashboardMetricCard({ title, value, change, loading = false }: { 
  title: string
  value: string | number
  change?: number
  loading?: boolean
}) {
  return (
    <Card className="p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground mb-2">{title}</p>
          <h3 className="text-3xl font-bold tracking-tight">
            {loading ? (
              <Loader2 className="h-6 w-6 animate-spin" />
            ) : (
              value
            )}
          </h3>
        </div>
        {typeof change !== 'undefined' && (
          <div className={`flex items-center ${change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {change >= 0 ? <ArrowUp className="h-5 w-5" /> : <ArrowDown className="h-5 w-5" />}
            <span className="text-sm font-medium ml-1">{Math.abs(change)}%</span>
          </div>
        )}
      </div>
    </Card>
  )
}

export default function DashboardPage() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState<DashboardData>({
    elasticityData: [],
    promotionsData: [],
    recommendations: [],
    metrics: {
      avgElasticity: 0,
      lostProfit: 0,
      potentialGrowth: 0,
      activePromotions: 0
    }
  })

  useEffect(() => {
    async function loadData() {
      try {
        const salesData = await fetchSalesData()
        const elasticityData = calculateElasticity(salesData)
        const promotionsData = analyzePromotions(salesData)

        // Расчет метрик
        const avgElasticity = elasticityData.reduce((sum, item) => sum + item.elasticity, 0) / elasticityData.length
        const lostProfit = elasticityData
          .filter(item => item.elasticity < -1)
          .reduce((sum, item) => sum + Math.abs(item.recommendedChange) * item.currentPrice / 100, 0)
        const potentialGrowth = elasticityData
          .filter(item => item.elasticity > -1)
          .reduce((sum, item) => sum + item.recommendedChange * item.currentPrice / 100, 0)

        // Генерация рекомендаций
        const recommendations = elasticityData
          .filter(item => Math.abs(item.recommendedChange) > 5)
          .map(item => ({
            product: item.category,
            currentPrice: item.currentPrice,
            recommendedPrice: item.optimumPrice,
            potentialProfit: {
              absolute: Math.abs(item.recommendedChange * item.currentPrice / 100),
              percentage: Math.abs(item.recommendedChange)
            },
            confidence: Math.min(Math.abs(item.elasticity) * 50, 100),
            priority: Math.abs(item.recommendedChange * item.elasticity)
          }))
          .sort((a, b) => b.priority - a.priority)
          .slice(0, 5)

        setData({
          elasticityData,
          promotionsData,
          recommendations,
          metrics: {
            avgElasticity: Number(avgElasticity.toFixed(2)),
            lostProfit: Math.round(lostProfit),
            potentialGrowth: Math.round(potentialGrowth),
            activePromotions: promotionsData.length
          }
        })
      } catch (error) {
        console.error('Error loading data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) {
    return (
      <div className="container mx-auto p-8 space-y-12">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {Array(4).fill(0).map((_, i) => (
            <DashboardMetricCard 
              key={i}
              title="Загрузка..." 
              value=""
              loading={true}
            />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-12 px-8 space-y-12">
      <div>
        <h1 className="text-4xl font-bold tracking-tight mb-2">Аналитика</h1>
        <p className="text-lg text-muted-foreground">Анализ эластичности и эффективности акций</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <DashboardMetricCard 
          title="Средняя эластичность" 
          value={data.metrics.avgElasticity.toFixed(2)} 
        />
        <DashboardMetricCard 
          title="Упущенная прибыль" 
          value={`${data.metrics.lostProfit.toLocaleString('ru-RU')} ₽`}
          change={-15}
        />
        <DashboardMetricCard 
          title="Потенциал роста" 
          value={`${data.metrics.potentialGrowth.toLocaleString('ru-RU')} ₽`}
          change={12}
        />
        <DashboardMetricCard 
          title="Активные акции" 
          value={data.metrics.activePromotions.toString()}
        />
      </div>

      <div className="grid gap-8 md:grid-cols-2">
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-6">Эластичность по категориям</h3>
          <Heatmap data={data.elasticityData} />
        </Card>

        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-6">Эффективность акций</h3>
          <PromotionsChart data={data.promotionsData} />
        </Card>
      </div>

      <Card className="p-6">
        <h3 className="text-xl font-semibold mb-6">Топ рекомендаций</h3>
        <RecommendationsTable data={data.recommendations} />
      </Card>
    </div>
  )
} 