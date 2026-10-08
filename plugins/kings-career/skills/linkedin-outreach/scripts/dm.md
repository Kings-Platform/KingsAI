# DM to a 1st-degree connection, without opening their profile

## Procedure

1. Navigate to `https://www.linkedin.com/messaging/`.
2. Click the **New message** button (label matched by regex: `/New message|Escrever mensagem/`
   on the text or `aria-label`; a `?profileUrn=` parameter on `/messaging/compose/` is ignored).
3. In the recipients `input` (placeholder contains "names" / "nomes"), insert the **full name**
   with `insertText`, wait ~2 s, and click the `[role=option]` whose text contains
   `"<Name> • 1st"` (or `1º`). No option → the person isn't a connection; stop.
4. Alternatively, from the person's profile page, the **Message** button opens the composer
   with the recipient set — use it only when step 3 can't find the name (the visit is shown).
5. In `.msg-form__contenteditable`, insert the template **paragraph by paragraph**:
   `insertText` for a line, `insertParagraph` between lines (an empty line = two
   `insertParagraph`). When the editor isn't found by JS right after opening, click inside the
   message box once and use real keyboard `type` with `shift+Return` for line breaks.
6. Confirm the recipient pill, then click `button.msg-form__send-button`. The URL becomes
   `/messaging/thread/2-…`; the sent text appears at the end of `.msg-s-message-list`.

## Reading before writing

- The **thread list** preview (name, time, last line) is enough to know who replied — no need
  to open the thread.
- Opening a thread marks it read. Open only the thread you're replying in, after the user saw
  the preview.

## Script (editor already open with the recipient set)

```js
const sl = ms => new Promise(r => setTimeout(r, ms));
const ed = document.querySelector('.msg-form__contenteditable');
const lines = [ /* rendered template, one entry per line, '' for a blank line */ ];
ed.focus();
lines.forEach((l, i) => { if (l) document.execCommand('insertText', false, l);
  if (i < lines.length - 1) document.execCommand('insertParagraph'); });
await sl(500);
document.querySelector('button.msg-form__send-button').click();
await sl(2500);
document.querySelector('.msg-s-message-list').innerText.slice(-300);
```

Keep each JS call short: a long loop over many people exceeds the tool timeout and, in a
background tab, timers are throttled — batch a few at a time.
