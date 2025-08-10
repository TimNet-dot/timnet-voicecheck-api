from fastapi import Request, HTTPException

VALID_KEYS = ["timnet-owner-key", "trusted-client-key"]

async def verify_api_key(request: Request):
    key = request.headers.get("Authorization")
    if key not in VALID_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")