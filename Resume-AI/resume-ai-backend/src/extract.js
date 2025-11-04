import pdf from "pdf-parse";
import mammoth from "mammoth";

export async function extractTextFromBuffer(filename, buf) {
  if (!buf || !(buf instanceof Buffer) || buf.length === 0) {
    throw new Error("extractTextFromBuffer: empty buffer");
  }
  const lower = (filename || "").toLowerCase();
  if (lower.endsWith(".pdf")) {
    const parsed = await pdf(buf);   // MUST be a Buffer
    return parsed.text;
  }
  if (lower.endsWith(".docx")) {
    const { value } = await mammoth.extractRawText({ buffer: buf });
    return value;
  }
  return buf.toString("utf8");
}
