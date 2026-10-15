# Branching Guide

This document states what each branch in the repository is for, which roadmap phase it belongs to, and how branches are expected to be used.

Branch status below is a snapshot taken on 15 October 2026. Refresh it with the commands in [Checking branch status](#checking-branch-status) before relying on it.

## Branch overview

| Branch | Purpose | Roadmap phase | Status (snapshot) |
|---|---|---|---|
| `main` | Stable, default branch. Always passes CI. Every change reaches it through a pull request. | All | Active |
| `docs/project-documentation` | Documentation work: architecture, policy and verification, benchmark and evaluation docs. | Phase 1 and 2 (documentation items) | 3 commits ahead of `main`, 3 behind. Changes are documentation only. |
| `test/benchmark-expansion` | Larger benchmark dataset, metric denominators, verification precision and recall, failure-category reporting, ablation runs. | Phase 2: Benchmark Reliability | Placeholder. No commits of its own, 11 behind `main`. |
| `feat/agent-planner` | Planner interface that suggests tool calls without bypassing the execution engine or policy checks. | Phase 4: Planner Interface (builds on Phase 3: Multi-Step Execution) | 4 commits ahead, 4 behind. Changes are documentation only so far. |
| `feat/llm-integration` | Optional, interchangeable model-provider interface for LLM-based planning. The core must not depend on a paid model. | Phase 5: Optional LLM Integration | Placeholder. No commits of its own, 11 behind `main`. |
| `feat/api` | API contract, request validation, structured responses, authentication where needed, bounded execution. | Phase 6: API and Operations | Placeholder. No commits of its own, 11 behind `main`. |
| `feat/audit-logging` | Structured audit events for policy decisions, executions and verification results. | Phase 6: API and Operations | Placeholder. No commits of its own, 11 behind `main`. |
| `project-documentation` | Earlier documentation branch, superseded by `docs/project-documentation`. | None | Stale. Nothing ahead of `main`. Candidate for deletion. |

## What "placeholder" means

Several branches currently point at an older commit of `main` and contain no work of their own. They record intent. Before starting real work on one of them, bring it up to date with `main` so it includes the code, tests, CI and configuration added since:

```bash
git checkout feat/api
git merge main        # or: git rebase main
```

Do this before the first commit on the branch, not after, to avoid large conflicts later.

## Branch naming

Use `<type>/<short-description>` with lowercase words separated by hyphens.

| Prefix | Use for | Example |
|---|---|---|
| `feat/` | New capabilities | `feat/audit-logging` |
| `fix/` | Bug fixes | `fix/policy-text-limit` |
| `test/` | Tests and benchmark changes | `test/benchmark-expansion` |
| `docs/` | Documentation only | `docs/project-documentation` |
| `chore/` | Tooling, dependencies, maintenance | `chore/update-actions` |
| `ci/` | Workflow changes | `ci/add-codeql` |

Dependabot creates its own `dependabot/...` branches. Leave them to the bot.

## Workflow

1. Create the branch from an up-to-date `main`.
2. Keep changes focused on one topic, in line with the branch's purpose above.
3. Run `ruff check .`, `pytest` and `python benchmarks/run_benchmark.py` locally.
4. Open a pull request into `main`. The pull request template and CODEOWNERS apply.
5. Merge only when CI passes: tests, lint, package build and CodeQL.
6. Delete the branch after merging.

Long-lived feature branches such as `feat/agent-planner` should merge `main` into themselves regularly so they do not drift.

## Rules for specific areas

- **Policy and verification** (`policy.py`, `verification.py`, `engine.py`, `registry.py`): changes need tests for permitted and denied cases, and must not weaken default restrictions silently. See [`policy-and-verification.md`](policy-and-verification.md).
- **Benchmark** (`benchmarks/`): document any change to the dataset, metric definitions or tool behavior, so results remain comparable. See [`benchmark-and-evaluation.md`](benchmark-and-evaluation.md).
- **Planner and LLM branches**: a planner may suggest tool calls but must never invoke tools directly or skip policy enforcement. See Phase 4 in [`roadmap.md`](roadmap.md).

## Suggested cleanup

- Delete `project-documentation`, locally and on GitHub, since it is superseded and has no unmerged work.
- Merge or close `docs/project-documentation` once its documentation changes are reviewed.
- Keep the placeholder `feat/` and `test/` branches only if they will be used soon. A branch can always be recreated from `main` when work begins, which avoids the drift described above.

Delete a branch locally and on GitHub with:

```bash
git branch -d <branch>
git push origin --delete <branch>
```

## Checking branch status

List all branches with their latest commit:

```bash
git fetch --all --prune
git branch -a -vv
```

See how far a branch is from `main` (first number is commits only in `main`, second is commits only in the branch):

```bash
git rev-list --left-right --count origin/main...origin/<branch>
```

See what a branch changes compared with `main`:

```bash
git diff --stat origin/main...origin/<branch>
```
