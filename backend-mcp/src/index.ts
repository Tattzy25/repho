import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

let status = "stopped";

app.post("/start", (_req, res) => {
  status = "running";
  res.json({ status });
});

app.post("/pause", (_req, res) => {
  status = "paused";
  res.json({ status });
});

app.post("/stop", (_req, res) => {
  status = "stopped";
  res.json({ status });
});

app.get("/status", (_req, res) => {
  res.json({ status });
});

const port = process.env.PORT || 3001;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
