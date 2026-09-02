---
title: Decision — RMF / Shop Attachment Rendering
type: decision
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-09-02/project_shop_rmf_postdemo_followups_20260831.md
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp1144_zendesk_attachments.md
  - raw/fls-work/git/2026-09-02/inventory-lookup/adr-signals.json
  - raw/fls-work/inventory-lookup-docs/2026-09-02/
related:
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[initiatives/pie-shop-replacement.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [decision, clearview, shop, rmf, attachments, security]
---

# Decision — RMF / Shop Attachment Rendering

**Context:** Post-demo ask — email threads, vendor docs, BOLs, and iPhone image formats must upload and remain usable on Shop/RMF requests. Raw download-only UX was insufficient; `<img>` on HEIC broke in Chrome/Firefox/Edge.

**Decision:**

1. Prefer **server-side rendering / view links** for accepted types instead of forcing raw downloads.
2. Expand accept list: images/PDF/HEIC + vendor docs (`.docx`/`.xlsx`) + email exports (`.eml`/`.msg`).
3. HEIC/HEIF → convert to JPEG (or view-link) so thumbnails work outside Safari.
4. `.docx` → sanitized HTML (mammoth); `.xlsx` → sanitized HTML table; sandbox rendered previews.
5. **Resolve MIME from extension** when the browser reports `application/octet-stream` / empty — otherwise validation rejects whitelisted files before S3.
6. Store the **resolved** content type on S3 PutObject (not the raw browser MIME) so the serve route's render switch can match (live bug: `.msg` stored as octet-stream, listed but never rendered).
7. Harden sanitizer: drop unconstrained inline `style`; treat previews as **stored XSS** risk (uploader ≠ viewer, same-origin session cookie).
8. Zendesk-linked attachments can show inline on detail where supported.

**Status:** Done for the post-demo attachments verification story.

**Consequences:** Preview path is a security surface — sanitizer + sandbox stay mandatory. New file types need an explicit accept + render strategy, not silent `<img>` assumptions. Upload validation and S3 metadata must share one resolved MIME helper.
