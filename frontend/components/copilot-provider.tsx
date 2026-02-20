"use client"

import type React from "react"
import { useState, useEffect } from "react"

// CopilotKit is loaded dynamically to prevent crashes when not configured
export default function CopilotProvider({ children }: { children: React.ReactNode }) {
  const [CopilotKitComponent, setCopilotKitComponent] = useState<React.ComponentType<any> | null>(null)
  const [enabled, setEnabled] = useState(false)

  useEffect(() => {
    // Only enable CopilotKit if the env flag is set
    const apiKey = process.env.NEXT_PUBLIC_COPILOTKIT_API_KEY
    if (apiKey) {
      import("@copilotkit/react-core").then((mod) => {
        setCopilotKitComponent(() => mod.CopilotKit)
        setEnabled(true)
      }).catch(() => {
        // CopilotKit not available, continue without it
      })
    }
  }, [])

  if (enabled && CopilotKitComponent) {
    return (
      <CopilotKitComponent publicApiKey={process.env.NEXT_PUBLIC_COPILOTKIT_API_KEY}>
        {children}
      </CopilotKitComponent>
    )
  }

  return <>{children}</>
}
