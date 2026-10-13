# Phenom

A company careers site running on Phenom: `/apply?jobSeqNo=<id>` on the company's careers domain.
No login for the first step.

## Steps

My Information → Experience → Application Questions → Terms → Review → Submit.

## Techniques

- **Native selects:** `form_input` by ref.
- **Set the country first:** it rebuilds the address block, wiping what was typed there.
- **CV size limit** can be 1 MB: read the limit before uploading — a file over it freezes the
  renderer.

## Stop conditions

Some tenants make an SMS opt-in required. When the profile's rules forbid SMS consent, stop:
`pending: SMS opt-in required`.
