import { useState, useRef, useEffect, KeyboardEvent } from 'react'
import type { ContentType } from '../../types'
import { CONTENT_MODES, MODE_GROUPS } from '../../types'

interface Props {
  onSend: (text: string, contentType: ContentType) => void
  isLoading: boolean
  contentType: ContentType
  onContentTypeChange: (t: ContentType) => void
  suggestedPrompt?: string
}

export function InputBar({ onSend, isLoading, contentType, onContentTypeChange, suggestedPrompt }: Props) {
  const [value, setValue] = useState('')
  const [showModes, setShowModes] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (suggestedPrompt) {
      setValue(suggestedPrompt)
      setTimeout(() => {
        textareaRef.current?.focus()
        autoResize()
      }, 0)
    }
  }, [suggestedPrompt])

  const submit = () => {
    const text = value.trim()
    if (!text || isLoading) return
    onSend(text, contentType)
    setValue('')
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit() }
  }

  const autoResize = () => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`
  }

  const currentMode = CONTENT_MODES.find((m) => m.type === contentType)

  return (
    <div className="border-t border-gray-200 bg-white px-3 pt-2 pb-3 md:px-4 md:pt-3">
      <div className="max-w-3xl mx-auto">

        {/* Mode selector — scrollable pill row on desktop, toggle on mobile */}
        <div className="hidden md:flex items-center gap-1 overflow-x-auto pb-2 scrollbar-hide">
          {MODE_GROUPS.map((group, gi) => (
            <div key={gi} className="flex items-center shrink-0">
              {gi > 0 && <div className="w-px h-5 bg-gray-200 mx-2" />}
              <span className="text-xs text-gray-400 font-semibold uppercase tracking-wide mr-1.5 shrink-0">
                {group.label}
              </span>
              {group.modes.map((mode) => {
                const m = CONTENT_MODES.find((x) => x.type === mode)!
                return (
                  <button
                    key={mode}
                    onClick={() => onContentTypeChange(mode)}
                    className={`shrink-0 px-3 py-1 rounded-full text-xs font-medium transition-all border mr-1 ${
                      contentType === mode
                        ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                        : 'bg-white text-gray-500 border-gray-200 hover:border-blue-300 hover:text-blue-600'
                    }`}
                  >
                    {m.label}
                  </button>
                )
              })}
            </div>
          ))}
        </div>

        {/* Mobile: current mode chip + change button */}
        <div className="flex md:hidden items-center gap-2 pb-2">
          <span className="text-xs font-medium text-blue-600 bg-blue-50 border border-blue-100 rounded-full px-3 py-1">
            {currentMode?.label ?? 'Coaching'}
          </span>
          <button
            onClick={() => setShowModes((v) => !v)}
            className="text-xs text-gray-500 underline"
          >
            Change
          </button>
        </div>

        {/* Mobile mode picker dropdown */}
        {showModes && (
          <div className="md:hidden flex flex-wrap gap-1.5 pb-2">
            {CONTENT_MODES.map((m) => (
              <button
                key={m.type}
                onClick={() => { onContentTypeChange(m.type); setShowModes(false) }}
                className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                  contentType === m.type
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-gray-600 border-gray-200'
                }`}
              >
                {m.label}
              </button>
            ))}
          </div>
        )}

        {/* Input row */}
        <div className="flex items-end gap-2">
          <textarea
            ref={textareaRef}
            rows={1}
            value={value}
            onChange={(e) => { setValue(e.target.value); autoResize() }}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            placeholder={`${currentMode?.label ?? 'Coaching'}...`}
            className="flex-1 resize-none rounded-xl border border-gray-300 px-3 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 placeholder-gray-400"
          />
          <button
            onClick={submit}
            disabled={isLoading || !value.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white rounded-xl px-4 py-3 text-sm font-medium transition-colors shrink-0"
          >
            {isLoading ? '...' : 'Go'}
          </button>
        </div>
        <p className="hidden md:block text-xs text-gray-400 text-center mt-2">Shift+Enter for new line</p>
      </div>
    </div>
  )
}
