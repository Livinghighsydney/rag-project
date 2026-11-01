import { useState } from 'react'
import type { SessionMeta } from '../../types'

interface Props {
  sessions: SessionMeta[]
  activeId: string
  onSelect: (id: string) => void
  onNewChat: () => void
  onDelete: (id: string) => void
  isOpen: boolean
  onClose: () => void
}

export function Sidebar({ sessions, activeId, onSelect, onNewChat, onDelete, isOpen, onClose }: Props) {
  const [hoveredId, setHoveredId] = useState<string | null>(null)

  const handleSelect = (id: string) => {
    onSelect(id)
    onClose()
  }

  const handleNewChat = () => {
    onNewChat()
    onClose()
  }

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-20 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar panel */}
      <aside
        className={`
          fixed inset-y-0 left-0 z-30 w-72 bg-gray-900 flex flex-col
          transform transition-transform duration-300 ease-in-out
          md:relative md:translate-x-0 md:w-60 md:z-auto md:shrink-0
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="p-3 border-b border-gray-700 flex items-center gap-2">
          <button
            onClick={handleNewChat}
            className="flex-1 text-sm bg-gray-700 hover:bg-gray-600 text-white rounded-lg px-3 py-2 transition-colors text-left"
          >
            + New conversation
          </button>
          <button
            onClick={onClose}
            className="md:hidden text-gray-400 hover:text-white p-2 rounded-lg hover:bg-gray-700 transition-colors"
          >
            ✕
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
                onClick={() => handleSelect(s.id)}
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
    </>
  )
}
