import React from 'react'
import ChatPanel from './ChatPanel'
import ControlPanel from './ControlPanel'

const App: React.FC = () => (
  <div className="p-4 space-y-8">
    <ControlPanel />
    <ChatPanel />
  </div>
)

export default App
