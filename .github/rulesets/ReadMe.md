# Repository rulesets

Rulesets are configured on GitHub, not in this repo. The JSON here is a checked-in copy of
what is (or should be) applied, so the configuration is reviewable and re-importable.

## `main.json`

Requires the `Validate DTDL` status check — produced by
[`.github/workflows/validate_dtdl.yml`](../workflows/validate_dtdl.yml) — to pass before a pull
request can be merged into the default branch.

### The bypass actor

`bypass_actors` contains the GitHub Actions app (`Integration`, id `15368`). This is required, not
incidental: [`merge_dtdl.yml`](../workflows/merge_dtdl.yml) opens and immediately merges its own
`auto/<version>` version-bump PR using `GITHUB_TOKEN`. GitHub does not trigger workflow runs for
events raised by `GITHUB_TOKEN`, so `Validate DTDL` never runs on those PRs and would otherwise
block the merge forever. The bypass lets that one automated flow through; PRs opened by people are
still gated.

## Applying it

Either import through the UI — **Settings → Rules → Rulesets → New ruleset → Import a ruleset** —
and upload `main.json`, or apply it with the API:

```sh
gh api -X POST repos/WillowInc/opendigitaltwins-building/rulesets --input .github/rulesets/main.json
```

To update an existing ruleset in place, get its id from `gh api repos/WillowInc/opendigitaltwins-building/rulesets`
and `PUT` to `.../rulesets/<id>` with the same `--input`.

After applying, confirm the bypass survived — the UI's bypass picker does not always offer GitHub
Actions, and an import that drops it will leave the version-bump PRs stuck:

```sh
gh api repos/WillowInc/opendigitaltwins-building/rulesets/<id> --jq '.bypass_actors'
```

## Classic branch protection

Rulesets and classic branch protection are enforced together, and the most restrictive wins —
a ruleset bypass does *not* exempt anyone from a classic rule. If **Settings → Branches** still has
a protection rule on `main`, remove or reconcile it, or the version-bump PRs will be blocked
regardless of what is configured here.
