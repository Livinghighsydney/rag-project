export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  contentType?: ContentType
}

export interface ChatRequest {
  session_id: string
  message: string
  content_type: ContentType
}

export interface ChatResponse {
  session_id: string
  answer: string
  content_type: string
}

export interface SessionMeta {
  id: string
  title: string
  createdAt: number
}

export type ContentType =
  | 'coaching'
  | 'linkedin'
  | 'instagram'
  | 'twitter'
  | 'email'
  | 'training_lesson'
  | 'playbook'
  | 'framework'

export interface ContentMode {
  type: ContentType
  label: string
  description: string
}

export interface ModeGroup {
  label: string
  modes: ContentType[]
}

export const CONTENT_MODES: ContentMode[] = [
  { type: 'coaching',       label: 'Coaching',        description: 'Full strategic coaching session' },
  { type: 'linkedin',       label: 'LinkedIn Post',   description: 'LinkedIn post' },
  { type: 'instagram',      label: 'Instagram',       description: 'Instagram caption' },
  { type: 'twitter',        label: 'Twitter Thread',  description: 'Twitter/X thread' },
  { type: 'email',          label: 'Email Campaign',  description: 'Email newsletter' },
  { type: 'training_lesson',label: 'Training Lesson', description: 'Full course lesson with framework' },
  { type: 'playbook',       label: 'Playbook',        description: 'Step-by-step execution guide' },
  { type: 'framework',      label: 'Framework',       description: 'Visual framework & reference card' },
]

export const MODE_GROUPS: ModeGroup[] = [
  { label: 'Coaching',      modes: ['coaching'] },
  { label: 'Social Media',  modes: ['linkedin', 'instagram', 'twitter'] },
  { label: 'Email',         modes: ['email'] },
  { label: 'Business Lab',  modes: ['training_lesson', 'playbook', 'framework'] },
]
