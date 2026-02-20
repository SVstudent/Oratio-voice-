"use client"

import { useState } from "react"
import { IconCheck, IconCopy } from "@tabler/icons-react"
import { cn } from "@/lib/utils"

interface CodeBlockProps {
  code: string
  language: string
  title?: string
}

export function CodeBlock({ code, language, title }: CodeBlockProps) {
  const [copied, setCopied] = useState(false)

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="relative group">
      {title && (
        <div className="flex items-center justify-between px-4 py-2 bg-blue-100/50 border-b border-blue-200 rounded-t-lg">
          <span className="text-xs font-medium text-gray-500">{title}</span>
          <span className="text-xs text-gray-400">{language}</span>
        </div>
      )}
      <div className="relative">
        <button
          onClick={copyToClipboard}
          className={cn(
            "absolute right-3 top-3 z-10",
            "p-2 rounded-md",
            "bg-neutral-800/80 hover:bg-neutral-700/80",
            "border border-blue-200",
            "opacity-0 group-hover:opacity-100",
            "transition-all duration-200",
            "flex items-center gap-2"
          )}
          aria-label="Copy code"
        >
          {copied ? (
            <>
              <IconCheck className="h-4 w-4 text-green-400" />
              <span className="text-xs text-green-400">Copied!</span>
            </>
          ) : (
            <>
              <IconCopy className="h-4 w-4 text-gray-500" />
              <span className="text-xs text-gray-500">Copy</span>
            </>
          )}
        </button>
        <pre
          className={cn(
            "overflow-x-auto p-4",
            "bg-blue-50/50 border border-blue-200/50",
            title ? "rounded-b-lg" : "rounded-lg",
            "text-sm leading-relaxed"
          )}
        >
          <code className={`language-${language} text-gray-700`}>
            {code}
          </code>
        </pre>
      </div>
    </div>
  )
}

