# Pipeline

<!-- One row per application or contact. The pipeline-keeper agent is the only writer. -->
<!-- Newest first. The plugin reads this before acting on any posting ("did I already apply?"). -->

## Applications

| Date | Company | Role | Channel | Contact | External id | Status | Next step |
|---|---|---|---|---|---|---|---|

Status values: `sent` · `pending-user: <what>` · `confirmed` · `in-process` · `rejected` ·
`discarded: <why>` · `closed`.

Channel values: `greenhouse` · `lever` · `ashby` · `workday` · `email` · `dm` ·
`easy-apply` · `site` · `<other ATS>`.

## Outreach

Invitations and DMs. The `linkedin-outreach` skill counts the last 7 days here against the
weekly budget in the profile index.

| Date | Person | Company | Kind | Language | Status |
|---|---|---|---|---|---|

Kind values: `invite` · `dm` · `reply`. Status: `sent` · `queued: quota` · `accepted` ·
`replied`.

## Queue

What couldn't be done yet and why (quota, permission, account to create, test to take).

| Opened | Item | Blocked by | Owner |
|---|---|---|---|
