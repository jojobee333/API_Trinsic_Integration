from trinsic.proto.services.trustregistry.v1 import AddFrameworkRequest,RegisterMemberRequest,\
    UnregisterMemberRequest, GetMembershipStatusRequest

from app.models.constants import *
from app.models.models import GovernanceFramework

router = APIRouter()


@router.post('/governance/framework/add', tags=[trust_registry_tag])
async def add_governance_framework(framework: GovernanceFramework) -> dict:
    try:
        request = AddFrameworkRequest(governance_framework_uri=framework.uri, description=framework.description,
                                      name=framework.name)
        trinsic_response = await trinsic.trust_registry.add_framework(request=request)
        return trinsic_response
    except Exception as e:
        error_message = f"Failed to add new governance framework: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/governance/issuer/register', tags=[trust_registry_tag])
async def register_issuer(did_uri: str, framework_id: str, schema_uri: str) -> dict:
    try:
        request = RegisterMemberRequest(did_uri=did_uri, framework_id=framework_id, schema_uri=schema_uri, )
        trinsic_response = await trinsic.trust_registry.register_member(request=request)
        return trinsic_response
    except Exception as e:
        error_message = f"Failed to register issuer. " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/governance/issuer/remove', tags=[trust_registry_tag])
async def remove_issuer(did_uri: str, framework_id: str, schema_uri: str) -> dict:
    try:
        request = UnregisterMemberRequest(framework_id=framework_id, schema_uri=schema_uri, did_uri=did_uri)
        trinsic_response = await trinsic.trust_registry.unregister_member(request=request)
        return trinsic_response
    except Exception as e:
        error_message = f"Failed to remove issuer. " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/governance/issuer/remove', tags=[trust_registry_tag])
async def check_issuer_status(did_uri: str, framework_id: str, schema_uri: str) -> dict:
    try:
        request = GetMembershipStatusRequest(did_uri=did_uri, framework_id=framework_id, schema_uri=schema_uri)
        trinsic_response = await trinsic.trust_registry.get_membership_status(request=request)
        return trinsic_response
    except Exception as e:
        error_message = f"Failed to get issuer status." + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/governance/issuer/search', tags=[trust_registry_tag])
async def search_trust_registry(query: str = "c") -> dict:
    try:
        trinsic_response = await trinsic.trust_registry.search(query=f"SELECT * FROM {query}")
        return trinsic_response
    except Exception as e:
        error_message = f"Failed to get issuer status." + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)
