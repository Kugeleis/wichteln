@echo off
REM Documentation commands for Windows

if "%1"=="docs-generate" goto docs-generate
if "%1"=="docs-serve" goto docs-serve
if "%1"=="docs-build" goto docs-build
if "%1"=="docs-deploy" goto docs-deploy
if "%1"=="docs" goto docs
if "%1"=="help" goto help

:help
echo Available documentation commands:
echo   docs.bat docs-generate  - Generate API documentation
echo   docs.bat docs-serve     - Start documentation server
echo   docs.bat docs-build     - Build documentation
echo   docs.bat docs-deploy    - Deploy to GitHub Pages
echo   docs.bat docs           - Generate and build documentation
goto end

:docs-generate
echo 🔄 Generating API documentation...
uv run python scripts/generate_docs.py
goto end

:docs-serve
echo 🌐 Starting documentation server...
echo    📚 Documentation: http://localhost:8000
uv run mkdocs serve
goto end

:docs-build
echo 🏗️ Building documentation...
uv run mkdocs build
goto end

:docs-deploy
echo 🚀 Deploying documentation to GitHub Pages...
uv run mkdocs gh-deploy
goto end

:docs
echo 📚 Generating and building documentation...
call docs.bat docs-generate
call docs.bat docs-build
echo ✅ Documentation built successfully!
echo    View at: ./site/index.html
goto end

:end
