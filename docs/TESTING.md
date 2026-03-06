# 🧪 DailyClaw Testing Specification

> Apollo - Testing & Quality Assurance Standards

## 📋 Test Checklist

### 1. Link Verification

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1.1 | GitHub Repository Link | ⬜ | `https://github.com/G3niusYukki/dailyclaw` |
| 1.2 | Workflow Badge Link | ⬜ | `daily-evolution.yml/badge.svg` |
| 1.3 | MIT License Link | ⬜ | `https://opensource.org/licenses/MIT` |
| 1.4 | Stars Link | ⬜ | `.../stargazers` |
| 1.5 | Git Clone URL | ⬜ | `https://github.com/G3niusYukki/dailyclaw.git` |
| 1.6 | Internal Markdown Links | ⬜ | Cross-references within repo |

### 2. Badge Format Validation

| # | Badge | Expected Format | Status |
|---|-------|-----------------|--------|
| 2.1 | Daily Evolution | `https://github.com/.../actions/workflows/.../badge.svg` | ⬜ |
| 2.2 | License (MIT) | `https://img.shields.io/badge/License-MIT-yellow.svg` | ⬜ |
| 2.3 | Stars | `https://img.shields.io/github/stars/...` | ⬜ |

### 3. GitHub Actions Workflow Validation

| # | Check | Tool/Method | Status |
|---|-------|-------------|--------|
| 3.1 | `daily-evolution.yml` YAML Syntax | `yq` validation | ⬜ |
| 3.2 | `pages.yml` YAML Syntax | `yq` validation | ⬜ |
| 3.3 | Trigger Events | Manual review | ⬜ |
| 3.4 | Permissions Configuration | Manual review | ⬜ |
| 3.5 | Step Dependencies | Manual review | ⬜ |

### 4. Documentation Completeness

| # | Document | Location | Status |
|---|----------|----------|--------|
| 4.1 | README (CN) | `./README.md` | ⬜ |
| 4.2 | README (EN) | `./README_EN.md` | ⬜ |
| 4.3 | Contributing Guide | `./CONTRIBUTING.md` | ⬜ |
| 4.4 | Progress Board | `./PROGRESS.md` | ⬜ |
| 4.5 | Docs Index | `./docs/README.md` | ⬜ |
| 4.6 | Showcase README | `./showcase/README.md` | ⬜ |

### 5. Bilingual Consistency

| # | Section | CN Match EN | Status |
|---|---------|-------------|--------|
| 5.1 | Project Vision | ⬜ | |
| 5.2 | Architecture | ⬜ | |
| 5.3 | Key Features Table | ⬜ | |
| 5.4 | Six-Cat System | ⬜ | |
| 5.5 | Quick Start | ⬜ | |
| 5.6 | Timeline | ⬜ | |
| 5.7 | License | ⬜ | |

### 6. Code Quality

| # | Check | Status |
|---|-------|--------|
| 6.1 | No hardcoded secrets | ⬜ |
| 6.2 | Proper .gitignore | ⬜ |
| 6.3 | LICENSE file exists | ⬜ |
| 6.4 | Code of Conduct (optional) | ⬜ |

---

## 🧬 Test Scenarios

### Daily Evolution Workflow

```yaml
# Expected Behavior
- Trigger: Daily at 00:00 UTC or manual workflow_dispatch
- Create: evolution/YYYY/MM/DD.md if not exists
- Update: PROGRESS.md with new entry
- Commit: Auto-commit with 🤖 emoji
```

**Test Cases:**
- [ ] Verify cron schedule: `0 0 * * *` (UTC 00:00 = Beijing 08:00)
- [ ] Verify workflow_dispatch enables manual trigger
- [ ] Verify date variables correctly set
- [ ] Verify file creation logic
- [ ] Verify progress.md update logic
- [ ] Verify git configuration

### GitHub Pages Deployment

```yaml
# Expected Behavior
- Trigger: Push to master branch
- Build: Static HTML from README/docs/showcase/evolution
- Deploy: GitHub Pages
```

**Test Cases:**
- [ ] Verify trigger on `master` branch
- [ ] Verify artifact upload path
- [ ] Verify HTML template generation
- [ ] Verify deployment to github-pages environment

---

## 🔧 QA Tools & Commands

```bash
# Validate YAML syntax
yq e '.' .github/workflows/daily-evolution.yml

# Check for broken links (requires npm)
npm install -g broken-link-checker
blc https://github.com/G3niusYukki/dailyclaw -ro

# Check markdown links
npm install -g markdown-link-check
markdown-link-check README.md

# Validate all internal links
find . -name "*.md" -exec grep -oE '\]\([^)]+\)' {} \; | \
  grep -v "^\\(" | while read link; do
    echo "$link"
  done
```

---

## 📊 Quality Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Link Availability | 100% | - |
| Badge Validity | 100% | - |
| YAML Validation Pass | 100% | - |
| Bilingual Consistency | 100% | - |
| Documentation Coverage | 100% | - |

---

## 🚀 Release Checklist

Before each release, verify:

- [ ] All links tested and working
- [ ] All badges render correctly
- [ ] Workflows pass validation
- [ ] Documentation complete (CN + EN)
- [ ] No sensitive data in repository
- [ ] CONTRIBUTING.md up to date

---

## 📝 Issue Templates

### Bug Report Template
```markdown
## Description
[Clear description of the issue]

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS:
- Browser:
- Version:

## Screenshots
[If applicable]
```

### Feature Request Template
```markdown
## Feature Description
[What you want to add]

## Use Case
[Why this is needed]

## Suggested Implementation
[How you think it should work]

## Alternatives Considered
[Other solutions you thought of]
```

---

*Last Updated: 2026-03-07*
*Maintainer: Apollo (Testing & QA)*
