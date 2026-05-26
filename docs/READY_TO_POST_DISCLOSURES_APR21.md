# DISCLOSURE DRAFTS - Ready to Post

## 🥇 PRIORITY 1: ettfemnio/dbd-server

**URL:** https://github.com/ettfemnio/dbd-server/issues/new

### Title:
```
🔴 CRITICAL: Production TLS Private Key Exposed in Repository
```

### Body:
```markdown
## Security Issue: Production Private Key Exposed

I've identified that your repository contains a **production TLS private key** that is actively used by your HTTPS server.

### Location
- **File:** `private/privatekey.key`
- **URL:** https://github.com/ettfemnio/dbd-server/blob/master/private/privatekey.key

### Confirmed Impact
This key is **hardcoded in production code** (`src/server.ts`):
```typescript
const httpsServer = https.createServer({
    key: fs.readFileSync(path.join('private', 'privatekey.key')),
    cert: fs.readFileSync(path.join('private', 'cert.crt')),
}, app)
httpsServer.listen(443, '0.0.0.0')
```

### Security Risks
- 🔴 **TLS/HTTPS Compromise** - Anyone can decrypt HTTPS traffic
- 🔴 **Server Impersonation** - Attackers can host fake instances
- 🔴 **Man-in-the-Middle Attacks** - Full cryptographic control exposed
- 🔴 **Player Data Exposure** - Game save encryption potentially compromised

### Immediate Actions Required
1. **URGENT:** Revoke the TLS certificate immediately
2. Generate new production key pair
3. Update all deployed servers with new certificate
4. Add `private/*.key` to `.gitignore`
5. Consider using environment variables for key paths
6. Remove from git history: `git-filter-repo --path private/privatekey.key --invert-paths`

### Timeline
I'm following responsible disclosure. This key has been publicly accessible and should be considered compromised.

Happy to discuss further or provide additional details.
```

---

## 🥈 PRIORITY 2: totaljs/superadmin  

**URL:** https://github.com/totaljs/superadmin/issues/new

### Title:
```
🔴 CRITICAL: SSL Private Key Exposed in Repository
```

### Body:
```markdown
## Security Issue: SSL Private Key Committed to Repository

I've identified that your repository contains an **SSL private key** with an associated certificate, which is used by the SuperAdmin application.

### Location
- **File:** `private/superadmin.key`
- **File:** `private/superadmin.csr` (matching certificate)
- **Key URL:** https://github.com/totaljs/superadmin/blob/master/private/superadmin.key

### Confirmed Impact
The key is **actively deployed** by the application (`definitions/superadmin.js`):
```javascript
var filename = Path.join(CONF.directory_ssl, 'superadmin.key');
Fs.copyFile(PATH.private('superadmin.key'), filename, NOOP);
```

And used for SSL configuration (`tasks/nginx.js`):
```javascript
domains.push({ 
  ssl_key: CONF.directory_ssl + 'superadmin.key',
  ssl_cer: CONF.directory_ssl + 'superadmin.csr'
});
```

### Security Risks
- 🔴 **Admin Panel Impersonation** - Anyone can authenticate as SuperAdmin
- 🔴 **SSL Certificate Forgery** - Can sign certificates as your organization
- 🟠 **Managed Server Compromise** - Access to servers running SuperAdmin

### Immediate Actions Required
1. **URGENT:** Generate new SSL key pair immediately
2. Rotate certificates on all deployments
3. Update `/www/ssl/superadmin.key` on all servers
4. Add to `.gitignore`:
   ```
   private/*.key
   private/*.csr
   ```
5. Remove from git history using BFG Repo-Cleaner or git-filter-repo
6. Monitor for unauthorized SuperAdmin instances

### Additional Context
- Verified RSA-2048 key
- Associated CSR present in repository
- Key modulus matches CSR (confirms usage)

### Timeline
Following responsible disclosure practices. Given the ~100 stars and 46 forks, multiple deployments may be affected.

Let me know if you need clarification or assistance with remediation.
```

---

## Posting Checklist

### ettfemnio/dbd-server (POST FIRST)
- [ ] Navigate to: https://github.com/ettfemnio/dbd-server/issues/new
- [ ] Paste title: `🔴 CRITICAL: Production TLS Private Key Exposed in Repository`
- [ ] Paste body text (above)
- [ ] Submit issue
- [ ] Copy issue URL: ____________________

### totaljs/superadmin (POST SECOND)
- [ ] Navigate to: https://github.com/totaljs/superadmin/issues/new  
- [ ] Paste title: `🔴 CRITICAL: SSL Private Key Exposed in Repository`
- [ ] Paste body text (above)
- [ ] Submit issue
- [ ] Copy issue URL: ____________________

---

## Notes
- Both disclosures ready
- Highest priority first (dbd-server = HTTPS in production)
- Professional tone, factual, actionable
- 7-day responsible disclosure timeline

---

## POSTING COMPLETION LOG

### Posted by User:
| Priority | Repository | Issue URL | Status |
|----------|------------|-----------|--------|
| 1 | ettfemnio/dbd-server | ____________________ | ⏳ PENDING |
| 2 | totaljs/superadmin | ____________________ | ⏳ PENDING |

Fill in issue URLs after posting, then commit this file.
