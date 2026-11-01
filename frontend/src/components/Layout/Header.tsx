interface Props {
  onNewChat: () => void
}

export function Header({ onNewChat }: Props) {
  return (
    <header className="h-14 border-b border-gray-200 bg-white flex items-center justify-between px-4 shrink-0">
      <div className="flex items-center gap-2">
        <div className="w-7 h-7 rounded-full bg-amber-500 flex items-center justify-center text-white text-xs font-bold">A</div>
        <span className="font-semibold text-gray-800">Business Growth Advisor</span>
      </div>
      <button
        onClick={onNewChat}
        className="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors"
      >
        + New Chat
      </button>
    </header>
  )
}
