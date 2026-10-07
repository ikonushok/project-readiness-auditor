# Export CLI specification

Version: 1.0; date: 2026-10-01; status: Approved; target: CLI release 1.

- FR-001: Collapse repeated whitespace inside each non-empty name and trim its edges. Given `  Ada   Lovelace `, normalization returns `Ada Lovelace`.
- FR-002: Ignore blank names, preserving the relative order and duplicates of remaining names.
- FR-003: Support `--format json` to emit a JSON array of normalized names.
- FR-004: Exports must have stable ordering.
- SC-001: Normalize 100,000 names within 100 ms on the deployment laptop.
