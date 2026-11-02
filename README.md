# OpenSearch Migrations schema artifacts

Versioned `workflow-user-schema.json` files and a version manifest for the public
[OpenSearch Migrations project](https://github.com/opensearch-project/opensearch-migrations).
The upstream project maintains the implementation and releases.

## Artifact URLs

| Resource | URL |
| --- | --- |
| Manifest | `https://raw.githubusercontent.com/AndreKurait/opensearch-migrations-schemas/main/versions.json` |
| Schema | `https://raw.githubusercontent.com/AndreKurait/opensearch-migrations-schemas/main/{version}/workflow-user-schema.json` |

`versions.json` maps each stored version to its artifact path. `latest` selects
the default stored version; it is not a live query of upstream releases.
Existing version directories and URLs are retained for consumers.

## Validate locally

```sh
python3 scripts/validate_manifest.py
```

The offline check verifies that `latest` names a manifest entry, every artifact
path remains inside this repository, and each referenced file exists and parses
as JSON. CI runs the same check on pull requests and pushes.

This checks artifact structure and availability. It does not compare files with
upstream release assets, validate every JSON Schema keyword, or test a migration.

## Add a version

1. Obtain the schema for the exact intended upstream release and place it at
   `{version}/workflow-user-schema.json`.
2. Add its path to `versions.json`. Update `latest` only when changing the default
   stored version.
3. Run the validator and review the artifact and manifest diff together.

Do not rename or overwrite existing versioned artifacts as part of adding a new
release. Include the upstream release/asset reference in the pull request so
reviewers can check its origin.
