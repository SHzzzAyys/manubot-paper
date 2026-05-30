# Roadmap

This roadmap describes the next maintenance priorities for the public research-writing workflow. It is intentionally conservative: it lists planned work and maintenance direction, not adoption claims.

## Near-Term Priorities

- Literature management
  - Normalize how new studies are added to `data/` evidence tables.
  - Add clearer checks for duplicate studies, missing DOI/PMID metadata, and incomplete intervention/outcome fields.
  - Document the expected review process before a literature update is merged.

- Figure and table checks
  - Add validation for figure/table references in manuscript text.
  - Check that table rows have complete source, intervention, host, and outcome fields.
  - Produce review-friendly diagnostics for missing captions, inconsistent abbreviations, and unresolved placeholders.

- Continuous integration
  - Keep CI focused on reproducibility: dependency setup, manuscript build, validation scripts, and artifact generation.
  - Add clearer failure summaries for citation, build, and evidence-table validation errors.
  - Review workflow permissions so automation uses the least privileges required.

- Manuscript version control
  - Define a lightweight release convention for manuscript snapshots.
  - Separate source manuscripts, generated artifacts, and local-only outputs more clearly.
  - Improve changelog notes for evidence-table and manuscript-structure changes.

- Citation consistency
  - Add checks for unmatched citations, duplicate references, missing identifiers, and inconsistent citation metadata.
  - Keep citation diagnostics visible in CI logs and local validation output.
  - Document how unresolved or unverifiable citation metadata should be marked.

## Longer-Term Direction

- Build a more complete public workflow guide for veterinary parasitology review projects.
- Add reusable templates for evidence extraction, study classification, and manuscript audit checklists.
- Improve generated HTML output so readers can inspect links between claims, evidence rows, and references.
- Keep private academic planning material outside the public repository boundary.

## Non-Goals

- This repository does not claim broad adoption or a large user community.
- This repository is not a clinical decision-support tool.
- This repository does not replace expert review of parasitology evidence, animal-study quality, or manuscript claims.
