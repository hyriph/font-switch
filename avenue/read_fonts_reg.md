# 관리자 권한 PowerShell에서 실행하세요.

# 1. 레지스트리 키 경로 지정
$regPath = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts'

# 2. 폰트 이름과 파일명 쌍을 "이름"="값" 형식으로 추출하여 배열에 저장
$entries = Get-ItemProperty -Path $regPath |
    ForEach-Object {
        $_.PSObject.Properties |
        Where-Object { 
            # 시스템 메타 속성(PSPath, PSChildName 등) 제외
            $_.Name -notmatch '^PS' -and $_.Value 
        } |
        ForEach-Object {
            # "이름"="값" 형식으로 포맷
            '"{0}"="{1}"' -f $_.Name, $_.Value
        }
    }

# 3. 파일로 출력 (UTF8 인코딩)
$entries | Out-File -FilePath "$PWD\Fonts.txt" -Encoding UTF8

Write-Host "Fonts.txt 파일로 저장이 완료되었습니다 – 경로: $PWD\Fonts.txt"
