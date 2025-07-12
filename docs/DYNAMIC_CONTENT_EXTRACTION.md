# ✨ Dynamic Content Extraction Implementation

## 🎯 Achievement Summary

Your content configuration script now **dynamically extracts information from your actual project structure** instead of using hardcoded values!

## 📊 Information Sources

### ✅ What Gets Extracted Automatically

| Information | Source File/Command | Extraction Method |
|-------------|-------------------|------------------|
| **Python Version** | `uv.lock` | Parses `requires-python = ">=3.12"` |
| **Repository URL** | `git remote origin` | Git command + fallback to README |
| **Project Description** | `README.md` | First substantial paragraph |
| **Project Version** | `src/*//__init__.py` | Searches for `__version__ = "x.x.x"` |
| **Task Commands** | `Taskfile.yml` | Parses task names + descriptions |
| **Make Commands** | `Makefile` | Extracts targets with comments |

### 🔍 Current Extraction Results

From your last run:
```
🐍 Python Version: 3.12 (from uv.lock)
📦 Repository: https://github.com/Kugeleis/wichteln (from git)
📝 Description: "A modern Flask web application for organizing Secret Santa events..."
🎯 Tasks: 15 commands extracted from Taskfile.yml
🔧 Make: 3 commands extracted from Makefile
```

## 🏗️ Architecture

```
docs/_config/content.py          # Dynamic extraction logic
        ↓
scripts/update_includes.py       # Template generator
        ↓
docs/_includes/*.md             # Generated include files
        ↓
docs/**/*.md                    # Documentation files using includes
```

## 🔄 Automatic Updates

Your documentation now automatically stays in sync with:

1. **Python Requirements**: Changes in `uv.lock` update all docs
2. **Repository Changes**: Git remote changes update clone commands
3. **Task Definitions**: New tasks in `Taskfile.yml` appear in docs
4. **Project Description**: README updates flow to all documentation

## 🎪 Benefits Achieved

### ✅ **True Single Point of Truth**
- **Before**: Hardcoded values scattered across multiple files
- **After**: Dynamic extraction from actual project structure

### ✅ **Self-Maintaining Documentation**
- **Before**: Manual updates required when changing versions/commands
- **After**: `task docs` automatically syncs everything

### ✅ **Zero Configuration Drift**
- **Before**: Documentation could become outdated
- **After**: Always reflects current project state

### ✅ **Developer-Friendly**
- **Before**: Edit in multiple places
- **After**: Change once in source, updates everywhere

## 🚀 Usage Examples

### Adding a New Task
```yaml
# In Taskfile.yml
new-feature:
  desc: "Runs the new amazing feature"
  cmds:
    - echo "Amazing!"
```
Result: Automatically appears in all documentation after `task docs`

### Updating Python Version
```toml
# In uv.lock (happens during uv update)
requires-python = ">=3.13"
```
Result: All documentation automatically shows Python 3.13 requirement

### Changing Repository
```bash
git remote set-url origin https://github.com/newowner/newname.git
```
Result: All clone commands automatically update

## 📋 Quality Assurance

The system provides:
- **Build-time validation**: Missing includes cause build failures
- **Source tracking**: Shows exactly where each piece of information comes from
- **Fallback values**: Graceful degradation if extraction fails
- **Error handling**: Clear error messages if configuration issues occur

## 🔮 Future Enhancements

The foundation supports easy addition of:
- Package dependency extraction from `uv.lock`
- Feature detection from source code
- API endpoint discovery
- Changelog generation from git history
- License information extraction

Your documentation system is now **truly dynamic and self-maintaining**! 🎉
