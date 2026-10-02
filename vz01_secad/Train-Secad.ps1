param (
    [Parameter(Mandatory=$true)]
    [string]$ConceptName,
    
    [Parameter(Mandatory=$true)]
    [string]$Description
)

$MemoryPath = "C:\Users\note\vz\vz01_secad\brain"
$MemoryFile = "$MemoryPath\secad_memory.json"

# 메모리 폴더 생성
if (!(Test-Path $MemoryPath)) {
    New-Item -ItemType Directory -Force -Path $MemoryPath | Out-Null
}

# 기존 메모리 로드
$MemoryData = @{}
if (Test-Path $MemoryFile) {
    $Content = Get-Content $MemoryFile -Raw
    if ($Content) {
        $MemoryData = $Content | ConvertFrom-Json -AsHashtable
    }
}

# 새 개념 학습 (저장)
$MemoryData[$ConceptName] = @{
    "Description" = $Description
    "LearnedAt" = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
}

# 디스크에 기록 (토큰 소모 없는 영구 학습)
$MemoryData | ConvertTo-Json -Depth 10 | Set-Content $MemoryFile -Encoding UTF8

Write-Host "[SECAD Learning Complete] '$ConceptName' 개념이 영구 메모리에 저장되었습니다." -ForegroundColor Green
Write-Host "AI는 다음 도면 설계 시 이 개념을 자동으로 참고합니다."
