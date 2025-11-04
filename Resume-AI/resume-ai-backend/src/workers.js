import dotenv from "dotenv";
dotenv.config();

import { ObjectId } from "mongodb";
import { getDb } from "./db.js";
import { getObjectBuffer, deleteObject } from "./s3.js";
import { extractTextFromBuffer } from "./extract.js";
import { buildPrompt, callLLM } from "./llm.js";

const INTERVAL_MS = 2000; // check every 2s

async function processOne() {
  const db = await getDb();
  const coll = db.collection("resume_reviews");

  // atomically claim one queued doc
  const doc = await coll.findOneAndUpdate(
    { status: "queued", s3Key: null },
    { $set: { status: "processing", updatedAt: new Date() } },
    { returnDocument: "after" }
  );

  if (!doc.value) return; // nothing to do
  const job = doc.value;

  try {
    console.log("JOB:", { id: String(job._id), s3Key: job.s3Key, hasResumeText: !!job.resumeText });

    if (!text && job.s3Key) {
      console.log("Downloading from S3:", job.s3Key);
      const buf = await getObjectBuffer(job.s3Key);
      console.log("S3 buffer length:", buf?.length, "isBuffer:", Buffer.isBuffer(buf));
      if (!buf || !Buffer.isBuffer(buf) || buf.length === 0) {
        throw new Error(`S3 object empty or missing for key ${job.s3Key}`);
      }
      text = await extractTextFromBuffer(job.s3Key, buf);
    }

    if (!text || text.trim().length < 20) {
      throw new Error("Failed to extract resume text");
    }

    const prompt = buildPrompt(text, job.jobDescription);
    const result = await callLLM(prompt);

    await coll.updateOne(
      { _id: new ObjectId(job._id) },
      { $set: { status: "done", result, updatedAt: new Date() } }
    );

    // Optional: delete file right after processing (or keep until TTL)
    // if (job.s3Key) await deleteObject(job.s3Key);

    console.log(`Processed ${job._id}`);
  } catch (e) {
    console.error("Worker error:", e.message);
    await coll.updateOne(
      { _id: new ObjectId(job._id) },
      { $set: { status: "error", error: e.message, updatedAt: new Date() } }
    );
  }
}

async function loop() {
  console.log("Worker running. Checking for jobs every", INTERVAL_MS, "ms");
  setInterval(processOne, INTERVAL_MS);
}

loop();
