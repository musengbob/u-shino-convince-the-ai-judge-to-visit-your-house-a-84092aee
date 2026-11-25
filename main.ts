// Convince the AI Judge to Visit Your House — entry program (Node 22).
//
// The entry is the image file entry.png sitting next to this script: a warm,
// funny invitation letter to the AI judge, drawn from scratch in code by
// compose.py (Pillow, deterministic — re-running compose.py always produces
// the same bytes).
//
// This program copies that image to $MAKEFUN_OUTPUT_DIR/entry.png, which is
// where the grader looks for the entry. The gate: a whole PNG, at most
// 1 MiB (1,048,576 bytes) and 1024 by 1024 pixels.
//
// Local check (outside the grader's container, /output stands in for it):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const source = new URL("./entry.png", import.meta.url);

// Resolve where the entry goes. The grader runs the program with
// $MAKEFUN_OUTPUT_DIR set to its writable output directory and reads the
// entry from there, so that wins; $OUTPUT_PATH is a second explicit
// override; a local output/ next to this file is the fallback for runs
// on a dev machine.
function resolveOutputPath(): string {
  const fromEnv = process.env.MAKEFUN_OUTPUT_DIR;
  if (fromEnv !== undefined && fromEnv.trim() !== "") {
    return join(fromEnv, "entry.png");
  }
  const legacy = process.env.OUTPUT_PATH;
  if (legacy !== undefined && legacy.trim() !== "") {
    return legacy;
  }
  return join(process.cwd(), "output", "entry.png");
}

const outPath = resolveOutputPath();
mkdirSync(join(outPath, ".."), { recursive: true });

copyFileSync(source, outPath);

// Validate the copy against the competition gate: a whole PNG, 1024x1024,
// at most 1 MiB (1,048,576 bytes). The PNG width/height live in the IHDR
// chunk at byte offsets 16 and 20 (big-endian uint32), right after the
// 8-byte PNG magic. Exits 1 with a plain message on any failure.
function validateEntry(bytes: Buffer, size: number): void {
  const PNG_MAGIC = Buffer.from([
    0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
  ]);
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    console.error("Validation failed: entry.png is not a PNG.");
    process.exit(1);
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width !== 1024 || height !== 1024) {
    console.error(`Validation failed: ${width}x${height}, must be 1024x1024.`);
    process.exit(1);
  }
  if (size > 1048576) {
    console.error(`Validation failed: ${size} bytes, over the 1 MiB gate.`);
    process.exit(1);
  }
  console.log(`Wrote ${size} bytes to ${outPath} (${width}x${height}).`);
  console.log("Validation passed: whole PNG, 1024x1024, within 1 MiB.");
}

const bytes = readFileSync(outPath);
const size = statSync(outPath).size;
validateEntry(bytes, size);
