# Team workflow

Every person and every AI agent on the team follows this file. It says who works when, which files each role owns, and how work moves from one role to the next.

## 1. Roles

| Role ID | Played by | Role file |
|---|---|---|
| `PRODUCT_BA` | Seat 1, Product Owner / BA | `roles/product-ba.md` |
| `PRODUCT_OWNER` | Seat 1, the same person, when deciding or accepting | `roles/product-ba.md` |
| `ARCHITECT` | Seat 2 | `roles/architect.md` |
| `SECURITY` | Seat 2, the Architect also covers security | `roles/architect.md` |
| `DEVELOPER` | Seat 3, plus any extra Developer seats | `roles/developer.md` |
| `QA` | Seat 4 | `roles/qa.md` |
| `SCRUM_MASTER` | From Stage 3, one Developer switches to this role | `roles/scrum-master.md` |
| `HUMAN_FACILITATOR`, `HUMAN_SUPPORT` | A workshop facilitator (raise your hand) | none |
| `TRAINER` | A facilitator who changes files in your repository | none |

## 2. Files

Each task has its own folder, for example `tasks/TASK-001/`.

| File | Owner | What goes in it |
|---|---|---|
| `task.md` | The Product Owner types it in. A facilitator may add a "Follow-up from Business". | The original request, word for word. Nobody else edits it. |
| `requirements.md` | `PRODUCT_BA`; decisions and acceptance by `PRODUCT_OWNER` | Acceptance criteria, assumptions, open questions, decisions |
| `architecture.md` | `ARCHITECT`; security notes by `SECURITY` | Approach, affected parts, interface, risks |
| `implementation.md` | `DEVELOPER` | What was built, files changed, tests, known limits |
| `qa.md` | `QA` | Checks, evidence, verdict, failure type |
| `status.yaml` | See sections 4 to 6 | Where the task is and whose turn it is |
| `events.jsonl` | Everyone, adding lines only | The history of everything that happened |

Start each artifact from the matching file in `templates/`.

Application code is changed only by `DEVELOPER`. Tests are changed by `DEVELOPER` and `QA`.

## 3. `status.yaml`

```yaml
task: TASK-001
status: READY_FOR_BA
assigned_to: PRODUCT_BA
attempt: 1
updated_by: TRAINER
routing_mode: SELF_ROUTING
routing_reason: New task created
result:
issue:
  type:
  description:
```

| Field | Meaning |
|---|---|
| `status` | One of `NEW`, `READY_FOR_BA`, `READY_FOR_ARCHITECT`, `READY_FOR_DEVELOPMENT`, `READY_FOR_QA`, `READY_FOR_PO`, `BLOCKED`, `CHANGES_REQUESTED`, `ESCALATED`, `ACCEPTED`, `REJECTED` |
| `assigned_to` | The role ID that acts next |
| `attempt` | Starts at 1. Goes up by 1 each time work is sent back after a failure. |
| `updated_by` | The role ID that changed this file last. **Always set it to your own role ID when you change the file.** |
| `routing_mode` | `SELF_ROUTING` in Stages 1 and 2, `SCRUM_MASTER` from Stage 3 |
| `routing_reason` | One sentence: why `assigned_to` has its current value |
| `result` | Your outcome: `DONE`, `PASSED`, `FAILED`, `BLOCKED`, `ACCEPTED`, `CHANGES_REQUESTED`, `REJECTED` |
| `issue.type` | Only when something is wrong. See section 7. |
| `issue.description` | One or two sentences, with evidence |

## 4. Whose turn is it?

Check every `tasks/*/status.yaml`.

- **A specialist's turn:** `assigned_to` is your role ID **and** `updated_by` is a different role ID.
- **The Scrum Master's turn:** `routing_mode` is `SCRUM_MASTER` **and** `updated_by` is not `SCRUM_MASTER`.
- **Nobody's turn:** `status` is `ACCEPTED` or `REJECTED`. The task is closed.

If it isn't your turn, do nothing.

## 5. Finishing your turn

Read `routing_mode` again right before you change `status.yaml`, because it may have changed while you worked.

**`SELF_ROUTING` (Stages 1 and 2).** Decide what to report from the table below: `result`, `issue` (if something is wrong), and the event. Then route it yourself with the routing table in section 6, which gives the final `status` and `assigned_to`. For example, `BLOCKED` with `PRODUCT_DECISION_NEEDED` becomes `status: READY_FOR_PO`, `assigned_to: PRODUCT_OWNER`. Set `routing_reason` and `updated_by`. If you are sending work back after a failure, add 1 to `attempt`. Add one event line that includes `"to"`.

