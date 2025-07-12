# Single Point of Truth Documentation Strategy

This document outlines multiple strategies to achieve a single point of truth for documentation, eliminating scattered information across multiple markdown files.

## 🎯 Problem Statement

You identified that information is scattered across multiple files:
- Installation instructions in `README.md`, `docs/guide/quickstart.md`, `docs/DEVELOPMENT_SETUP.md`
- Commands repeated in various files
- Prerequisites mentioned in multiple places
- Platform-specific notes duplicated

## 🔧 Implemented Solutions

### Strategy 1: MkDocs Includes/Snippets ✅ IMPLEMENTED

**How it works:**
- Create reusable content blocks in `docs/_includes/` directory
- Use MkDocs snippets syntax: `--8<-- "_includes/file.md:section"`
- Single source files that get included where needed

**Files created:**
```
docs/
├── _includes/
│   ├── installation.md    # Prerequisites, installation steps
│   ├── commands.md        # Available commands
│   └── content.yaml       # Configuration data
└── _config/
    └── content.py         # Python configuration
```

**Usage example:**
```markdown
# In any documentation file
--8<-- "_includes/installation.md:prerequisites"
--8<-- "_includes/installation.md:installation-uv"
--8<-- "_includes/commands.md:common-commands"
```

**Benefits:**
- ✅ Immediate implementation with existing MkDocs setup
- ✅ Content is cached and reused automatically
- ✅ Changes in one place update everywhere
- ✅ Supports conditional content blocks

### Strategy 2: Configuration-Driven Generation ✅ IMPLEMENTED

**How it works:**
- Central configuration in `scripts/update_includes.py`
- Automated generation of include files
- Task command: `task update-includes`

**Benefits:**
- ✅ Single Python file contains all variable content
- ✅ Type-safe configuration
- ✅ Programmatic generation allows complex logic
- ✅ Integrated into build process

### Strategy 3: YAML Configuration Data ✅ IMPLEMENTED

**How it works:**
- Store configuration in `docs/_config/content.yaml`
- Can be used by template generators or MkDocs macros

**Benefits:**
- ✅ Human-readable configuration format
- ✅ Can be processed by multiple tools
- ✅ Version controlled alongside documentation

## 🚀 Advanced Strategies (Future Implementation)

### Strategy 4: MkDocs Macros Plugin

Install `mkdocs-macros-plugin` to use variables directly in markdown:

```yaml
# mkdocs.yml
plugins:
  - macros:
      include_dir: docs/_config
```

```markdown
# In documentation
{{ config.project.name }} requires {{ config.project.python_version }}
```

### Strategy 5: Custom Pre-commit Hook

Create a pre-commit hook that validates consistency:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: docs-consistency
      name: Documentation Consistency Check
      entry: python scripts/validate_docs_consistency.py
      language: python
      files: '^(README\.md|docs/.*\.md)$'
```

### Strategy 6: Symbolic Links (Advanced)

For identical sections, use symbolic links:
```bash
# Link common sections
ln -s ../shared/installation.md docs/guide/installation.md
ln -s ../shared/installation.md README_installation.md
```

### Strategy 7: Template Engine Integration

Use Jinja2 templates with MkDocs:

```yaml
# mkdocs.yml
plugins:
  - jinja2:
      template_folder: docs/_templates
```

## 📋 Implementation Checklist

### ✅ Completed
- [x] MkDocs snippets configuration
- [x] Created reusable include files
- [x] Updated quickstart guide to use includes
- [x] Created Python-based configuration
- [x] Added task command for updating includes
- [x] Integrated includes into documentation build process
- [x] YAML configuration file for future expansion

### 🔄 Next Steps (Optional)
- [ ] Install mkdocs-macros-plugin for variable substitution
- [ ] Create consistency validation script
- [ ] Add pre-commit hook for documentation validation
- [ ] Consider template engine for complex conditional content

## 🎯 Current Benefits Achieved

1. **Single Source of Truth**: All installation, commands, and platform notes are in `docs/_includes/`
2. **Automated Updates**: Run `task update-includes` to regenerate from central config
3. **Build Integration**: Includes are automatically updated during `task docs-generate`
4. **Maintainability**: Change information once, it updates everywhere
5. **Consistency**: No more version mismatches between files

## 📝 Usage Guidelines

### Adding New Shared Content

1. **Identify repeated information** across multiple files
2. **Add to configuration** in `scripts/update_includes.py`
3. **Create include section** with appropriate snippet markers
4. **Replace in source files** with snippet includes
5. **Run** `task update-includes` to generate
6. **Test** with `task docs-serve`

### Editing Shared Content

1. **Edit** the configuration in `scripts/update_includes.py`
2. **Run** `task update-includes` to regenerate includes
3. **Build docs** with `task docs` to see changes

### Best Practices

- Use descriptive snippet section names
- Keep include files focused (installation, commands, etc.)
- Document which files use which includes
- Test documentation builds after changes
- Use task commands rather than direct python execution

## 🔍 Monitoring & Validation

The current setup provides:
- **Build-time validation**: MkDocs will fail if includes are missing
- **Task integration**: `task docs` automatically updates includes
- **Version control**: All configuration is tracked in git
- **Documentation**: This strategy document explains the system

Your documentation now has a true single point of truth! 🎉
