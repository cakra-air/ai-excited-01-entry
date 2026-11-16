<# 
.SYNOPSIS
    Record + Codex build + Submit for make.fun markdown-render-speed-02
.DESCRIPTION
    Run this script in a CLEAN PowerShell terminal (NOT Hermes, NOT VS Code integrated terminal if contaminated).
    Best: Right-click this file → "Run with PowerShell" 
    Or: Terminal → New Terminal → PowerShell → paste: .\record-and-submit.ps1
#>

# Load make.fun agent config for @vanstya
. "$env:USERPROFILE\Aws\agent_ai\makefun\makefun-agent-setup.bat"

# Paths
$KIT_DIR = "C:\tmp\makefun-kits\markdown-render-speed-02-kit"
$REPO_DIR = "C:\Users\User\Aws\task-markdown-render-speed-02"

Write-Host "📦 Kit: $KIT_DIR" -ForegroundColor Cyan
Write-Host "📁 Repo: $REPO_DIR" -ForegroundColor Cyan
Write-Host "🔑 API Key loaded: $env:MAKEFUN_API_KEY" -ForegroundColor Green

# Step 1: Record + Codex (wrap mode)
Write-Host "`n🎬 Starting recording + Codex..." -ForegroundColor Yellow
Write-Host "   This will take 5-15 minutes. Wait for Codex to finish, then press Ctrl+C to seal." -ForegroundColor Gray

cd $KIT_DIR
node cli/makefun.mjs record --competition markdown-render-speed-02 --source $REPO_DIR -- npx @openai/codex exec --sandbox danger-full-access "Optimize parse.js to be faster than marked 18.1.3 while returning IDENTICAL HTML for all 720 test cases. Kit at C:\tmp\makefun-kits\markdown-render-speed-02-kit. Test with: `$env:MAKEFUN_INPUT_DIR='C:\Users\User\AppData\Local\Temp\makefun-kits\markdown-render-speed-02-kit\practice\input'; `$env:MAKEFUN_OUTPUT_DIR='out'; node main.ts"

# After Ctrl+C, the recording ID will be printed. 
# Copy it and run Step 2 manually:
Write-Host "`n✅ Recording sealed! Copy the RECORDING_ID above, then run:" -ForegroundColor Green
Write-Host "   node cli/makefun.mjs submit --competition markdown-render-speed-02 --recording <RECORDING_ID> --repo-url https://github.com/cakra-air/task-markdown-render-speed-02 --commit c462609 --title 'Faster marked drop-in' --keypair ~/Aws/agent_ai/makefun/agent-keypair.json" -ForegroundColor Cyan