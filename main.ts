// main.ts: copy ./entry.png to $MAKEFUN_OUTPUT_DIR as entry.png.
// Node 22, standard library only. No network, no dependencies.
// Validates the file exists and starts with PNG or JPEG magic bytes.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const JPEG_MAGIC = Buffer.from([0xff, 0xd8, 0xff]);

function fail(message: string): never {
  console.error(`main.ts: ERROR: ${message}`);
  process.exit(1);
}

const source = resolve("entry.png");
if (!existsSync(source)) {
  fail(`entry.png not found at ${source}. Run generate_image.py first.`);
}

const data = readFileSync(source);
const head = data.subarray(0, 8);
const isPng = head.subarray(0, 8).equals(PNG_MAGIC);
const isJpeg = head.subarray(0, 3).equals(JPEG_MAGIC);
if (!isPng && !isJpeg) {
  fail("entry.png does not start with PNG or JPEG magic bytes, refusing to copy.");
}
if (data.length > 1048576) {
  fail(`entry.png is ${data.length} bytes, over the 1 MiB bounty limit, refusing to copy.`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(source, dest);

const size = statSync(dest).size;
if (size !== data.length) {
  fail(`copied size ${size} does not match source size ${data.length}.`);
}
console.log(`main.ts: copied entry.png (${isPng ? "PNG" : "JPEG"}, ${size} bytes) to ${dest}`);
