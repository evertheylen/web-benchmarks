// adapted from https://bun.sh/guides/http/cluster

import { spawn } from "bun";
const { cpus } = require('./common.js');

const buns = new Array(cpus);

for (let i = 0; i < cpus; i++) {
  buns[i] = spawn({
    cmd: ["/usr/bin/bun", "./bun-single.js"],
    cwd: __dirname,
    stdout: "inherit",
    stderr: "inherit",
    stdin: "inherit",
  });
}

function kill() {
  for (const bun of buns) {
    bun.kill();
  }
}

process.on("SIGINT", kill);
process.on("exit", kill);
