import { useCallback, useEffect, useRef, useState } from 'react'
import './App.css'

type Role = 'user' | 'assistant'

interface ChatMessage {
  id: string
  role: Role
  text: string
}

function buildMockPost(topic: string): string {
  const t = topic.trim()
  return [
    `You asked for a post on: ${t}`,
    '',
    'Most teams treat LinkedIn like a checklist. The ones that win treat it like a weekly editorial decision: one idea, one point of view, one clear ask.',
    '',
    `If you're writing about ${t}, start with a single sharp sentence someone would stop for—then earn the next lines with specifics (what you tried, what broke, what you learned).`,
    '',
    'What is the one takeaway you want readers to remember after 10 seconds?',
  ].join('\n')
}

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)
  const listEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = useCallback(() => {
    listEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, busy, scrollToBottom])

  const send = useCallback(async () => {
    const topic = input.trim()
    if (!topic || busy) return

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      text: topic,
    }
    setMessages((m) => [...m, userMsg])
    setInput('')
    setBusy(true)

    await new Promise((r) => setTimeout(r, 650))

    const assistantMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'assistant',
      text: buildMockPost(topic),
    }
    setMessages((m) => [...m, assistantMsg])
    setBusy(false)
  }, [input, busy])

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      void send()
    }
  }

  const showPreviewLabel = messages.length > 0
  const showEmpty = messages.length === 0 && !busy

  return (
    <div className="screen" data-node-id="1:2">
      <header className="header" data-node-id="1:3">
        <h1 className="headerTitle" data-node-id="1:4">
          Linkedin Content Writer
        </h1>
      </header>

      <div
        className="messages"
        role="log"
        aria-live="polite"
        aria-relevant="additions"
        data-node-id="1:5"
      >
        {showEmpty && (
          <p className="emptyHint">
            Enter a topic below and tap <strong>Send</strong> to see a draft-style
            response (demo — wire your Crew backend later).
          </p>
        )}

        {showPreviewLabel && (
          <p className="previewLabel" data-node-id="3:8">
            Generated post (preview)
          </p>
        )}

        {messages.map((msg) =>
          msg.role === 'user' ? (
            <div key={msg.id} className="row rowUser" data-name="Row / user">
              <div className="bubbleUser">{msg.text}</div>
            </div>
          ) : (
            <div key={msg.id} className="row rowAssistant" data-name="Row / assistant">
              <div className="bubbleAssistant">{msg.text}</div>
            </div>
          ),
        )}

        {busy && <div className="typing">Writing…</div>}
        <div ref={listEndRef} />
      </div>

      <div className="composer" data-node-id="1:6">
        <label className="topicField" data-node-id="1:7">
          <span className="visually-hidden">Topic</span>
          <input
            className="topicInput"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="What topic should your LinkedIn post cover?"
            disabled={busy}
            autoComplete="off"
            aria-label="Topic for your LinkedIn post"
            data-node-id="1:8"
          />
        </label>
        <button
          type="button"
          className="sendBtn"
          onClick={() => void send()}
          disabled={busy || !input.trim()}
          data-node-id="1:9"
        >
          Send
        </button>
      </div>
    </div>
  )
}
