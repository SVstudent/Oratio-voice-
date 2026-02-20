"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, Sparkles } from "lucide-react"
import { motion } from "framer-motion"
import { WavyBackground } from "@/components/ui/wavy-background"
import { LiquidGlassCard } from "@/components/kokonutui/liquid-glass-card"

export function HeroSection() {
  return (
    <WavyBackground
      className="mx-auto max-w-7xl"
      containerClassName="relative overflow-hidden border-b border-border/40"
      colors={["#3b82f6", "#2563eb", "#1d4ed8", "#1e40af", "#60a5fa"]}
      waveWidth={50}
      backgroundFill="black"
      blur={10}
      speed="fast"
      waveOpacity={0.5}
    >
      <div className="container relative mx-auto px-4 py-20 md:px-6 md:py-32">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-4xl text-center"
        >
          <LiquidGlassCard className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-md w-auto">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-accent/30 bg-accent/10 px-4 py-1.5 text-sm">
              <Sparkles className="h-3.5 w-3.5 text-accent" />
              <span className="text-accent-foreground">AWS Bedrock | Datadog | MiniMax | CopilotKit</span>
            </div>

            <h1
              className="mb-8 text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 via-blue-500 to-cyan-400 bg-clip-text text-transparent"
              style={{ fontFamily: 'Audiowide, sans-serif' }}
            >
              Test & Optimize Your Cold Outreach Scripts with AI
            </h1>

            {/* Sponsor Badges */}
            <div className="mb-8 flex flex-col items-center justify-center gap-6">
              <div className="flex items-center justify-center gap-4 flex-wrap">
                <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-gray-900/80">
                  <span className="h-2 w-2 rounded-full bg-orange-400" /> AWS Bedrock
                </span>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-gray-900/80">
                  <span className="h-2 w-2 rounded-full bg-purple-400" /> Datadog
                </span>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-gray-900/80">
                  <span className="h-2 w-2 rounded-full bg-green-400" /> MiniMax Voice
                </span>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-gray-900/80">
                  <span className="h-2 w-2 rounded-full bg-blue-400" /> CopilotKit
                </span>
              </div>

              <p className="text-sm text-gray-900/70">
                Built for the AWS x Datadog GenAI Hackathon
              </p>
            </div>
          </LiquidGlassCard>

          <p className="mb-10 mt-8 text-pretty text-lg text-muted-foreground md:text-xl">
            Upload your cold call scripts, deploy AI-powered outreach agents, and optimize with real-time analytics.
            Test multiple scripts side by side, practice with AI voice prospects, and find what converts best.
          </p>

          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/login">
              <Button size="lg" className="group w-full bg-accent text-accent-foreground hover:bg-accent/90 sm:w-auto">
                Start Testing Your Scripts
                <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
          </div>

        </motion.div>

      </div>
    </WavyBackground>
  )
}
