$baseUrl = "http://localhost:8080"

Write-Host "--- 1. Register User ---" -ForegroundColor Cyan
$registerBody = @{
    username = "test@example.com"
    password = "password123"
    fullName = "Test User"
    phoneNumber = "9999999999"
} | ConvertTo-Json

try {
    $regRes = Invoke-WebRequest -Uri "$baseUrl/api/auth/register" -Method Post -Body $registerBody -ContentType "application/json" -UseBasicParsing
    Write-Host "Status: $($regRes.StatusCode)"
    Write-Host "Body: $($regRes.Content)"
} catch {
    Write-Host "Error in registration: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        Write-Host "Response Body: $($reader.ReadToEnd())"
    }
}

Write-Host "`n--- 2. Login User ---" -ForegroundColor Cyan
$loginBody = @{
    username = "test@example.com"
    password = "password123"
} | ConvertTo-Json

try {
    $loginRes = Invoke-WebRequest -Uri "$baseUrl/api/auth/login" -Method Post -Body $loginBody -ContentType "application/json" -SessionVariable sess -UseBasicParsing
    Write-Host "Status: $($loginRes.StatusCode)"
    Write-Host "Body: $($loginRes.Content)"
    
    # Safely print cookie header if present
    if ($loginRes.Headers.ContainsKey("Set-Cookie")) {
        Write-Host "Cookie header: $($loginRes.Headers['Set-Cookie'])" -ForegroundColor Green
    } else {
        Write-Host "No Set-Cookie header found, checking all headers..."
        $loginRes.Headers
    }
} catch {
    Write-Host "Error in login: $_" -ForegroundColor Red
}

Write-Host "`n--- 3. Create Transaction ---" -ForegroundColor Cyan
$txBody = @{
    amount = 5000
    date = "2024-01-10"
    category = "Salary"
    description = "Test"
} | ConvertTo-Json

try {
    $txRes = Invoke-WebRequest -Uri "$baseUrl/api/transactions" -Method Post -Body $txBody -ContentType "application/json" -WebSession $sess -UseBasicParsing
    Write-Host "Status: $($txRes.StatusCode)"
    Write-Host "Body: $($txRes.Content)"
} catch {
    Write-Host "Error in creating transaction: $_" -ForegroundColor Red
}

Write-Host "`n--- 4. Get Transactions ---" -ForegroundColor Cyan
try {
    $getRes = Invoke-WebRequest -Uri "$baseUrl/api/transactions" -Method Get -WebSession $sess -UseBasicParsing
    Write-Host "Status: $($getRes.StatusCode)"
    Write-Host "Body: $($getRes.Content)"
} catch {
    Write-Host "Error in getting transactions: $_" -ForegroundColor Red
}
