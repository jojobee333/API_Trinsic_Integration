from app.models.constants import *

router = APIRouter()


@router.post('/add-identity/initial', tags=[identity_tag])
async def add_identity_initial(identity: str, wallet_auth_token: str) -> dict:
    """Initializes adding an identity to a wallet."""
    # working
    provider = IdentityProvider.EMAIL
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    requestInit = AddExternalIdentityInitRequest(identity=identity, provider=provider)
    try:
        responseInit = await trinsic_wallet.wallet.add_external_identity_init(request=requestInit)
        return {"challenge": responseInit.challenge, "msg": "Success. Please check email for OTP."}
    except Exception as e:
        error_message = f"Failed to initialize external identity: {str(e)}"
        raise HTTPException(status_code=status_code, detail=error_message)

@router.post('/add-identity/confirm', tags=[identity_tag])
async def add_identity_confirm(code: str, wallet_auth_token: str, challenge: str) -> dict:
    # working
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    requestConfirm = AddExternalIdentityConfirmRequest(challenge=challenge, response=code)
    try:
        responseConfirm = await trinsic_wallet.wallet.add_external_identity_confirm(request=requestConfirm)
        return {"msg": "Identity added successfully.", "response": responseConfirm}
    except Exception as e:
        error_message = f"Failed to confirm external identity: {str(e)}"
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/remove-identity', tags=[identity_tag])
async def remove_identity(identity: str) -> dict:
    """Removes an identity from an authenticated wallet."""
    # working
    request = RemoveExternalIdentityRequest(identity=identity)
    try:
        trinsic_response = await trinsic.wallet.remove_external_identity(request=request)
        return {"response": trinsic_response}
    except Exception as e:
        error_message = f"Failed to remove external identity: {str(e)}"
        raise HTTPException(status_code=status_code, detail=error_message)


