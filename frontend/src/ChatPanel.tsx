import React, { useEffect } from 'react'
import { toast } from './components/ui/sonner'

const ChatPanel: React.FC = () => {
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/errors')
    ws.addEventListener('open', () => {
      toast.success('Connected to orchestrator')
    })
    ws.addEventListener('message', event => {
      try {
        const data = JSON.parse(event.data)
        toast.error(`Job ${data.job_id} failed in phase ${data.phase}: ${data.error}`)
      } catch (err) {
        console.error('invalid message', err)
      }
    })
    ws.addEventListener('close', () => {
      toast.error('Disconnected from orchestrator')
    })
    ws.addEventListener('error', () => {
      toast.error('WebSocket error')
    })
    return () => ws.close()
  }, [])

  return (
    <div>
      <h1 className="text-xl font-bold">Error Alerts</h1>
      <p>Notifications appear in the top-right corner.</p>
    </div>
  )
}

export default ChatPanel
