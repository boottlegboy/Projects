import { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";
import dotenv from "dotenv";
dotenv.config();

export const s3 = new S3Client({ region: process.env.AWS_REGION || "us-east-1" });
const BUCKET = process.env.S3_BUCKET;

export async function uploadBuffer(key, buf, contentType = "application/octet-stream") {
  await s3.send(new PutObjectCommand({
    Bucket: BUCKET, Key: key, Body: buf, ContentType: contentType, ServerSideEncryption: "AES256"
  }));
  return `s3://${BUCKET}/${key}`;
}

export async function getObjectBuffer(key) {
  const out = await s3.send(new GetObjectCommand({ Bucket: BUCKET, Key: key }));
  const chunks = [];
  for await (const c of out.Body) chunks.push(c);
  return Buffer.concat(chunks);
}

export async function deleteObject(key) {
  await s3.send(new DeleteObjectCommand({ Bucket: BUCKET, Key: key }));
}
