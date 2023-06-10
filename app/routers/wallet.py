from trinsic.proto.services.universalwallet.v1 import DeleteItemRequest
from app.constants import *
from app.models.models import JsonObject

router = APIRouter()

@router.post('/wallet/create', tags=[wallet_tag])
async def create_sub_wallet() -> dict:
    """Creates a new wallet."""
    # API working
    request = CreateWalletRequest(ecosystem_id=ecosystem_id)
    try:
        trinsic_response = await trinsic.wallet.create_wallet(
            request=request)
        # wallet_auth_token = response.wallet_auth_token
        response = {"wallet_auth_token": trinsic_response.auth_token, "wallet_info": trinsic_response.wallet}
        return response
    except Exception as e:
        error_message = f"Failed to create new wallet: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.get('/wallet/search', tags=[wallet_tag])
async def search_wallet(wallet_auth_token: str, query: str = None) -> dict:
    """Return items from specified wallet."""
    # API working |
    query = "." + query if query else None
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    try:
        request = SearchRequest(query=f"SELECT * FROM c{query}")
        wallet_items = await trinsic_wallet.wallet.search_wallet(request=request)
        items = [json.loads(item) for item in wallet_items.items]
        return {"wallet_items": items}
    except Exception as e:
        error_message = f"Failed to search wallet: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/wallet/item/insert', tags=[wallet_tag])
async def insert_item(document_json: JsonObject, wallet_auth_token: str) -> dict:
    """Takes Credential and Auth Token of a wallet and inserts a json_object into a wallet. Please pass the json_object
    into the request body."""
    # working
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    try:
        request = InsertItemRequest(item_json=json.dumps(document_json.json_object), item_type="VerifiableCredential")
        trinsic_response = await trinsic_wallet.wallet.insert_item(request=request)
        return {"item_id": trinsic_response.item_id}
    except Exception as e:
        error_message = f"Failed to insert item: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.get('/wallet/item/retrieve', tags=[wallet_tag])
async def retrieve_item(wallet_auth_token: str, item_id: str) -> dict:
    """Retrieves a specific item from a wallet based on item id."""
    # retrieves wallet item based on the id.
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    request = GetItemRequest(item_id)
    try:
        trinsic_response = await trinsic_wallet.wallet.get_item(request=request)
        return {"item": json.loads(trinsic_response.item_json)}
    except Exception as e:
        error_message = f"Failed to retrieve item from wallet: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.get('/wallet/item/delete', tags=[wallet_tag])
async def delete_item(wallet_auth_token: str, item_id: str) -> dict:
    """Deletes a specific item from a wallet based on id"""
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    request = DeleteItemRequest(item_id=item_id)
    try:
        trinsic_response = await trinsic_wallet.wallet.delete_item(request=request)
        return {"response": trinsic_response}
    except Exception as e:
        error_message = f"Failed to delete item: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/wallet/delete', tags=[wallet_tag])
async def delete_sub_wallet(did: str) -> dict:
    """Deletes a specified wallet."""
    # API working
    request = DeleteWalletRequest(did_uri=did)
    try:
        response = await trinsic.wallet.delete_wallet(
            request=request)
        if not response:
            return {"msg": "Wallet has been deleted."}
        else:
            detail = "Bad Request."
            raise HTTPException(status_code=status_code, detail=detail)
    except Exception as e:
        error_message = f"Failed to delete item: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/wallet/authenticate-initial', tags=[wallet_tag])
async def auth_wallet_initial(identity_email: str, wallet_auth_token: str) -> dict:
    """Initializes wallet authentication. Copy challenge and paste it into authenticate confirm to complete."""
    # Not working with sub wallets
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    requestInit = AuthenticateInitRequest(identity=identity_email,
                                          ecosystem_id=ecosystem_id,
                                          provider=IdentityProvider.EMAIL)
    try:
        responseInit = await trinsic_wallet.wallet.authenticate_init(request=requestInit)
        return {"challenge": responseInit.challenge, "msg": "Success. Please check email for OTP."}
    except Exception as e:
        error_message = f"Failed to initialize wallet authentication: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/wallet/authenticate-confirm', tags=[wallet_tag])
async def auth_wallet_confirm(code: str, challenge: str, wallet_auth_token: str) -> dict:
    """Must run auth wallet initial in order to input the challenge."""
    # Not working with sub wallets
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    requestConfirm = AuthenticateConfirmRequest(challenge=challenge, response=code)
    try:
        responseConfirm = await trinsic_wallet.wallet.authenticate_confirm(request=requestConfirm)
        print(responseConfirm)
        return {"wallet_auth_token": responseConfirm.auth_token}
    except Exception as e:
        error_message = f"Failed to authenticate wallet: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)
