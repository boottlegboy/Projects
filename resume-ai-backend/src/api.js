import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { nanoid } from "nanoid";
import { getDb } from "./db.js";
import { uploadBuffer } from "./s3.js";
import { ObjectId } from "mongodb";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// CORS: wide-open for local dev; we'll lock this down later.
app.use(cors());
app.use(express.json({ limit: "1mb" }));

// Health check
app.get("/health", (_req, res) => res.json({ ok: true }));

// Create a review job (paste-only in Step 1)
app.post("/api/reviews", async (req, res) => {
  try {
    const { resumeText, jobDescription, fileBase64, filename } = req.body || {};
    if (!resumeText && !fileBase64) {
      return res.status(400).json({ error: "Provide resumeText or fileBase64+filename" });
    }

    const now = new Date();
    const expiresAt = new Date(now.getTime() + 72 * 3600 * 1000);

    let source = "paste";
    let s3Key = null;
    let contentType = "application/octet-stream";

    if (fileBase64) {
      if (!filename) return res.status(400).json({ error: "filename is required with fileBase64" });
      const ext = filename.split(".").pop().toLowerCase();
      if (!["pdf","docx","doc","txt"].includes(ext)) {
        return res.status(415).json({ error: "Unsupported file type" });
      }
      source = "upload";
      if (ext === "pdf") contentType = "application/pdf";
      if (ext === "docx") contentType = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
      if (ext === "doc") contentType = "application/msword";
      if (ext === "txt") contentType = "text/plain";

      const key = `uploads/${Date.now()}-${Math.random().toString(36).slice(2)}.${ext}`;
      const buf = Buffer.from(fileBase64, "base64");
      await uploadBuffer(key, buf, contentType);
      s3Key = key;
    }

    const doc = {
      status: "queued",
      source,
      s3Key,
      resumeText: resumeText?.trim() || null,
      jobDescription: (jobDescription || "").trim(),
      result: null,
      error: null,
      createdAt: now,
      updatedAt: now,
      expiresAt
    };

    const db = await getDb();
    const { insertedId } = await db.collection("resume_reviews").insertOne(doc);
    res.json({ id: insertedId.toString() });
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "failed to create review" });
  }
});


// Read review status/result
app.get("/api/reviews/:id", async (req, res) => {
  try {
    const db = await getDb();
    const doc = await db.collection("resume_reviews").findOne(
      { _id: new ObjectId(req.params.id) },
      { projection: { resumeText: 0 } } // don’t echo raw resume text
    );
    if (!doc) return res.status(404).json({ error: "not found" });

    res.json({
      id: doc._id.toString(),
      status: doc.status,
      result: doc.result,
      error: doc.error
    });
  } catch (e) {
    return res.status(400).json({ error: "bad id" });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Local API listening on http://localhost:${PORT}`);
});
