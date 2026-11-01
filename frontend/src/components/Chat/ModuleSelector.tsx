import type { ContentType } from '../../types'
import { CONTENT_MODES } from '../../types'

interface FeaturedModule {
  type: ContentType
  title: string
  tagline: string
  description: string
  accent: string
  badge: string
  examples: string[]
}

const FEATURED: FeaturedModule[] = [
  {
    type: 'playbook',
    title: 'Execution Playbook',
    tagline: 'Step-by-step operating manual',
    badge: 'Business Lab',
    accent: 'blue',
    description:
      'Get a complete implementation guide — exact steps, fill-in-the-blank templates, checklists, success metrics, and troubleshooting. Execute a complex system starting today.',
    examples: [
      'Build a lead generation system from scratch',
      'Implement Profit First cash management',
      'Create a team hiring and onboarding process',
      'Set up a content marketing machine',
    ],
  },
  {
    type: 'training_lesson',
    title: 'Training Lesson',
    tagline: 'Certification-level structured module',
    badge: 'Business Lab',
    accent: 'amber',
    description:
      'Full structured lesson with core concept, named framework, worksheet with fill-in-the-blank fields, 6-step real-world application, and your action step this week.',
    examples: [
      'How Profit First permanently fixes cash flow',
      'The lead generation system from 100M Leads',
      'How to build a business that runs without you',
      'The customer value journey — all 8 stages',
    ],
  },
]

const OTHER_MODES: ContentType[] = ['coaching', 'linkedin', 'instagram', 'twitter', 'email', 'framework']

interface Props {
  onSelect: (type: ContentType, prefill?: string) => void
}

function AccentBar({ color }: { color: string }) {
  return (
    <div
      className={`h-1 w-full rounded-t-xl ${color === 'blue' ? 'bg-blue-600' : 'bg-amber-500'}`}
    />
  )
}

export function ModuleSelector({ onSelect }: Props) {
  return (
    <div className="flex flex-col items-center justify-center h-full px-6 py-8 overflow-y-auto">
      <div className="w-full max-w-3xl">

        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-amber-100 text-amber-600 font-bold text-xl mb-3">
            A
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Business Growth Lab</h1>
          <p className="text-gray-500 text-sm mt-1 max-w-md mx-auto">
            Powered by 100+ business books. Choose what you want to create.
          </p>
        </div>

        {/* Featured modules */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {FEATURED.map((mod) => (
            <div
              key={mod.type}
              className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow overflow-hidden cursor-pointer group"
              onClick={() => onSelect(mod.type)}
            >
              <AccentBar color={mod.accent} />
              <div className="p-5">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <span
                      className={`text-xs font-semibold uppercase tracking-wide ${
                        mod.accent === 'blue' ? 'text-blue-600' : 'text-amber-600'
                      }`}
                    >
                      {mod.badge}
                    </span>
                    <h2 className="text-lg font-bold text-gray-900 mt-0.5">{mod.title}</h2>
                    <p className="text-xs text-gray-500 font-medium">{mod.tagline}</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 leading-relaxed mb-4">{mod.description}</p>
                <div>
                  <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">
                    Try asking:
                  </p>
                  <div className="flex flex-col gap-1.5">
                    {mod.examples.map((ex) => (
                      <button
                        key={ex}
                        onClick={(e) => {
                          e.stopPropagation()
                          onSelect(mod.type, ex)
                        }}
                        className={`text-left text-xs px-3 py-2 rounded-lg border transition-colors ${
                          mod.accent === 'blue'
                            ? 'border-blue-100 bg-blue-50 text-blue-700 hover:bg-blue-100'
                            : 'border-amber-100 bg-amber-50 text-amber-700 hover:bg-amber-100'
                        }`}
                      >
                        {ex}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Other modes */}
        <div className="border-t border-gray-100 pt-5">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide text-center mb-3">
            Also available
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {OTHER_MODES.map((type) => {
              const mode = CONTENT_MODES.find((m) => m.type === type)!
              return (
                <button
                  key={type}
                  onClick={() => onSelect(type)}
                  className="px-4 py-2 rounded-full border border-gray-200 text-sm text-gray-600 hover:border-blue-400 hover:text-blue-600 hover:bg-blue-50 transition-colors bg-white"
                >
                  {mode.label}
                </button>
              )
            })}
          </div>
        </div>

      </div>
    </div>
  )
}
