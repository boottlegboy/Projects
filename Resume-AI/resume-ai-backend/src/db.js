import { MongoClient } from "mongodb";
import dotenv from "dotenv";
dotenv.config();

let client;
export async function getDb() {
  if (!client) {
    client = new MongoClient(process.env.MONGODB_URI, { maxPoolSize: 5 });
    await client.connect();
  }
  return client.db(process.env.MONGODB_DB || "resume_ai");
}