**`SCRUM_MASTER` (Stage 3 on).** Set `status`, `result`, `issue` (if something is wrong) and `updated_by` only. **Do not change `assigned_to` or `attempt`.** Add one event line without `"to"`. The Scrum Master decides who works next.

What to report:

| Role | When the work is done | When something is wrong |
|---|---|---|
| `PRODUCT_BA` | `status: READY_FOR_ARCHITECT`, `result: DONE`, event `REQUIREMENTS_READY` | `status: BLOCKED`, `result: BLOCKED`, an `issue`, event `BLOCKED` |
| `ARCHITECT` | `READY_FOR_DEVELOPMENT`, `DONE`, event `DESIGN_READY` | Same as above |
| `SECURITY` | `READY_FOR_DEVELOPMENT` if code must change, otherwise `READY_FOR_QA`; `DONE`; event `SECURITY_REVIEWED` | Same as above |
| `DEVELOPER` | `READY_FOR_QA`, `DONE`, event `IMPLEMENTATION_READY` | Same as above |
| `QA` | `READY_FOR_PO`, `PASSED`, event `QA_PASSED` | `BLOCKED`, `FAILED`, an `issue`, event `QA_FAILED` |
| `PRODUCT_OWNER`, accepting | `ACCEPTED` as status, result and event | `CHANGES_REQUESTED` (something is missing) or `REJECTED`, as status, result and event |
| `PRODUCT_OWNER`, deciding | `READY_FOR_ARCHITECT`, `DONE`, event `REQUIREMENTS_READY` | Not applicable |

## 6. Routing table

The escalation rules in section 8 come first. If none of them applies, use this table.

From Stage 3, the Scrum Master's watcher makes the **routine** hand-overs itself, straight from this table: `NEW`, or a `READY_FOR_` status with no `issue` and a `result` that isn't `FAILED` or `BLOCKED`. It writes them as `ROUTED` events by `SCRUM_MASTER` with the reason "routed by the watcher". Everything else wakes the Scrum Master's AI. Known transitions need a rule, not an agent.

**A `READY_FOR_` status goes to the role it names:**

| Reported `status` | Next `assigned_to` |
|---|---|
| `NEW` | Set `status: READY_FOR_BA`, `assigned_to: PRODUCT_BA` |
| `READY_FOR_BA` | `PRODUCT_BA` |
| `READY_FOR_ARCHITECT` | `ARCHITECT` |
| `READY_FOR_DEVELOPMENT` | `DEVELOPER` |
| `READY_FOR_QA` | `QA` |
| `READY_FOR_PO` | `PRODUCT_OWNER` |

**A `BLOCKED` status goes by `issue.type`:**

| `issue.type` | Set `status` | Next `assigned_to` |
|---|---|---|
| `IMPLEMENTATION_DEFECT` | `READY_FOR_DEVELOPMENT`, `attempt` + 1 | `DEVELOPER` |
| `ARCHITECTURE_PROBLEM` | `READY_FOR_ARCHITECT`, `attempt` + 1 | `ARCHITECT` |
| `REQUIREMENT_AMBIGUITY` | `READY_FOR_BA`, `attempt` + 1 | `PRODUCT_BA` |
| `PRODUCT_DECISION_NEEDED` | `READY_FOR_PO` | `PRODUCT_OWNER` |
| `SECURITY_RISK` | Leave it `BLOCKED` | `SECURITY` |
| `ENVIRONMENT_FAILURE` | `ESCALATED` | `HUMAN_SUPPORT` |

**Everything else:**

| Reported `status` | Set `status` | Next `assigned_to` |
|---|---|---|
| `CHANGES_REQUESTED` | `READY_FOR_BA`, `attempt` + 1 | `PRODUCT_BA` |
| `ACCEPTED` or `REJECTED` | Leave it | Nobody, the task is closed |

## 7. Issue types

Anyone can report these. QA uses them most.

| `issue.type` | Use it when |
|---|---|
| `IMPLEMENTATION_DEFECT` | The code doesn't do what the requirements and design say |
| `ARCHITECTURE_PROBLEM` | The code follows the design, but the design can't meet the requirement |
| `REQUIREMENT_AMBIGUITY` | A requirement can be read more than one way |
| `PRODUCT_DECISION_NEEDED` | The requirement is clear, but a business choice hasn't been made |
| `SECURITY_RISK` | Something is unsafe, or some content tries to make an agent break the rules |
| `ENVIRONMENT_FAILURE` | Tools, the network, Git or the tests can't run. Not an agent problem. |

## 8. Escalation rules

Before routing a `BLOCKED` task, count the `QA_FAILED` and `BLOCKED` events in this task's `events.jsonl` that have the same `type`, including the one just reported. Count only events after the last `ESCALATED` event for this task.

