import { useState } from 'react'
import type { SessionMeta } from '../../types'

interface Props {
  sessions: SessionMeta[]
  activeId: string
  onSelect: (id: string) => void
  onNewChat: () => void
  onDelete: (id: string) => void
}

export function Sidebar({ sessions, activeId, onSelect, onNewChat, onDelete }: Props) {
  const [hoveredId, setHoveredId] = useState<string | null>(null)

  return (
    <aside className="w-60 shrink-0 bg-gray-900 flex flex-col h-full">
      <div className="p-3 border-b border-gray-700">
        <button
          onClick={onNewChat}
          className="w-full text-sm bg-gray-700 hover:bg-gray-600 text-white rounded-lg px-3 py-2 transition-colors text-left"
        >
          + New conversation
        </button>
      </div>

      <div className="flex-1 overflow-y-auto py-2">
        {sessions.length === 0 && (
          <p className="text-gray-500 text-xs px-4 pt-4">No conversations yet</p>
        )}
        {sessions.map((s) => (
          <div
            key={s.id}
            className="relative"
            onMouseEnter={() => setHoveredId(s.id)}
            onMouseLeave={() => setHoveredId(null)}
          >
            <button
              onClick={() => onSelect(s.id)}
              className={`w-full text-left px-4 py-3 text-sm transition-colors pr-9 ${
                s.id === activeId
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <p className="truncate font-medium">{s.title}</p>
              <p className="text-xs text-gray-500 mt-0.5">
                {new Date(s.createdAt).toLocaleDateString()}
              </p>
            </button>
            {hoveredId === s.id && (
              <button
                onClick={(e) => { e.stopPropagation(); onDelete(s.id) }}
                className="absolute right-2 top-1/2 -translate-y-1/2 w-6 h-6 flex items-center justify-center text-gray-500 hover:text-white hover:bg-gray-600 rounded transition-colors text-xs"
                title="Delete conversation"
              >
                ×
              </button>
            )}
          </div>
        ))}
      </div>

      <div className="p-3 border-t border-gray-700">
        <p className="text-xs text-gray-600 text-center">Business Growth Advisor</p>
      </div>
    </aside>
  )
}
