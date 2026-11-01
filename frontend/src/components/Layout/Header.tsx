interface Props {
  onNewChat: () => void
  onMenuOpen: () => void
}

export function Header({ onNewChat, onMenuOpen }: Props) {
  return (
    <header className="h-14 border-b border-gray-200 bg-white flex items-center justify-between px-4 shrink-0">
      <div className="flex items-center gap-3">
        {/* Hamburger — mobile only */}
        <button
          onClick={onMenuOpen}
          className="md:hidden flex flex-col gap-1.5 p-1 rounded text-gray-600 hover:text-gray-900"
          aria-label="Open menu"
        >
          <span className="block w-5 h-0.5 bg-current" />
          <span className="block w-5 h-0.5 bg-current" />
          <span className="block w-5 h-0.5 bg-current" />
        </button>
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-full bg-amber-500 flex items-center justify-center text-white text-xs font-bold">A</div>
          <span className="font-semibold text-gray-800 text-sm md:text-base">Business Growth Advisor</span>
        </div>
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
