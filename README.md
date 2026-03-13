# opensearch-migrations-schemas

Versioned JSON schemas from [opensearch-migrations](https://github.com/opensearch-project/opensearch-migrations) releases, served as direct-download raw files (no redirects).

## URLs

| Resource | URL Pattern |
|----------|-------------|
| Version manifest | `https://raw.githubusercontent.com/AndreKurait/opensearch-migrations-schemas/main/versions.json` |
| Schema by version | `https://raw.githubusercontent.com/AndreKurait/opensearch-migrations-schemas/main/{version}/workflow-user-schema.json` |

## Adding a new version

```bash
VERSION=2.9.0
mkdir -p ${VERSION}
curl -sL "https://github.com/opensearch-project/opensearch-migrations/releases/download/${VERSION}/workflow-user-schema.json" -o ${VERSION}/workflow-user-schema.json
# Update versions.json, commit, push
```
