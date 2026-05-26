---
title: Impact Assessment - April 21 Hunt Findings
date: 2026-04-21
status: verified
---

## 🔍 Impact Verification Complete

### Finding #1: totaljs/superadmin

| Field | Value |
|-------|-------|
| **Repository** | totaljs/superadmin |
| **File** | `private/superadmin.key` |
| **Stars** | 99 ⭐ |
| **Forks** | 46 |
| **Description** | Manage your Linux servers and Total.js applications easily |
| **Last Updated** | 2026-02-01 |
| **File Size** | 1,704 bytes |
| **File Exists** | ✅ YES (still accessible) |
| **Last Commit** | 2020-11-15 |

**Impact Level: MEDIUM**
- Server management tool with moderate user base
- Key may be used for SSH/authentication to managed servers
- Potential server compromise across 99+ user deployments

**Risk Assessment:**
- ⚠️ **Active exposure** - key still in main branch
- ⚠️ **Production impact** - server management app
- ✅ **Limited reach** - 99 stars vs enterprise-scale

---

### Finding #2: ettfemnio/dbd-server

| Field | Value |
|-------|-------|
| **Repository** | ettfemnio/dbd-server |
| **File** | `private/privatekey.key` |
| **Stars** | 18 ⭐ |
| **Forks** | 4 |
| **Description** | N/A (database server project) |
| **Last Updated** | 2026-02-18 |
| **File Size** | 1,703 bytes |
| **File Exists** | ✅ YES (still accessible) |
| **Last Commit** | 2021-02-05 |

**Impact Level: MEDIUM**
- Database server application
- Key likely for DB encryption or SSH access
- Lower exposure but still cryptographic compromise

**Risk Assessment:**
- ⚠️ **Active exposure** - key still in main branch
- ⚠️ **Database implication** - "dbd" suggests database daemon
- ✅ **Lower adoption** - 18 stars

---

## ⚠️ CRITICAL: FILES STILL EXPOSED

Both private keys remain **PUBLICLY ACCESSIBLE** on GitHub:

1. https://github.com/totaljs/superadmin/blob/master/private/superadmin.key
2. https://github.com/ettfemnio/dbd-server/blob/master/private/privatekey.key

**Immediate Action Required:**
- Both repositories need disclosure posted
- Key rotation should be assumed urgent
- Git history cleanup recommended

---

## Hunt Summary

| Metric | Value |
|--------|-------|
| Hunt Date | 2026-04-21 18:40 |
| Discoveries | 2 |
| Files Checked | 5 |
| Hit Rate | 40% |
| Rate Limit Reached | Yes (30 searches) |

---

## Rate Limit Status

🚨 **Search API exhausted** - 30 searches in ~5 minutes
- Resets hourly
- Need to wait ~55 minutes before next hunt
- Alternative: Use GitHub Events API or commit stream
