# Building the manuscript

[`build.sh`](build.sh) builds the repository.
`bash build/build.sh` should be executed from the root directory of the repository.
By default, `build.sh` creates HTML and PDF outputs.
However, setting the `BUILD_PDF` environment variable to `false` will suppress PDF output.
For example, run local builds using the command `BUILD_PDF=false bash build/build.sh`.

To build a DOCX file of the manuscript, set the `BUILD_DOCX` environment variable to `true`.
For example, use the command `BUILD_DOCX=true bash build/build.sh` locally.
To export DOCX for all CI builds, set an environment variable in the CI configuration file.
For GitHub Actions, set the variable in `.github\workflows\manubot.yaml` (see [docs](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/using-environment-variables)):

```yaml
name: Manubot
env:
  BUILD_DOCX: true
```

To generate a single DOCX output of the latest manuscript with GitHub Actions, click the "Actions" tab at the top of the repository.
Select the "Manubot" workflow, then the "Run workflow" button and check "generate DOCX output" before clicking the green "Run workflow" button.

Currently, equation numbers via `pandoc-eqnos` are not supported for DOCX output.

Format conversion is done using [Pandoc](https://pandoc.org/MANUAL.html).
`build.sh` calls `pandoc` commands using the options specified in [`pandoc/defaults`](pandoc/defaults).
Each file specifies a set of pandoc `--defaults` options for a given format.
To change the options, either edit the YAML files directly or add additional `--defaults` files.

## Environment

Note: currently, **Windows is not supported**.

The recommended local environment now uses a repository-local Python virtual environment in `.venv`.
From the repository root, run one of the following setup helpers:

```sh
# Linux / macOS
bash scripts/setup_local_env.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/setup_local_env.ps1
```

Or create the environment manually:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-local.txt
```

To refresh an existing local `.venv`, reactivate it and rerun:

```sh
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-local.txt
```

The CI workflow uses the same `pip` dependency set via `ci/requirements-ci.txt`, so local and CI installs are now aligned.
[`environment.yml`](environment.yml) is retained only as a historical reference from the original rootstock setup.

Because the build process is dependent on having the appropriate version of the `manubot` Python package,
it is necessary to use the pinned version from `requirements-local.txt` / `ci/requirements-ci.txt`.
The latest `manubot` release on PyPI may not be compatible with the latest version of this rootstock repository.

## Building PDFs

If Docker is available, `build.sh` uses the [Athena](https://www.athenapdf.com/) [Docker image](https://hub.docker.com/r/arachnysdocker/athenapdf) to build the PDF.
Otherwise, `build.sh` uses [WeasyPrint](https://weasyprint.org/) to build the PDF.
It is common for WeasyPrint to generate many warnings and errors that can be safely ignored.
Examples are shown below:

```text
WARNING: Ignored `pointer-events: none` at 3:16, unknown property.
WARNING: Ignored `font-display:auto` at 1:53114, descriptor not supported.
ERROR: Failed to load font at "https://use.fontawesome.com/releases/v5.7.2/webfonts/fa-brands-400.eot#iefix"
WARNING: Expected a media type, got only/**/screen
```
