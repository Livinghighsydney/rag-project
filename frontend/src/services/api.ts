import type { ChatResponse, ContentType } from '../types'

const BASE = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, options)
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`)
  return res.json() as Promise<T>
}

export function sendMessage(
  sessionId: string,
  message: string,
  contentType: ContentType,
): Promise<ChatResponse> {
  return request<ChatResponse>('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message, content_type: contentType }),
  })
}

export function clearSession(sessionId: string): Promise<void> {
  return request<void>(`/chat/history/${sessionId}`, { method: 'DELETE' })
}

export async function* streamMessage(
  sessionId: string,
  message: string,
  contentType: ContentType,
): AsyncGenerator<string> {
  const res = await fetch(`${BASE}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message, content_type: contentType }),
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`)

  const reader = res.body!.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() ?? ''
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      const payload = line.slice(6)
      if (payload === '[DONE]') return
      try {
        const parsed = JSON.parse(payload) as { c?: string; error?: string }
        if (parsed.error) throw new Error(parsed.error)
        if (parsed.c) yield parsed.c
      } catch {
        // ignore malformed lines
      }
    }
  }
}
