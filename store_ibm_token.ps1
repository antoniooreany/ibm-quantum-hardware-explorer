# --------------------------------------------------------------
    # store_ibm_token.ps1
    # Securely store the IBM Quantum API token in Windows Credential Manager
    # --------------------------------------------------------------

    # -----------------------------------------------------------------
    # 1️⃣  Define the generic credential name – must match the name used
    #     in the Python code (keyring.get_password('IBM_QUANTUM_TOKEN', …))
    # -----------------------------------------------------------------
    $CredName = 'IBM_QUANTUM_TOKEN'   # <-- generic target name

    Write-Host "`n🔐  Storing credential: $CredName`n"

    # -----------------------------------------------------------------
    # 2️⃣  Prompt for the token (input hidden, stored as SecureString)
    # -----------------------------------------------------------------
    $SecureToken = Read-Host -AsSecureString "Enter your IBM Quantum API token"

    # -----------------------------------------------------------------
    # 3️⃣  Convert the SecureString to plain‑text **only in memory**
    #     (the plain text never touches console output or files)
    # -----------------------------------------------------------------
    $PlainToken = [Runtime.InteropServices.Marshal]::PtrToStringUni(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureToken)
    )

    # -----------------------------------------------------------------
    # 4️⃣  Remove any existing credential with the same generic name
    # -----------------------------------------------------------------
    cmdkey /delete:$CredName 2>$null

    # -----------------------------------------------------------------
    # 5️⃣  Add the new generic credential
    # -----------------------------------------------------------------
    cmdkey /generic:$CredName /user:$CredName /pass:$PlainToken

    # -----------------------------------------------------------------
    # 6️⃣  Verify that it was stored correctly
    # -----------------------------------------------------------------
    if (cmdkey /list | Select-String $CredName) {
        Write-Host "`n✅  Token stored successfully in Credential Manager."
    } else {
        Write-Warning "`n⚠️  Credential not found – something went wrong."
    }

    # -----------------------------------------------------------------
    # 7️⃣  Clean up the in‑memory plain‑text variable (good hygiene)
    # -----------------------------------------------------------------
    Remove-Variable PlainToken -Force
    