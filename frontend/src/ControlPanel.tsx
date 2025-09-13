import React from 'react'

const ControlPanel: React.FC = () => (
  <div className="space-y-4">
    <h2 className="text-xl font-bold">Control Panel</h2>
    <ol className="list-decimal list-inside space-y-2">
      <li>
        Start Redis streams
        <pre className="bg-gray-100 p-2 rounded">python backend/infra/init_redis_streams.py</pre>
      </li>
      <li>
        Run the orchestrator
        <pre className="bg-gray-100 p-2 rounded">python backend/orchestrator.py</pre>
      </li>
      <li>
        Launch the API server
        <pre className="bg-gray-100 p-2 rounded">uvicorn backend.server:app --reload</pre>
      </li>
      <li>
        Start the UI
        <pre className="bg-gray-100 p-2 rounded">npm run dev</pre>
      </li>
    </ol>
    <p>Keep these commands running. Error messages will appear as toasts.</p>
  </div>
)

export default ControlPanel
