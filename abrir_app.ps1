$ProjectDir = "C:\Carrer_ops"
$AppUrl = "http://localhost:8501"

function Test-AppOnline {
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $AppUrl -TimeoutSec 2
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

Set-Location $ProjectDir

if (-not (Test-AppOnline)) {
    Start-Process `
        -WindowStyle Hidden `
        -FilePath "python" `
        -ArgumentList @(
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.headless",
            "true",
            "--server.port",
            "8501"
        ) `
        -WorkingDirectory $ProjectDir

    for ($tentativa = 1; $tentativa -le 20; $tentativa++) {
        Start-Sleep -Seconds 1

        if (Test-AppOnline) {
            break
        }
    }
}

Start-Process $AppUrl
