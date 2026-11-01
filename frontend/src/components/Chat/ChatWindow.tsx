import { useEffect, useRef, useState } from 'react'
import type { Message, ContentType } from '../../types'
import { MessageBubble } from './MessageBubble'
import { InputBar } from './InputBar'
import { ModuleSelector } from './ModuleSelector'

interface Props {
  messages: Message[]
  isLoading: boolean
  error: string | null
  contentType: ContentType
  onContentTypeChange: (t: ContentType) => void
  onSend: (text: string, contentType: ContentType) => void
}

function TypingIndicator() {
  return (
    <div className="flex justify-start mb-4">
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 rounded-full bg-amber-500 flex items-center justify-center text-white text-xs font-bold">A</div>
        <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3">
          <div className="flex gap-1 items-center h-4">
            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0ms]" />
            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:150ms]" />
            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:300ms]" />
          </div>
        </div>
      </div>
    </div>
  )
}

export function ChatWindow({ messages, isLoading, error, contentType, onContentTypeChange, onSend }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)
  const scrollContainerRef = useRef<HTMLDivElement>(null)
  const [suggestedPrompt, setSuggestedPrompt] = useState<string | undefined>()
  const userScrolledUp = useRef(false)
  const prevMessageCount = useRef(messages.length)

  // When a new user message is added, always snap to bottom and reset the flag
  useEffect(() => {
    if (messages.length > prevMessageCount.current) {
      userScrolledUp.current = false
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
    prevMessageCount.current = messages.length
  }, [messages.length])

  // During streaming (content growing), only scroll if user hasn't scrolled up
  useEffect(() => {
    if (!userScrolledUp.current) {
      bottomRef.current?.scrollIntoView({ behavior: 'instant' })
    }
  }, [messages])

  const handleScroll = () => {
    const el = scrollContainerRef.current
    if (!el) return
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight
    userScrolledUp.current = distanceFromBottom > 80
  }

  const handleModuleSelect = (type: ContentType, prefill?: string) => {
    onContentTypeChange(type)
    if (prefill) setSuggestedPrompt(prefill)
  }

  const handleSend = (text: string, ct: ContentType) => {
    setSuggestedPrompt(undefined)
    onSend(text, ct)
  }

  const showSelector = messages.length === 0 && !isLoading

  return (
    <div className="flex flex-col h-full">
      <div ref={scrollContainerRef} onScroll={handleScroll} className="flex-1 overflow-y-auto px-4 py-4 bg-gray-50">
        <div className="max-w-3xl mx-auto h-full">
          {showSelector ? (
            <ModuleSelector onSelect={handleModuleSelect} />
          ) : (
            <>
              {messages.map((msg, i) => <MessageBubble key={i} message={msg} />)}
              {isLoading && messages[messages.length - 1]?.content === '' && <TypingIndicator />}
              {error && <p className="text-center text-sm text-red-500 mt-2">Error: {error}</p>}
              <div ref={bottomRef} />
            </>
          )}
        </div>
      </div>
      <InputBar
        onSend={handleSend}
        isLoading={isLoading}
        contentType={contentType}
        onContentTypeChange={onContentTypeChange}
        suggestedPrompt={suggestedPrompt}
      />
    </div>
  )
}
