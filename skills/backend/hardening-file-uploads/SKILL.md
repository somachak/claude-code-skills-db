---
name: hardening-file-uploads
description: Secures file upload flows for validation, scanning, storage isolation, content-type trust, and post-processing safety. Use when handling avatars, attachments, imports, or user-generated media.
when_to_use: file upload, content type, virus scan
allowed-tools: Read Grep Bash
---

## Secure File Handling

File uploads are vectors for RCE, XXE, path traversal, and storage attacks. The skill is validating MIME types, scanning for malware, storing securely, and serving safely.

### When to Use

- Building file upload features (avatars, documents, exports)
- Reviewing upload endpoints for security
- Designing a file storage service

### Decision Framework for Node.js/Python + S3 or Local Storage

1. **MIME type validation on server, not client.** Check file extension and magic bytes (first few bytes). Don't trust `Content-Type` header.
2. **Sanitize filenames.** Uploaded file "../../etc/passwd"? Sanitize to remove directory traversal. Use UUIDs instead of original names.
3. **Virus scanning is essential.** Use ClamAV, VirusTotal, or cloud-native scanning (AWS GuardDuty). Scan before storing.
4. **Store files outside the web root.** Never serve uploads directly from `public/` where they're executable. Stream from storage, serving as attachments.
5. **Enforce size limits.** 5GB upload = DoS. Set max file size; reject oversized uploads.

### Anti-patterns to Avoid

- Trusting MIME type header. Attacker uploads .exe with type=image/png.
- Storing files in web root with original name. User uploads shell.php; it's executable.
- No malware scanning. Uploaded file is a trojan; distributed to other users.
- Path traversal: filename "../../etc/passwd" stored as-is.

### Checklist

- [ ] Filename is sanitized (remove .., /, special chars)
- [ ] File extension is validated (whitelist: jpg, png, pdf, etc.)
- [ ] MIME type is validated server-side (magic bytes, not just header)
- [ ] File is scanned for malware before storage
- [ ] Max file size is enforced
- [ ] Files are stored outside web root (S3, cloud storage, or protected directory)
- [ ] Files are served with `Content-Disposition: attachment` (download, not execute)
- [ ] Test: upload .php file with image MIME type; verify it's rejected or served as attachment, not executed
