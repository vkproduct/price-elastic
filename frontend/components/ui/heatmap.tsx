import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface HeatmapProps {
  data: {
    category: string
    elasticity: number
    optimumPrice: number
    currentPrice: number
    recommendedChange: number
  }[]
  className?: string
}

export function Heatmap({ data, className }: HeatmapProps) {
  const getElasticityColor = (elasticity: number) => {
    // Цветовая шкала от синего (неэластичный) к красному (эластичный)
    if (elasticity >= -0.5) return "bg-blue-100 dark:bg-blue-900"
    if (elasticity >= -1.0) return "bg-blue-200 dark:bg-blue-800"
    if (elasticity >= -1.5) return "bg-red-100 dark:bg-red-900"
    if (elasticity >= -2.0) return "bg-red-200 dark:bg-red-800"
    return "bg-red-300 dark:bg-red-700"
  }

  return (
    <div className={cn("grid gap-2", className)}>
      <div className="grid grid-cols-5 gap-2 text-sm font-medium">
        <div>Категория</div>
        <div>Эластичность</div>
        <div>Текущая цена</div>
        <div>Оптимальная цена</div>
        <div>Рекомендуемое изменение</div>
      </div>
      {data.map((item, index) => (
        <div
          key={index}
          className="grid grid-cols-5 gap-2 text-sm"
        >
          <div className="font-medium">{item.category}</div>
          <div className={cn(
            "px-2 py-1 rounded",
            getElasticityColor(item.elasticity)
          )}>
            {item.elasticity.toFixed(2)}
          </div>
          <div>{item.currentPrice.toFixed(2)} ₽</div>
          <div>{item.optimumPrice.toFixed(2)} ₽</div>
          <div className={cn(
            "px-2 py-1 rounded",
            item.recommendedChange > 0 ? "bg-green-100 dark:bg-green-900" : "bg-red-100 dark:bg-red-900"
          )}>
            {item.recommendedChange > 0 ? "+" : ""}{item.recommendedChange.toFixed(1)}%
          </div>
        </div>
      ))}
    </div>
  )
} 