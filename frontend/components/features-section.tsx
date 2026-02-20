"use client"

import { FlaskConical, Phone, Activity, Zap, Sparkles, Building2 } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { AnimatedWaves } from "./animated-waves"

const features = [
  {
    icon: FlaskConical,
    title: "Script A/B Testing",
    description:
      "Test multiple cold call script variations against AI prospects. Compare conversion rates, objection handling, and overall effectiveness side by side.",
  },
  {
    icon: Phone,
    title: "AI Voice Calls",
    description:
      "Simulate real cold calls with AI-powered voice prospects using MiniMax. Practice your pitch, handle objections, and refine your delivery before going live.",
  },
  {
    icon: Activity,
    title: "Real-Time Analytics",
    description:
      "Track call duration, sentiment analysis, and conversion metrics with Datadog-powered dashboards. Identify what works and iterate fast.",
  },
  {
    icon: Zap,
    title: "Instant Deployment",
    description:
      "Deploy your outreach agents in seconds with AWS Bedrock AgentCore and Chameleon architecture. One runtime for unlimited agents.",
  },
  {
    icon: Sparkles,
    title: "AI Script Optimization",
    description:
      "Use CopilotKit's AI copilot to analyze and improve your scripts. Get real-time suggestions for better openers, objection handlers, and closing techniques.",
  },
  {
    icon: Building2,
    title: "Enterprise Scale",
    description:
      "Run unlimited outreach agents on a single runtime with Chameleon architecture. Multi-tenant, secure, and built on AWS infrastructure.",
  },
]

export function FeaturesSection() {
  return (
    <section id="features" className="relative border-b border-border/40 bg-background py-20 md:py-32">
      <AnimatedWaves />

      <div className="container relative mx-auto px-4 md:px-6">
        <div className="mx-auto mb-16 max-w-3xl text-center">
          <h2 className="mb-4 text-balance text-3xl font-bold tracking-tight md:text-4xl lg:text-5xl">
            Everything you need to master cold outreach
          </h2>
          <p className="text-pretty text-lg text-muted-foreground">
            AI-powered tools to test, optimize, and scale your cold outreach scripts.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <Card
              key={index}
              className="border-border/50 bg-card transition-all hover:border-accent/50 hover:shadow-lg hover:shadow-accent/5"
            >
              <CardContent className="p-6">
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-accent/10">
                  <feature.icon className="h-6 w-6 text-accent" />
                </div>
                <h3 className="mb-2 text-xl font-semibold">{feature.title}</h3>
                <p className="text-pretty leading-relaxed text-muted-foreground">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
