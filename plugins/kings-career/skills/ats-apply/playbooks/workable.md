# Workable

`apply.workable.com/<company>/j/<id>/apply`. React.

- Text fields: `form_input` by ref. The phone formats itself.
- **Yes/No:** styled "YES"/"NO" buttons. Clicking the radio by ref doesn't tick it; click the
  button by coordinate (recompute after scrolling).
- Personal free-text questions ("your favorite…") have no basis in the profile → pending for
  the user, with the tab left open.
- **Submit:** Cloudflare "Verify you are human" may follow. Not the agent's: leave the tab;
  when it passes, the URL gets `?success` and "Thank you!".
