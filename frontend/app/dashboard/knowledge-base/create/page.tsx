"use client"
import DashboardLayout from "@/components/dashboard-layout"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { IconFile, IconX, IconArrowLeft } from "@tabler/icons-react"
import { useState, useCallback } from "react"
import { useRouter } from "next/navigation"
import FileUpload from "@/components/file-upload"
import Link from "next/link"

interface FileWithDescription {
  file: File
  description: string
}

export default function CreateKnowledgeBasePage() {
  const router = useRouter()
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [files, setFiles] = useState<FileWithDescription[]>([])

  const handleFileUploadSuccess = useCallback((file: File) => {
    setFiles((prev) => [...prev, { file, description: "" }])
  }, [])

  const updateFileDescription = (index: number, description: string) => {
    setFiles((prev) => prev.map((f, i) => (i === index ? { ...f, description } : f)))
  }

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleCreate = () => {
    console.log({
      name,
      description,
      files,
    })
    router.push("/dashboard/knowledge-base")
  }

  const canCreate = name.trim() !== "" && description.trim() !== "" && files.length > 0

  return (
    <DashboardLayout>
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="border-b border-blue-200 bg-blue-50/50 backdrop-blur-sm">
          <div className="p-6 md:p-8">
            <Link href="/dashboard/knowledge-base">
              <Button variant="ghost" className="text-gray-500 hover:text-blue-600 mb-4 -ml-2">
                <IconArrowLeft className="h-4 w-4 mr-2" />
                Back to Knowledge Base
              </Button>
            </Link>
            <h1 className="text-3xl font-bold text-gray-900">Create Knowledge Base</h1>
            <p className="text-gray-500 mt-1">Upload documents and files for your AI agents.</p>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6 md:p-8">
          <div className="max-w-3xl mx-auto space-y-6">
            <Card className="bg-blue-50 border-blue-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Knowledge Base Details</h2>
              <div className="space-y-6">
                <div>
                  <Label htmlFor="kb-name" className="text-gray-900 mb-2">
                    Name
                  </Label>
                  <Input
                    id="kb-name"
                    placeholder="e.g., Product Documentation"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="bg-white border-blue-200 text-gray-900"
                  />
                </div>
                <div>
                  <Label htmlFor="kb-description" className="text-gray-900 mb-2">
                    Description
                  </Label>
                  <Textarea
                    id="kb-description"
                    placeholder="Describe what this knowledge base contains..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    className="bg-white border-blue-200 text-gray-900 resize-none"
                  />
                </div>
              </div>
            </Card>

            <Card className="bg-blue-50 border-blue-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">Upload Files</h2>
              <p className="text-gray-500 text-sm mb-6">
                Upload documents, PDFs, text files, or other resources. Each file can have a description.
              </p>

              <div className="mb-6">
                <FileUpload
                  onUploadSuccess={handleFileUploadSuccess}
                  maxFileSize={10 * 1024 * 1024} // 10MB
                  uploadDelay={1500}
                  className="max-w-full"
                />
              </div>

              {/* Files List */}
              {files.length > 0 && (
                <div className="space-y-4">
                  <h3 className="text-sm font-medium text-gray-900">Uploaded Files ({files.length})</h3>
                  {files.map((fileItem, index) => (
                    <div key={index} className="bg-white border border-blue-200 rounded-lg p-4">
                      <div className="flex items-start gap-3 mb-3">
                        <IconFile className="h-5 w-5 text-accent shrink-0 mt-0.5" />
                        <div className="flex-1 min-w-0">
                          <p className="text-gray-900 font-medium truncate">{fileItem.file.name}</p>
                          <p className="text-gray-400 text-xs">{(fileItem.file.size / 1024).toFixed(2)} KB</p>
                        </div>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => removeFile(index)}
                          className="text-gray-500 hover:text-red-400"
                        >
                          <IconX className="h-4 w-4" />
                        </Button>
                      </div>
                      <Input
                        placeholder="Add a description for this file..."
                        value={fileItem.description}
                        onChange={(e) => updateFileDescription(index, e.target.value)}
                        className="bg-blue-50 border-blue-200 text-gray-900 text-sm"
                      />
                    </div>
                  ))}
                </div>
              )}
            </Card>

            <div className="flex items-center justify-end gap-4">
              <Link href="/dashboard/knowledge-base">
                <Button variant="outline" className="border-neutral-700 text-gray-900 hover:bg-blue-100 bg-transparent">
                  Cancel
                </Button>
              </Link>
              <Button onClick={handleCreate} disabled={!canCreate} className="bg-accent hover:bg-accent/90 text-white">
                Create Knowledge Base
              </Button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
