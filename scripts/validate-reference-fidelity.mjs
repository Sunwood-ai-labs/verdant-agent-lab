#!/usr/bin/env node
import fs from 'node:fs';

const ledger = JSON.parse(fs.readFileSync('assets/layouts/reference-instance-ledger.v1.json', 'utf8'));
const unresolved = ledger.instances.filter((instance) => instance.status !== 'verified');

for (const instance of unresolved) {
  console.error(`OPEN ${instance.id}: ${instance.status} — ${instance.reason}`);
}

if (ledger.status !== 'complete' || unresolved.length) {
  console.error(`REFERENCE FIDELITY INCOMPLETE: ${unresolved.length} unresolved instance records`);
  process.exit(1);
}

console.log(`REFERENCE FIDELITY PASS: ${ledger.instances.length} verified instances`);
