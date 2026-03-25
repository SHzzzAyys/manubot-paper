# Manubot Paper Workspace

This repository is a personalized Manubot starter workspace for drafting a scholarly manuscript with Git-based collaboration.
It keeps the official Manubot build pipeline while replacing the template content with a cleaner default structure for real writing.

## What To Edit

- `content/metadata.yaml`: manuscript title, authors, affiliations, keywords
- `content/01.abstract.md`: abstract
- `content/02.introduction.md`: introduction and background
- `content/03.methods.md`: methods
- `content/04.results.md`: results
- `content/05.discussion.md`: discussion and conclusion
- `content/images/`: figures and diagrams

## Local Workflow

On this machine, the Manubot environment is already installed.
Use the helper script at `C:\Users\zheng shang\use-manubot.ps1` to confirm the environment is available.

For local manuscript builds on Windows, run the build steps from Git Bash:

```bash
bash build/build.sh
manubot webpage
cd webpage
python -m http.server
```

## Collaboration Workflow

- Create a feature branch for each substantial change.
- Open a pull request for section edits, figure updates, or citation-heavy revisions.
- Let GitHub Actions validate the build before merging.
- Keep one sentence per line in manuscript files to make diffs easier to review.

See `CONTRIBUTING.md` for the repository conventions used in this workspace.
