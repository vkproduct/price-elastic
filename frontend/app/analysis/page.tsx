import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function AnalysisPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Анализ</h2>
      </div>
      <div className="grid gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Загрузка данных</CardTitle>
            <CardDescription>
              Загрузите файл с данными о продажах для анализа ценовой эластичности
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center w-full">
              <label
                htmlFor="dropzone-file"
                className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer bg-background hover:bg-accent/50"
              >
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <svg
                    className="w-8 h-8 mb-4 text-muted-foreground"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 16"
                  >
                    <path
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                    />
                  </svg>
                  <p className="mb-2 text-sm text-muted-foreground">
                    <span className="font-semibold">Нажмите для загрузки</span> или
                    перетащите файл
                  </p>
                  <p className="text-xs text-muted-foreground">
                    CSV, Excel (до 10MB)
                  </p>
                </div>
                <input id="dropzone-file" type="file" className="hidden" />
              </label>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 