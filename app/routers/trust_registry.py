from trinsic.proto.services.trustregistry.v1 import AddFrameworkRequest, RegisterMemberRequest, \
    UnregisterMemberRequest, GetMembershipStatusRequest

from app.constants import *
from app.models.models import GovernanceFramework

router = APIRouter()


@router.post('/governance/issuer/register', tags=[trust_registry_tag])
async def register_issuer(did_uri: str, schema_uri: str, wallet_auth_token: str):
    try:
        request = RegisterMemberRequest(did_uri=did_uri, schema_uri=schema_uri)
        trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
        trinsic_response = await trinsic_wallet.trust_registry.register_member(request=request)
        return trinsic_response
    except Exception as e:
        error_message = f"Failed to register issuer. " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/governance/issuer/remove', tags=[trust_registry_tag])
async def remove_issuer(did_uri: str, schema_uri: str) -> dict:
    try:
        request = UnregisterMemberRequest(did_uri=did_uri, schema_uri=schema_uri)
        trinsic_response = await trinsic.trust_registry.unregister_member(request=request)
        return trinsic_response
    except Exception as e:
        error_message = f"Failed to remove issuer. " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/governance/issuer/remove', tags=[trust_registry_tag])
async def check_issuer_status(did_uri: str, schema_uri: str) -> dict:
    try:
        request = GetMembershipStatusRequest(did_uri=did_uri, schema_uri=schema_uri)
        trinsic_response = await trinsic.trust_registry.get_membership_status(request=request)
        return trinsic_response
    except Exception as e:
        error_message = f"Failed to get issuer status." + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/governance/issuer/search', tags=[trust_registry_tag])
async def search_trust_registry(query: str = None) -> dict:
    query = "." + query if query else None
    try:
        trinsic_response = await trinsic.trust_registry.search()
        return trinsic_response.items_json
    except Exception as e:
        error_message = f"Failed to get issuer status." + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)
