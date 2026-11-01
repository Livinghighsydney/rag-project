import { useState, useEffect, useCallback } from 'react'
import type { Message, ContentType } from '../types'
import { streamMessage } from '../services/api'
import { clearSession as apiClear } from '../services/api'

const storageKey = (id: string) => `chat_messages_${id}`

export function useChat(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const stored = localStorage.getItem(storageKey(sessionId))
    setMessages(stored ? (JSON.parse(stored) as Message[]) : [])
    setError(null)
  }, [sessionId])

  const persist = (msgs: Message[]) =>
    localStorage.setItem(storageKey(sessionId), JSON.stringify(msgs))

  const sendMessage = useCallback(
    async (text: string, contentType: ContentType) => {
      const userMsg: Message = { role: 'user', content: text, timestamp: Date.now(), contentType }
      const withUser = [...messages, userMsg]
      setMessages(withUser)
      persist(withUser)
      setIsLoading(true)
      setError(null)

      const assistantMsg: Message = {
        role: 'assistant',
        content: '',
        timestamp: Date.now(),
        contentType,
      }
      setMessages([...withUser, assistantMsg])

      try {
        let fullContent = ''
        for await (const chunk of streamMessage(sessionId, text, contentType)) {
          fullContent += chunk
          setMessages([
            ...withUser,
            { ...assistantMsg, content: fullContent },
          ])
        }
        const final = [...withUser, { ...assistantMsg, content: fullContent }]
        persist(final)
      } catch (e) {
        setMessages(withUser)
        setError(e instanceof Error ? e.message : 'Request failed')
      } finally {
        setIsLoading(false)
      }
    },
    [sessionId, messages],
  )

  const clearHistory = useCallback(async () => {
    await apiClear(sessionId).catch(() => null)
    localStorage.removeItem(storageKey(sessionId))
    setMessages([])
    setError(null)
  }, [sessionId])

  return { messages, isLoading, error, sendMessage, clearHistory }
}
