import React from "react";
import { Button } from "./components/ui/button";

const API_BASE = "http://localhost:3001";

export default function App() {
  const send = async (endpoint: string) => {
    await fetch(`${API_BASE}/${endpoint}`, { method: "POST" });
  };

  return (
    <div className="flex gap-4 p-4">
      <Button onClick={() => send("start")}>Start</Button>
      <Button onClick={() => send("pause")}>Pause</Button>
      <Button onClick={() => send("stop")}>Stop</Button>
    </div>
  );
}
