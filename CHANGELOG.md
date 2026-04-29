# CHANGELOG.md
**version**: 0.0.1

**type**: stable

**total changes**: 2

---

1. Use `tomllib` (with fallback to `tomli`) to parse `pyproject.toml` from uploaded package archives and populate `PkgMetaData` fields: `author`, `user_name`, and `license`. **(tag: feature)

2. Prevent storing duplicate package versions: endpoint now checks for an existing `PkgMetaData` with the same `pkg_id` and `version`; on conflict it removes the uploaded file (best-effort) and returns HTTP 409. **(tag: feature)**
