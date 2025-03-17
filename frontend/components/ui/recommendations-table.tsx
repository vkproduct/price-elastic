import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"

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

interface RecommendationsTableProps {
  data: Recommendation[]
  className?: string
}

export function RecommendationsTable({ data, className }: RecommendationsTableProps) {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return "text-green-500"
    if (confidence >= 70) return "text-yellow-500"
    return "text-red-500"
  }

  const getPriorityColor = (priority: number) => {
    if (priority >= 8) return "bg-red-100 dark:bg-red-900"
    if (priority >= 5) return "bg-yellow-100 dark:bg-yellow-900"
    return "bg-green-100 dark:bg-green-900"
  }

  return (
    <div className={cn("overflow-x-auto", className)}>
      <table className="w-full">
        <thead>
          <tr className="border-b">
            <th className="text-left p-2">Товар</th>
            <th className="text-right p-2">Текущая цена</th>
            <th className="text-right p-2">Рекомендуемая цена</th>
            <th className="text-right p-2">Потенциальная прибыль</th>
            <th className="text-center p-2">Уверенность</th>
            <th className="text-center p-2">Приоритет</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index} className="border-b">
              <td className="p-2 font-medium">{item.product}</td>
              <td className="text-right p-2">{item.currentPrice.toFixed(2)} ₽</td>
              <td className="text-right p-2">{item.recommendedPrice.toFixed(2)} ₽</td>
              <td className="text-right p-2">
                <div>{item.potentialProfit.absolute.toLocaleString()} ₽</div>
                <div className="text-sm text-muted-foreground">
                  +{item.potentialProfit.percentage}%
                </div>
              </td>
              <td className="text-center p-2">
                <span className={cn(
                  "font-medium",
                  getConfidenceColor(item.confidence)
                )}>
                  {item.confidence}%
                </span>
              </td>
              <td className="text-center p-2">
                <span className={cn(
                  "px-2 py-1 rounded font-medium",
                  getPriorityColor(item.priority)
                )}>
                  {item.priority}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
} 