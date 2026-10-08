# Invitation with a note, without opening the profile

Tested on LinkedIn's web app (Portuguese and English interfaces). Button labels are matched by
regex so either interface works; adjust the patterns if yours differs.

## Why this path

- Opening a profile shows the visit; the preload modal doesn't.
- Many recruiters only show "Follow" on search cards; the preload URL always offers the invite.
- The "Connect" button next to a **post's author** sends immediately, with no note.

## Procedure

1. Navigate to `https://www.linkedin.com/preload/custom-invite/?vanityName=<slug>`
   (the slug is the `/in/<slug>` part; accents stay URL-encoded, e.g. `%C3%AD`).
2. The modal "Add a note to your invitation?" opens. Click **Add a note**.
3. Focus the dialog's `textarea` and insert the note with `document.execCommand('insertText')`
   — keyboard `type` drops characters on this page.
4. Click **Send**. Read the recipient's name from the dialog text before it closes, to log it.
5. If the modal never appears, the person is already connected, already invited, or the slug is
   wrong — report, don't retry.

## Script (one person per call; keep calls short)

```js
// NOTE: fill `note` with the profile template already rendered for this person.
const sl = ms => new Promise(r => setTimeout(r, ms));
let add;
for (let i = 0; i < 30 && !(add = [...document.querySelectorAll('button')]
  .find(b => /Add a note|Adicionar nota/.test(b.innerText))); i++) await sl(300);
if (!add) { 'NO DIALOG: ' + (document.querySelector('[role=dialog]')?.innerText.slice(0, 200) || 'none'); }
else {
  const dialog = document.querySelector('[role=dialog]').innerText;
  const name = (dialog.match(/invitation to ([^.\n]+)\.|convite a ([^.\n]+)\./) || []).slice(1).find(Boolean) || '';
  add.click();
  let ta; for (let i = 0; i < 20 && !(ta = document.querySelector('textarea')); i++) await sl(200);
  const note = `…`;                       // rendered template, {first_name} already replaced
  ta.focus(); document.execCommand('insertText', false, note);
  await sl(400);
  const send = [...document.querySelectorAll('button')]
    .find(b => /^Send$|^Enviar$/.test(b.innerText.trim()) || /Send invitation|Enviar convite/.test(b.getAttribute('aria-label') || ''));
  send.click(); await sl(1500);
  name + ' | ' + ta.value.length + ' | sent';
}
```

The first name for the template: first token of `name`, capitalized (`Ana Virgínia` → `Ana`).
Some names come back in capitals; normalize before rendering.

## Verifying a batch

`https://www.linkedin.com/mynetwork/invitation-manager/sent/` lists the most recent first, ten
or so per screen; scroll (real wheel scroll, then wait) until every name of the batch is in the
page text. Names missing after two scrolls were not sent.

## Limits

- Weekly cap, unpublished (~100 per rolling 7 days). Stop at the first "limit reached" message.
- Withdrawing a pending invitation blocks a new one to the same person for ~3 weeks.
