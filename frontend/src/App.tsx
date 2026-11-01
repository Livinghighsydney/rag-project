import { useState, useCallback } from 'react'
import { v4 as uuidv4 } from 'uuid'
import type { SessionMeta, ContentType } from './types'
import { Sidebar } from './components/Layout/Sidebar'
import { Header } from './components/Layout/Header'
import { ChatWindow } from './components/Chat/ChatWindow'
import { useChat } from './hooks/useChat'

const SESSIONS_KEY = 'chat_sessions'

function loadSessions(): SessionMeta[] {
  try {
    return JSON.parse(localStorage.getItem(SESSIONS_KEY) ?? '[]') as SessionMeta[]
  } catch {
    return []
  }
}

function saveSessions(sessions: SessionMeta[]) {
  localStorage.setItem(SESSIONS_KEY, JSON.stringify(sessions))
}

function getOrCreateSession(sessions: SessionMeta[]): { id: string; sessions: SessionMeta[] } {
  if (sessions.length > 0) return { id: sessions[0].id, sessions }
  const id = uuidv4()
  const next = [{ id, title: 'New conversation', createdAt: Date.now() }]
  saveSessions(next)
  return { id, sessions: next }
}

export default function App() {
  const [sessions, setSessions] = useState<SessionMeta[]>(() => {
    const loaded = loadSessions()
    return getOrCreateSession(loaded).sessions
  })
  const [activeId, setActiveId] = useState<string>(() => {
    return getOrCreateSession(loadSessions()).id
  })
  const [contentType, setContentType] = useState<ContentType>('coaching')

  const { messages, isLoading, error, sendMessage } = useChat(activeId)

  const handleSend = useCallback(
    (text: string, ct: ContentType) => {
      const isNew = sessions.find((s) => s.id === activeId)?.title === 'New conversation'
      if (isNew) {
        const updated = sessions.map((s) =>
          s.id === activeId ? { ...s, title: text.slice(0, 50) } : s,
        )
        setSessions(updated)
        saveSessions(updated)
      }
      sendMessage(text, ct)
    },
    [activeId, sessions, sendMessage],
  )

  const newChat = useCallback(() => {
    const id = uuidv4()
    const next = [{ id, title: 'New conversation', createdAt: Date.now() }, ...sessions]
    setSessions(next)
    saveSessions(next)
    setActiveId(id)
    setContentType('coaching')
  }, [sessions])

  const deleteSession = useCallback((id: string) => {
    const updated = sessions.filter((s) => s.id !== id)
    localStorage.removeItem(`chat_messages_${id}`)
    if (updated.length === 0) {
      const newId = uuidv4()
      const fresh = [{ id: newId, title: 'New conversation', createdAt: Date.now() }]
      setSessions(fresh)
      saveSessions(fresh)
      setActiveId(newId)
    } else {
      setSessions(updated)
      saveSessions(updated)
      if (id === activeId) setActiveId(updated[0].id)
    }
  }, [sessions, activeId])

  return (
    <div className="flex h-screen overflow-hidden bg-white">
      <Sidebar sessions={sessions} activeId={activeId} onSelect={setActiveId} onNewChat={newChat} onDelete={deleteSession} />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header onNewChat={newChat} />
        <div className="flex-1 overflow-hidden">
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            error={error}
            contentType={contentType}
            onContentTypeChange={setContentType}
            onSend={handleSend}
          />
        </div>
      </div>
    </div>
  )
}
