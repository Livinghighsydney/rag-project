import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import type { Message } from '../../types'
import { CONTENT_MODES } from '../../types'

interface Props {
  message: Message
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)
  const copy = () => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }
  return (
    <button
      onClick={copy}
      className="text-xs text-gray-400 hover:text-gray-600 border border-gray-200 rounded px-2 py-0.5 transition-colors"
    >
      {copied ? 'Copied' : 'Copy'}
    </button>
  )
}

function ModeTag({ contentType }: { contentType: string }) {
  const mode = CONTENT_MODES.find((m) => m.type === contentType)
  if (!mode || contentType === 'answer') return null
  return (
    <span className="text-xs bg-blue-50 text-blue-600 border border-blue-100 rounded-full px-2 py-0.5 font-medium">
      {mode.label}
    </span>
  )
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user'
  const time = new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

  if (isUser) {
    return (
      <div className="flex justify-end mb-4">
        <div className="max-w-[70%]">
          <div className="bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 text-sm leading-relaxed">
            {message.content}
          </div>
          <p className="text-xs text-gray-400 text-right mt-1">{time}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start mb-4">
      <div className="max-w-[82%]">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-6 h-6 rounded-full bg-amber-500 flex items-center justify-center text-white text-xs font-bold">
            A
          </div>
          <span className="text-xs text-gray-500 font-medium">Advisor</span>
          {message.contentType && <ModeTag contentType={message.contentType} />}
        </div>
        <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 text-sm leading-relaxed prose prose-sm max-w-none">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>
        <div className="flex items-center gap-3 mt-1 ml-1">
          <p className="text-xs text-gray-400">{time}</p>
          <CopyButton text={message.content} />
        </div>
      </div>
    </div>
  )
}
