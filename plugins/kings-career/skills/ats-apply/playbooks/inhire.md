# InHire

`<company>.inhire.app/vagas/<uuid>/<slug>`. Short form on the posting page, then a screening
questionnaire.

## Form

- Ids: `name`, `email`, `phone` (with a `phoneCountry` selector), `linkedinUsername`,
  `resume` (file), `salaryExpectation` (text, formats as currency as you type), plus
  country/city and a referral radio on some boards. Brazilian boards add a **CPF** field: the
  user's, always (`pending`).
- Real click by ref + keyboard `type` works. The salary field formats digits as currency: type
  the plain number and read the result (`20000` → `R$ 20.000,00`).
- **Phone country** defaults to +1: open the selector, type the country, scroll and click the
  exact entry (`find "<Country> +<code>"`); then type the number again — changing the country
  clears it.
- CV: `file_upload` on the file input.
- "Continue registration" opens the questionnaire; a `g-recaptcha-response` textarea exists
  but hasn't blocked.

## Questionnaire

One question per screen, Typeform-style. Single-choice: clicking the option **advances by
itself**. Multi-choice: click each option, then "OK" — if OK doesn't advance, use the down
arrow in the bottom-right pager. The last screen has "Enviar"/"Submit".

Questions are generic (self-rated level, best practices, which AI tools, communication style):
answer from the bank and from the facts page; a multi-platform question ("iOS and Android")
answered "autonomous" is honest only for the platform the candidate owns — note it in the
output so the user can qualify it later.

Confirmation: "Registration successful!" dialog.
