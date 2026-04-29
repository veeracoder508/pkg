# CHANGELOG.md
**version**: 0.0.1

**type**: stable

**total changes**: 2

---

1. Use `tomllib` (with fallback to `tomli`) to parse `pyproject.toml` from uploaded package archives and populate `PkgMetaData` fields: `author`, `user_name`, and `license`. **(tag: feature)**

2. Prevent storing duplicate package versions: endpoint now checks for an existing `PkgMetaData` with the same `pkg_id` and `version`; on conflict it removes the uploaded file (best-effort) and returns HTTP 409. **(tag: feature)**

3. Added: `tools/generate_pdoc.py` — wrapper script that sets `PYTHONPATH` to the repository `src` directory and runs `pdoc` to generate HTML for the `pkg` package. Path: `tools/generate_pdoc.py`.

4. Added: `scripts/generate_docs.ps1` — Windows PowerShell helper that runs the Python wrapper (uses `.venv` python if present). Path: `scripts/generate_docs.ps1`.

5. Added: `docs/GENERATE_DOCS.md` — short instructions for running the wrapper and PowerShell helper. Path: `docs/GENERATE_DOCS.md`.

6. Updated: Todo list via agent to track tasks performed. (Internal `manage_todo_list` updates.)