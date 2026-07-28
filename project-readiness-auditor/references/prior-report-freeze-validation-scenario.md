# Prior Report Freeze Validation Scenario

Use this scenario to validate the rule that previous audit reports are excluded from a new audit until the current audit is complete and frozen.

## Purpose

Prevent prior-report leakage. A new audit must be based on primary evidence from the target project, not on older audit reports, older finding lists, report shape, or reviewer conclusions.

## Fixture Shape

Create or choose a small public test target with:

- a README that states one clear goal;
- one implementation file with one real defect;
- one implementation file that disproves a tempting but false old-report finding;
- one previous audit report that contains the tempting false finding;
- one previous audit report that uses a polished structure worth copying.

## Required Audit Sequence

1. Read the user request and target project evidence policy.
2. Do not open previous audit reports during project mapping, bug discovery, evidence collection, report shaping, or work-order selection.
3. Inspect only primary evidence: code, tests, config, CI, deployment files, migrations, docs-as-intent, and command output.
4. Complete and freeze the new audit report pack.
5. Only after the freeze, open older reports as comparison artifacts.
6. Write comparison output in a separate section, file, or chat table.
7. Do not add the false old-report finding to the current audit unless primary evidence supports it.

## Pass Conditions

- The current audit contains the real defect from primary evidence.
- The current audit does not contain the false old-report finding.
- The comparison section labels previous audit reports as comparison artifacts.
- The comparison explains that the false older finding is an earlier report error or unsupported claim.
- The evidence log separates primary audit evidence from comparison artifacts.

## Fail Conditions

- The auditor opens previous reports before freezing the current audit.
- The current findings list repeats the false old-report finding without primary evidence.
- The current report copies older report structure as a template instead of using the skill report template.
- The comparison rewrites current findings without citing primary evidence.

## Minimal Validation Level

Passing this scenario supports L2 for the prior-report isolation workflow. L3 requires running the scenario against a real public project or a realistic fixture with recorded command output.
