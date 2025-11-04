import { MongoClient } from "mongodb";
import dotenv from "dotenv";
dotenv.config();

async function main() {
  const client = new MongoClient(process.env.MONGODB_URI);
  await client.connect();
  const db = client.db(process.env.MONGODB_DB || "resume_ai");
  const coll = db.collection("resume_reviews");

  // Delete when expiresAt < now (0 seconds after)
  await coll.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });

  // Helpful extra indexes
  await coll.createIndex({ status: 1 });
  await coll.createIndex({ createdAt: 1 });

  console.log("Indexes created");
  await client.close();
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
