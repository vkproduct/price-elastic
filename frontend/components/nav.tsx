"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { ThemeToggle } from "./theme-toggle"
import { useEffect, useState } from "react"

const navigation = [
  {
    name: "Дашборд",
    href: "/dashboard",
  },
  {
    name: "Анализ",
    href: "/analysis",
  },
  {
    name: "Отчеты",
    href: "/reports",
  },
  {
    name: "Настройки",
    href: "/settings",
  },
]

export function Nav() {
  const pathname = usePathname()
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0)
    }

    window.addEventListener("scroll", handleScroll, { passive: true })
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <header 
      className={cn(
        "fixed top-0 z-50 w-full transition-all duration-200",
        isScrolled 
          ? "border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 shadow-sm" 
          : "bg-background"
      )}
    >
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-14 items-center">
          <Link href="/" className="flex items-center space-x-2">
            <span className="font-bold">
              Price Elastic
            </span>
          </Link>
          
          <div className="flex-1 flex justify-center">
            <div className="hidden md:flex md:items-center md:space-x-6">
              {navigation.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "text-sm font-medium transition-colors hover:text-foreground/80",
                    pathname === item.href
                      ? "text-foreground"
                      : "text-foreground/60"
                  )}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>

          <div className="flex items-center">
            <ThemeToggle />
          </div>
        </div>
      </nav>
    </header>
  )
} 