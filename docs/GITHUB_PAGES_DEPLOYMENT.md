# Documentation Deployment Guide

This project uses GitHub Actions to automatically build and deploy documentation to GitHub Pages.

## 🚀 Automatic Deployment

### When Documentation is Deployed

Documentation is automatically built and deployed when:

- ✅ **Push to main/master branch** with changes to:
  - `docs/` directory (markdown files)
  - `scripts/` directory (documentation generators)
  - `mkdocs.yml` (site configuration)
  - `pyproject.toml` or `uv.lock` (dependencies)

- ✅ **Manual trigger** via GitHub Actions workflow dispatch

### What Happens During Deployment

1. **🔧 Environment Setup**
   - Ubuntu latest runner
   - Python 3.12 installation
   - UV package manager setup with caching

2. **📚 Documentation Generation**
   - Generate API documentation from source code
   - Update includes from project configuration
   - Build static site with MkDocs

3. **🌐 GitHub Pages Deployment**
   - Upload built site as Pages artifact
   - Deploy to `https://<username>.github.io/<repository>/`

4. **🔍 Quality Checks**
   - Run pre-commit hooks (linting, formatting, security)
   - Test documentation generation pipeline
   - Check documentation links (optional, non-blocking)

## 📋 Pull Request Previews

For pull requests that modify documentation:

- ✅ Documentation builds are tested
- ✅ Preview artifacts are uploaded (7-day retention)
- ✅ Quality checks must pass
- ❌ No automatic deployment (preview only)

## 🛠️ Local Development

### Quick Commands

```bash
# Generate and serve documentation locally
task docs-serve

# Build documentation for testing
task docs-build

# Generate API documentation
task docs-generate

# Update includes from project data
task update-includes
```

### Manual Commands

```bash
# Generate API documentation
uv run python scripts/generate_docs.py

# Update includes from project configuration
uv run python scripts/update_includes.py

# Build documentation
uv run mkdocs build

# Serve documentation locally
uv run mkdocs serve

# Deploy to GitHub Pages (if configured)
uv run mkdocs gh-deploy
```

## 🔧 Configuration Files

- **`.github/workflows/docs.yml`** - Main CI/CD workflow
- **`mkdocs.yml`** - MkDocs site configuration
- **`.htmltest.yml`** - Link checking configuration
- **`docs/_config/content.py`** - Dynamic content extraction
- **`scripts/generate_docs.py`** - API documentation generator
- **`scripts/update_includes.py`** - Include file generator

## 🌐 Published Documentation

Once set up, your documentation will be available at:

```
https://<username>.github.io/<repository>/
```

### First-Time Setup

1. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: "GitHub Actions"
   - Save settings

2. **Push Documentation Changes**:
   - Commit any documentation changes
   - Push to main/master branch
   - GitHub Actions will automatically deploy

3. **Verify Deployment**:
   - Check Actions tab for workflow status
   - Visit the GitHub Pages URL once deployed

## 🚨 Troubleshooting

### Common Issues

**Build Fails with Missing Dependencies**
```bash
# Solution: Update uv.lock
uv lock
git add uv.lock
git commit -m "Update dependencies"
```

**MkDocs Build Errors**
```bash
# Solution: Test locally first
uv run mkdocs build --strict --verbose
```

**Link Checker Warnings**
- Link checking is non-blocking and optional
- Warnings don't prevent deployment
- Fix broken links for better documentation quality

### Workflow Status

Monitor deployment status:
- ✅ **Actions tab** - Real-time workflow progress
- ✅ **Deployments section** - GitHub Pages deployment history
- ✅ **Pages settings** - Current deployment URL and status

## 📈 Performance Optimizations

The workflow includes several optimizations:

- **🚀 Caching**: UV dependencies cached between runs
- **📁 Path Filtering**: Only runs when documentation files change
- **⚡ Parallel Jobs**: Quality checks run in parallel with build
- **🎯 Conditional Deploy**: Only deploys from main/master branch
- **💾 Cache Pruning**: Minimizes cache size for efficiency

## 🔒 Security

- **🔐 Minimal Permissions**: Only required permissions granted
- **🛡️ Pre-commit Hooks**: Security scanning with bandit
- **🔍 Dependency Scanning**: Automated dependency vulnerability checks
- **📝 Audit Trail**: All deployments logged in GitHub Actions
