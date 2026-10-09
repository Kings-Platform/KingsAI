# Templates

<!-- Your approved texts. This page is the INDEX the skills read: each text, in each language, -->
<!-- points to where it lives. A file in this folder is the default; any other source works -->
<!-- (a doc, a note app block…) as long as the row says how to read it. One text, one source. -->

## Where each text lives

| Text | Language | Source | How to read it |
|---|---|---|---|
| `invite` | `en` | `invite.en.md` | file in this folder |
| `dm` | `en` | `dm.en.md` | file in this folder |
| `email` | `en` | `email.en.html` | file in this folder |
| `cover-letter` | `en` | `cover-letter.en.md` | file in this folder |
| `relocation` | `en` | `relocation.en.md` | file in this folder |

A text kept elsewhere: put the address in **Source** and the tool and any quirk in **How to
read it** — e.g. `block <id>` · `document connector, fetch by id; placeholders come escaped as
\{name\}`. The skills follow that column; they never keep a copy, and when the source can't be
read they stop and say so instead of writing the text themselves.

## What each text is for

| Text | Used by | Limits |
|---|---|---|
| `invite` | `linkedin-outreach` | LinkedIn: 300 characters with Premium, 200 without — the skill checks |
| `dm` | `linkedin-outreach` | Paragraphs separated by blank lines |
| `email` | `application-email` | Paragraphs; the CV goes as attachment. HTML or plain paragraphs — the skill turns paragraphs into `<p>` |
| `cover-letter` | `ats-apply` | Where a form has a cover-letter text field; otherwise the PDF in the profile index |
| `relocation` | all | The one sentence used when relocation is `conditional` |

## Placeholders

| Placeholder | Filled with |
|---|---|
| `{first_name}` | The recipient's first name, capitalized |
| `{company}` | The company, only where the template asks for it |
| `{role}` | The role title, usually only in the email subject |
| `{cv_link}` | The public CV link from the profile index, in the text's language |
| `{relocation}` | The `relocation` text, when the posting is in another country; otherwise the line is dropped |
| `{country}` | The posting's country, inside `relocation` |

The skills fill the placeholders and change nothing else.

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
