# Public Release Checklist

Use this checklist before making a branch, tag, release, or repository state
public. The goal is to improve transparency without exposing private academic
assets or making unsupported claims.

## Identity and Project Claims

- `README.md` states the project scope accurately.
- No text claims broad adoption, many users, production deployment, institutional
  endorsement, or large community use unless there is public evidence.
- `content/metadata.yaml` uses a truthful author name and affiliation.
- Public contact fields are intentionally empty, neutral, or safe for public use.
- The repository description and topics match the actual workflow.

## Private Data Boundary

Confirm that the public tree does not include:

- personal email addresses or other private contact details;
- local paths such as private Windows user directories;
- thesis, proposal, defense, pre-defense, weekly-report, or planning drafts;
- private Word, PowerPoint, PDF, ZIP, or generated office artifacts;
- API keys, tokens, cookies, SSH keys, or CI secrets;
- logs that reveal private files or machine-specific paths.

Suggested search from a clean public clone. Replace `PRIVATE_EMAIL_DOMAIN` with
any personal email domain that must remain private before running the command:

```powershell
rg -n -i "PRIVATE_EMAIL_DOMAIN|C:\\Users\\|开题|答辩|预答辩|周报|毕业论文|proposal|defense|weekly-report|private draft|token|secret|api[_-]?key" .
```

Review matches manually. Some words may be false positives, such as `thesis`
inside `hypothesis`.

## Branch and Tag Hygiene

Check public branches:

```powershell
git ls-remote --heads https://github.com/SHzzzAyys/manubot-paper.git
```

Check public tags:

```powershell
git ls-remote --tags https://github.com/SHzzzAyys/manubot-paper.git
```

Before release, delete unsafe public branches or tags that expose private files.
Do not rely only on the GitHub web UI if sensitive content was briefly public.

## Reproducibility and Maintenance Evidence

- `CITATION.cff` exists and contains only accurate metadata.
- `LICENSE`, `LICENSE.md`, and `LICENSE-CC0.md` match the intended public use.
- `CHANGELOG.md` records real changes only.
- `ROADMAP.md` describes planned work without adoption claims.
- `CONTRIBUTING.md` explains how manuscript, evidence-table, citation, and
  workflow changes should be reviewed.
- `.github/pull_request_template.md` includes privacy and validation checks.
- The Manubot GitHub Actions workflow passes or has a documented failure.

## Release Steps

1. Open a pull request from the release-preparation branch into `main`.
2. Review the full diff, especially generated files and metadata.
3. Run the privacy-boundary search on a clean clone.
4. Wait for CI or document why CI could not be completed.
5. Merge with a clear message.
6. Create a release tag such as `v0.1.0` from `main`.
7. Do not attach private Word, PowerPoint, thesis, proposal, defense, or local
   generated files to the release.

## After Release

- Verify the repository is public only after the privacy checks pass.
- Verify the GitHub profile intended for the application is public.
- Confirm that the release page, README, repository topics, and citation metadata
  all describe the same public workflow.
