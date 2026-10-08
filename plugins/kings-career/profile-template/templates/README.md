# Templates

<!-- Your approved texts. One file per text and language: invite.en.md, invite.pt.md, dm.en.md, -->
<!-- email.en.html, cover-letter.en.md … The skills fill the placeholders and change nothing else. -->

| File | Used by | Limits |
|---|---|---|
| `invite.<lang>.md` | `linkedin-outreach` | LinkedIn: 300 characters with Premium, 200 without — the skill checks |
| `dm.<lang>.md` | `linkedin-outreach` | Paragraphs separated by blank lines |
| `email.<lang>.html` | `application-email` | Plain HTML paragraphs; the CV goes as attachment |
| `cover-letter.<lang>.md` | `ats-apply` | Where a form has a cover-letter field; otherwise the PDF in the profile index |
| `relocation.<lang>.md` | all | The one sentence used when relocation is `conditional` |

## Placeholders

| Placeholder | Filled with |
|---|---|
| `{first_name}` | The recipient's first name, capitalized |
| `{company}` | The company, only where the template asks for it |
| `{role}` | The role title, usually only in the email subject |
| `{cv_link}` | The public CV link from the profile index |
| `{relocation}` | The relocation sentence, when the posting is in another country |

## Example: `invite.en.md`

```
Hi {first_name}!
I'm an iOS dev with 7+ years of experience (5+ in Swift), focused on performance and
architecture in large-scale apps. Fluent in English, experienced as a tech lead and mentor.
I'm exploring new iOS opportunities.
Thanks! :)
```

## Example: `email.en.html`

```html
<p>Hi {first_name},</p>
<p>I hope you're doing well.</p>
<p>My name is …, and I'm an iOS developer with … </p>
<p>I also have experience as … </p>
<p>{relocation}</p>
<p>If this opening isn't the right fit, and you know someone or another opportunity where my
profile could make sense, I'd really appreciate the referral.</p>
<p>Please find my resume attached.</p>
<p>Best regards,<br>…<br>+00 00 00000-0000<br><a href="https://www.linkedin.com/in/…">LinkedIn</a></p>
```
