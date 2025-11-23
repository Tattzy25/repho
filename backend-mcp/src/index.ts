import express from "express";
import cors from "cors";
import { exec } from "child_process";
import { WebSocketServer } from "ws";
import http from "http";
import fs from "fs";
import path from "path";

// Allow dashboard access from localhost during development and codehomie.chat in production.
const allowedOrigins = (process.env.ALLOWED_ORIGINS ||
  "http://localhost:8002,https://codehomie.chat").split(",");

const app = express();
app.use(
  cors({
    origin: (origin, callback) => {
      if (!origin || allowedOrigins.includes(origin)) callback(null, true);
      else callback(new Error("Not allowed by CORS"));
    },
  })
);
app.use(express.json());

let status = "stopped";

interface Connection {
  name: string;
  command: string;
  status: string;
}

const connectionsPath = path.join(__dirname, "../mcp-connections.json");
let connections: Connection[] = [];

function loadConnections() {
  if (fs.existsSync(connectionsPath)) {
    const raw = fs.readFileSync(connectionsPath, "utf-8");
    connections = JSON.parse(raw).connections || [];
  }
}

function saveConnections() {
  fs.writeFileSync(
    connectionsPath,
    JSON.stringify({ connections }, null, 2)
  );
}

async function testConnection(conn: Connection) {
  return new Promise<string>((resolve) => {
    exec(`${conn.command} --version`, { timeout: 10000 }, (err) => {
      conn.status = err ? "error" : "connected";
      resolve(conn.status);
    });
  });
}

loadConnections();
connections.forEach((c) => {
  c.status = "checking";
  testConnection(c).then(() => broadcastConnections());
});

function run(cmd: string) {
  return new Promise<string>((resolve, reject) => {
    exec(cmd, { cwd: process.cwd() }, (err, stdout, stderr) => {
      if (err) reject(stderr || err.message);
      else resolve(stdout);
    });
  });
}

function broadcast(message: string) {
  wss.clients.forEach((client) => {
    if (client.readyState === 1) client.send(message);
  });
}

function broadcastConnections() {
  broadcast(`connections:${JSON.stringify(connections)}`);
}

app.post("/start", (_req, res) => {
  status = "running";
  broadcast(`status:${status}`);
  res.json({ status });
});

app.post("/pause", (_req, res) => {
  status = "paused";
  broadcast(`status:${status}`);
  res.json({ status });
});

app.post("/stop", (_req, res) => {
  status = "stopped";
  broadcast(`status:${status}`);
  res.json({ status });
});

app.post("/install", async (_req, res) => {
  try {
    const output = await run("npm install");
    res.json({ output });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

app.post("/build", async (_req, res) => {
  try {
    const output = await run("npm run build");
    res.json({ output });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

app.post("/run", async (_req, res) => {
  try {
    const output = await run("npm start");
    res.json({ output });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

app.get("/status", (_req, res) => {
  res.json({ status });
});

app.get("/tools", (_req, res) => {
  const cfg = fs.readFileSync(
    path.join(__dirname, "../mcp-tools.json"),
    "utf-8"
  );
  res.type("application/json").send(cfg);
});

app.get("/connections", (_req, res) => {
  res.json({ connections });
});

app.post("/connections", async (req, res) => {
  const { name, command } = req.body;
  if (!name || !command) {
    return res.status(400).json({ error: "name and command required" });
  }
  const existing = connections.find((c) => c.name === name);
  if (existing) {
    return res.status(409).json({ error: "connection exists" });
  }
  const conn: Connection = { name, command, status: "checking" };
  connections.push(conn);
  await testConnection(conn);
  saveConnections();
  broadcastConnections();
  res.json(conn);
});

app.post("/connections/:name/test", async (req, res) => {
  const conn = connections.find((c) => c.name === req.params.name);
  if (!conn) return res.status(404).json({ error: "not found" });
  conn.status = "checking";
  await testConnection(conn);
  saveConnections();
  broadcastConnections();
  res.json(conn);
});

const server = http.createServer(app);
const wss = new WebSocketServer({ server });

wss.on("connection", (ws) => {
  ws.send(`status:${status}`);
  ws.send(`connections:${JSON.stringify(connections)}`);
  ws.on("message", (msg) => {
    const text = msg.toString();
    if (text.includes("status")) {
      ws.send(`status:${status}`);
    } else {
      ws.send(`echo:${text}`);
    }
  });
});

const port = process.env.PORT || 3001;
server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
