import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface PromotionData {
  name: string
  salesIncrease: number
  averageCheck: number
  conversionRate: number
}

interface PromotionsChartProps {
  data: PromotionData[]
  className?: string
}

export function PromotionsChart({ data, className }: PromotionsChartProps) {
  return (
    <div className={cn("h-[400px]", className)}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 60
          }}
          barGap={8}
          barSize={24}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.4} />
          <XAxis 
            dataKey="name"
            interval={0}
            angle={0}
            height={60}
            tick={{ fontSize: 14 }}
          />
          <YAxis 
            tickFormatter={(value) => `${value}%`}
            tick={{ fontSize: 14 }}
            width={50}
          />
          <Tooltip
            cursor={{ fill: 'rgba(0, 0, 0, 0.1)' }}
            contentStyle={{
              backgroundColor: 'var(--background)',
              borderColor: 'var(--border)',
              borderRadius: '8px',
              fontSize: '14px',
              padding: '12px'
            }}
            formatter={(value: number, name: string) => {
              switch (name) {
                case 'salesIncrease':
                  return [`${value}%`, 'Рост продаж']
                case 'averageCheck':
                  return [`${value}%`, 'Изменение среднего чека']
                case 'conversionRate':
                  return [`${value}%`, 'Рост конверсии']
                default:
                  return [value, name]
              }
            }}
            labelStyle={{
              marginBottom: '8px',
              fontWeight: 'bold'
            }}
          />
          <Legend 
            verticalAlign="bottom"
            height={40}
            wrapperStyle={{
              fontSize: '14px'
            }}
          />
          <Bar 
            dataKey="salesIncrease" 
            fill="#2563eb" 
            name="Рост продаж"
            radius={[4, 4, 0, 0]}
          />
          <Bar 
            dataKey="averageCheck" 
            fill="#16a34a" 
            name="Изменение среднего чека"
            radius={[4, 4, 0, 0]}
          />
          <Bar 
            dataKey="conversionRate" 
            fill="#ca8a04" 
            name="Рост конверсии"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
} 