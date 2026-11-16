<# 
.SYNOPSIS
    Test baseline (marked 18.1.3) on practice set - verify 720/720 pass
.DESCRIPTION
    Run this FIRST before recording to confirm baseline works.
    Right-click → "Run with PowerShell"
#>

. "$env:USERPROFILE\Aws\agent_ai\makefun\makefun-agent-setup.bat"

$REPO_DIR = "C:\Users\User\Aws\task-markdown-render-speed-02"
$INPUT_DIR = "C:\Users\User\AppData\Local\Temp\makefun-kits\markdown-render-speed-02-kit\practice\input"
$OUTPUT_DIR = "out"

Write-Host "🧪 Testing baseline on practice set..." -ForegroundColor Cyan

cd $REPO_DIR
$env:MAKEFUN_INPUT_DIR = $INPUT_DIR
$env:MAKEFUN_OUTPUT_DIR = $OUTPUT_DIR

node main.ts

Write-Host "`n📊 Comparing output..." -ForegroundColor Yellow

# Compare with expected
$out = Get-Content "$REPO_DIR\out\html.json" -Raw | ConvertFrom-Json
$exp = Get-Content "C:\Users\User\AppData\Local\Temp\makefun-kits\markdown-render-speed-02-kit\practice\reference\expected.json" -Raw | ConvertFrom-Json

$match = 0
for ($i = 0; $i -lt $out.Count; $i++) {
    $expectedHtml = $exp.cases[$i].html
    if ($out[$i] -eq $expectedHtml) { $match++ }
    elseif ($i -lt 5) { Write-Host "Mismatch at $i: $($out[$i].Substring(0,100)) != $($expectedHtml.Substring(0,100))" -ForegroundColor Red }
}

Write-Host "`n✅ Matched: $match / $($out.Count)" -ForegroundColor Green
Write-Host "Expected cases: $($exp.cases.Count)" -ForegroundColor Gray

if ($match -eq 720) {
    Write-Host "`n🎉 Baseline PASSED! Ready for recording." -ForegroundColor Green
} else {
    Write-Host "`n❌ Baseline FAILED! Fix before recording." -ForegroundColor Red
}