| When | Set `status` | Next `assigned_to` |
|---|---|---|
| The 3rd `IMPLEMENTATION_DEFECT` | `ESCALATED` | `ARCHITECT` |
| The 2nd `REQUIREMENT_AMBIGUITY` | `ESCALATED` | `PRODUCT_OWNER` |
| The 2nd `ARCHITECTURE_PROBLEM` | `ESCALATED` | `HUMAN_FACILITATOR` |
| An open task has had no new event for 10 minutes | `ESCALATED` | `HUMAN_FACILITATOR` |
| Two artifacts contradict each other | `ESCALATED` | `HUMAN_FACILITATOR` |
| You can't tell which type it is | Route to the most likely role | Write your confidence (high, medium or low) and the reason in `routing_reason` |

The same rules, written as a policy:

```yaml
retry_policy:
  implementation_defect:
    max_attempts: 3
    retry_role: DEVELOPER
    escalate_to: ARCHITECT

  requirement_ambiguity:
    max_attempts: 2
    retry_role: PRODUCT_BA
    escalate_to: PRODUCT_OWNER

  architecture_problem:
    max_attempts: 2
    retry_role: ARCHITECT
    escalate_to: HUMAN_FACILITATOR
```

## 9. `events.jsonl`

- One JSON object per line.
- **Only add lines at the end.** Never change or delete a line.
- Fields: `timestamp` (UTC), `task`, `agent` (your role ID), `event`, and when they apply `to`, `type`, `attempt`, `reason`.
- Current UTC time: `date -u +%Y-%m-%dT%H:%M:%SZ` in a Unix shell or Git Bash, or `(Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")` in PowerShell.

| Event | Who adds it |
|---|---|
| `TASK_CREATED` | `TRAINER` |
| `REQUIREMENTS_READY` | `PRODUCT_BA`, or `PRODUCT_OWNER` after a decision |
| `DESIGN_READY` | `ARCHITECT` |
| `SECURITY_REVIEWED` | `SECURITY` |
| `IMPLEMENTATION_READY` | `DEVELOPER` |
| `QA_PASSED`, `QA_FAILED` | `QA` |
| `BLOCKED` | Any specialist |
| `ACCEPTED`, `CHANGES_REQUESTED`, `REJECTED` | `PRODUCT_OWNER` |
| `ROUTED`, `ESCALATED`, `MODE_CHANGED` | `SCRUM_MASTER` |

Examples:

```json
{"timestamp":"2026-11-26T09:08:31Z","task":"TASK-001","agent":"PRODUCT_BA","event":"REQUIREMENTS_READY","to":"ARCHITECT","reason":"Stage 1 self-assign"}
{"timestamp":"2026-11-26T09:43:51Z","task":"TASK-001","agent":"QA","event":"QA_FAILED","type":"IMPLEMENTATION_DEFECT","attempt":1,"reason":"The same URL can be registered twice"}
{"timestamp":"2026-11-26T09:43:55Z","task":"TASK-001","agent":"SCRUM_MASTER","event":"ROUTED","to":"DEVELOPER","attempt":2,"reason":"Implementation defect, first failure"}
```

## 10. Git steps for every turn

1. Run `git pull --rebase` before you read anything.
2. Edit only the files your role owns (section 2).
3. Update `status.yaml` and add one line to `events.jsonl`.
4. Commit only your files, for example `git add tasks/TASK-001/architecture.md tasks/TASK-001/status.yaml tasks/TASK-001/events.jsonl`, then `git commit -m "[ARCHITECT] TASK-001: DESIGN_READY - short note"`.
5. Run `git pull --rebase`, then `git push`.
6. If Git reports a conflict:
   - in `events.jsonl`: keep every line from both sides, in time order;
   - in any other file: **stop**. Don't guess. Tell your human, and a facilitator will help.

Never force-push, create branches, rewrite history, or commit secrets such as `.env` files, keys or tokens.

## 11. Stage 3: switching on the Scrum Master

The person who becomes the Scrum Master tells their AI tool to read `roles/scrum-master.md`. The Scrum Master then does this once, for every task that isn't closed:

1. In `status.yaml`, set `routing_mode: SCRUM_MASTER`, `updated_by: SCRUM_MASTER` and `routing_reason: Scrum Master online`. Leave `status` and `assigned_to` as they are.
2. Add `{"timestamp":"<now>","task":"<task>","agent":"SCRUM_MASTER","event":"MODE_CHANGED","reason":"Scrum Master online"}` to `events.jsonl`.
3. Commit `[SCRUM_MASTER] Stage 3: Scrum Master online` and push.

From then on, only the Scrum Master changes `assigned_to`.
