# Repository rulesets

Rulesets are configured on GitHub, not in this repo. The JSON here is a checked-in copy of
what is (or should be) applied, so the configuration is reviewable and re-importable.

## `main.json`

Requires the `Validate DTDL` status check — produced by
[`.github/workflows/validate_dtdl.yml`](../workflows/validate_dtdl.yml) — to pass before a pull
request can be merged into the default branch.

## `bypass_actors.json`

Grants the GitHub Actions app (`Integration`, id `15368`) a bypass on that ruleset. This is
required, not incidental: [`merge_dtdl.yml`](../workflows/merge_dtdl.yml) opens and immediately
merges its own `auto/<version>` version-bump PR using `GITHUB_TOKEN`. GitHub does not trigger
workflow runs for events raised by `GITHUB_TOKEN`, so `Validate DTDL` never runs on those PRs and
would otherwise block the merge forever. The bypass lets that one automated flow through; PRs
opened by people are still gated.

It is a separate file because the UI's ruleset importer rejects it with *"contains an invalid
actor"* — the importer only accepts bypass actors it can resolve from the repo's installed apps,
and GitHub Actions is not installed as an integration. The REST API accepts it.

## Applying it

**1. Create the ruleset.** Import `main.json` through the UI — **Settings → Rules → Rulesets →
New ruleset → Import a ruleset** — or `POST` it:

```powershell
gh api -X POST repos/WillowInc/opendigitaltwins-building/rulesets --input .github/rulesets/main.json
```

**2. Add the bypass, before the next `merge_dtdl` run.** Between step 1 and step 2 the ruleset is
enforced on everything, including the bot. Get the ruleset id, then `PATCH` the bypass onto it:

```powershell
gh api repos/WillowInc/opendigitaltwins-building/rulesets --jq '.[] | "\(.id) \(.name)"'
gh api -X PATCH repos/WillowInc/opendigitaltwins-building/rulesets/<id> --input .github/rulesets/bypass_actors.json
```

Without `gh`, the same call with a PAT that has `administration:write`:

```powershell
$headers = @{ Authorization = "Bearer $env:GITHUB_PAT"; Accept = "application/vnd.github+json"; "User-Agent" = "willow" }
Invoke-RestMethod -Method Patch -Uri "https://api.github.com/repos/WillowInc/opendigitaltwins-building/rulesets/<id>" `
  -Headers $headers -Body (Get-Content .github/rulesets/bypass_actors.json -Raw)
```

**3. Verify the bypass took.** If it is missing, the version-bump PRs will hang:

```powershell
gh api repos/WillowInc/opendigitaltwins-building/rulesets/<id> --jq '.bypass_actors'
```

## If the API also rejects the actor

Some orgs cannot attach the GitHub Actions integration as a bypass actor at all. Do not substitute
a `RepositoryRole` bypass — the bot merges with write permission, so a write-role bypass would
exempt every human contributor too and defeat the gate.

Use this instead: have `merge_dtdl.yml` report the check itself. It has already run the merger
successfully by that point, and the version bump touches only `Metadata/*.nuspec`, so the ontology
it validated is the ontology being merged. After the `git push` and before `gh pr merge`, add:

```yaml
    - name: 'Report Validate DTDL status'
      run: |
        gh api -X POST repos/${{ github.repository }}/statuses/$(git rev-parse HEAD) \
          -f state=success \
          -f context='Validate DTDL' \
          -f description='Validated by Merge DTDL'
```

The status is attributed to `github-actions[bot]`, which satisfies the `integration_id: 15368`
pinned in `main.json`. This needs `statuses: write` on the job's `GITHUB_TOKEN`.

## Classic branch protection

Rulesets and classic branch protection are enforced together, and the most restrictive wins —
a ruleset bypass does *not* exempt anyone from a classic rule. If **Settings → Branches** still has
a protection rule on `main`, remove or reconcile it, or the version-bump PRs will be blocked
regardless of what is configured here.
