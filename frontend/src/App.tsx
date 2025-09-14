import React from "react";
import { Button } from "./components/ui/button";
import ChatPanel from "./ChatPanel";

const API_BASE = "http://localhost:3001";

export default function App() {
  const send = async (endpoint: string) => {
    await fetch(`${API_BASE}/${endpoint}`, { method: "POST" });
  };

  return (
    <div className="p-4 space-y-6">
      <div className="flex gap-4">
        <Button onClick={() => send("start")}>Start</Button>
        <Button onClick={() => send("pause")}>Pause</Button>
        <Button onClick={() => send("stop")}>Stop</Button>
      </div>
      <div className="space-y-2">
        <h2 className="text-lg font-semibold">Keep these backend commands running</h2>
        <pre className="bg-neutral-900 text-neutral-100 p-3 rounded">python backend/orchestrator.py</pre>
        <pre className="bg-neutral-900 text-neutral-100 p-3 rounded">uvicorn backend.server:app --host 0.0.0.0 --port 8000 --reload</pre>
        <p className="text-sm text-neutral-500">(Run once if first time) <code>python backend/infra/init_redis_streams.py</code></p>
      </div>
      <ChatPanel />
    </div>
  );
}
