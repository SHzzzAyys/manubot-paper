# Security and Private Data Reports

This repository is primarily a research-writing workflow, not a deployed service.
The main safety risks are accidental disclosure of private academic material,
contact information, credentials, local paths, or CI logs.

## In Scope

- Private contact information, including personal email addresses, added to the
  public repository by mistake.
- Private thesis, proposal, defense, weekly-report, or unpublished planning
  drafts.
- API keys, tokens, SSH keys, cookies, or other credentials.
- Local machine paths or generated logs that reveal private workspace structure.
- Build or release artifacts that include non-public files.

## Out of Scope

- Scientific disagreements that can be handled through normal issues or pull
  requests.
- Requests for clinical, veterinary, or diagnostic advice.
- Problems caused by forks or mirrors outside this repository.

## How to Report

Do not paste secrets, private drafts, personal email addresses, or private local
paths into a public issue.

Preferred reporting path:

1. Use GitHub's private vulnerability reporting or security advisory mechanism
   if it is enabled for this repository.
2. If only public issues are available, open a minimal issue that describes the
   category of problem without copying the sensitive content.
3. Include the affected file path, branch, commit, or release tag when it can be
   shared safely.

The maintainer will make a best-effort response. For confirmed private-data
exposure, the expected remediation is to remove the content from public branches,
delete unsafe tags or releases when needed, and document the public boundary so
the same issue is less likely to recur.
