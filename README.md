# Offline Phishing Email Triage

Analyzes saved `.eml` files without opening links or contacting external services. It inventories sender/reply-to domains, URL hosts, attachment names, sizes, and SHA-256 hashes.

```bash
python main.py sample.eml
python -m unittest -v
```

The output supports analyst review and preserves uncertainty; it does not label an email malicious automatically.
