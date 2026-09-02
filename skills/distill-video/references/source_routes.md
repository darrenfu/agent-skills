# Source Routes

Read only the section for the current platform. Preserve the original URL, final URL, metadata, resolved assets, and generated evidence in the artifact folder.

## YouTube

1. Probe without downloading:

   ```bash
   python3 <skill-dir>/scripts/video_mvp.py \
     "https://www.youtube.com/watch?v=<id>" \
     --out-dir artifacts/youtube_<id> \
     --probe-only
   ```

2. Prefer official subtitles or a browser-exported YouTube transcript when available. Otherwise download and transcribe the audio.
3. The helper uses an installed `yt-dlp`, or `uvx --from yt-dlp yt-dlp` when `uvx` is available.
4. Do not claim success from a title/search result alone. Require resolved metadata and a transcript, captions, or downloaded media suitable for the user's request.

## Xiaohongshu video

1. Try `video_mvp.py` first. SSR pages commonly expose `noteDetailMap` and a `masterUrl`.
2. A direct HTTP 403/404 on a short link is a route failure, not proof that the post was deleted.
3. If the generic route fails and the local `xiaohongshu-skills` package is available, run from that package directory:

   ```bash
   python scripts/cli.py get-share-detail \
     --url "<public-share-url>"
   ```

4. Use the returned note metadata and video URL, or inspect the browser-resolved page assets. Download the actual media and verify it is playable before transcription.
5. Do not require login when the public share-detail route succeeds.

## Xiaohongshu public image/text post

Use the anonymous share-detail route before any login flow:

```bash
python scripts/cli.py get-share-detail \
  --url "<public-share-url>" \
  --download-images \
  --output-dir "<artifact-dir>/images"
```

Acceptance requires structured note text plus every public image downloaded successfully. OCR image text only when it carries independent content, and keep these layers separate:

- Post caption/body
- Text visibly embedded in images
- Comments, only when the user requests or needs them
- Analyst inference

If the public route returns a login or risk-control gate, report that state and switch to the approved authenticated route. Do not bypass private, deleted, or restricted content.

## Stockbee and other authenticated video pages

Use the user's approved Chrome session when the page requires authentication.

1. Open the original page in Chrome. A request to retrieve content from that page implies login may be used for that site.
2. Use only visible page state and visible Chrome/system autofill. Never inspect browser cookies, local storage, profiles, saved-password databases, or credential files; never print credentials.
3. If visible autofill populates the login form, submit through the normal page UI. Stop after the first rejected credential or unexpected authentication error. Hand MFA or CAPTCHA to the user.
4. After navigation, confirm the intended content page is visible rather than a login redirect.
5. Inspect observable page assets. Prefer the rendered page's video resource or browser asset export, then save the media in the artifact folder.
6. Verify the local file is playable and record the page URL, asset URL or browser-export method, and authentication method as `Chrome visible autofill`; never record credential values.

Authentication grants access only to content the user is entitled to view. It does not authorize bypassing paywalls, copying credentials, or publishing restricted media.
