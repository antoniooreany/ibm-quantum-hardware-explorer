import os
import sys
import keyring

def get_token():
    # Try environment variable first
    token = os.getenv('IBM_QUANTUM_TOKEN')
    source = 'environment variable'
    if token:
        return token, source
    # Fallback to Credential Manager
    try:
        token = keyring.get_password('IBM_QUANTUM_TOKEN', 'IBM_QUANTUM_TOKEN')
        if token:
            source = 'Windows Credential Manager'
            return token, source
    except Exception:
        pass
    return None, None

if __name__ == '__main__':
    token, src = get_token()
    if token:
        print(f'✅ IBM Quantum token found via {src}.')
    else:
        sys.exit('❌ IBM Quantum token not found (neither env var nor Credential Manager).')
