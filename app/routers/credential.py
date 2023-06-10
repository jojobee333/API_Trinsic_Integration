from app.constants import *
from app.models.models import JsonObject

router = APIRouter()


@router.post('/credential/issue', tags=[cred_tag])
async def issue_credential_from_template(auth_token: str, template_id: str, credential: JsonObject) -> dict:
    """Takes a required wallet token, a json_object object, and a template id."""
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=auth_token))
    request = IssueFromTemplateRequest(
        template_id=template_id,
        values_json=json.dumps(credential.json_object)
    )
    try:
        issue_response = await trinsic_wallet.credential.issue_from_template(request=request)
        return json.loads(issue_response.document_json)
    except Exception as e:
        error_message = f"Failed to verify proof: {str(e)}"
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post("/credential/proof/create", tags=[cred_tag])
async def create_proof(wallet_auth_token: str, attributes: JsonObject, reveal_template: list) -> dict:
    # API | Working
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    reveal_template = RevealTemplateAttributes(template_attributes=reveal_template)
    request = CreateProofRequest(document_json=json.dumps(attributes.json_object), reveal_template=reveal_template)
    try:
        trinsic_response = await trinsic_wallet.credential.create_proof(request=request)
        return {"response": json.loads(trinsic_response.proof_document_json)}
    except Exception as e:
        error_message = f"Failed to create proof: {str(e)}"
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post("/credential/proof/verify", tags=[cred_tag])
async def verify_proof(wallet_auth_token: str, proof: dict) -> dict:
    # Working
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    request = VerifyProofRequest(proof_document_json=json.dumps(proof))
    try:
        trinsic_response = await trinsic_wallet.credential.verify_proof(request=request)
        return {"results": trinsic_response.validation_results}
    except Exception as e:
        error_message = f"Failed to verify proof: {str(e)}"
        raise HTTPException(status_code=status_code, detail=error_message)


@router.get("/credential/revocation/check", tags=[cred_tag])
async def check_revocation(wallet_auth_token: str, cred_status_id: str) -> dict:
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    request = CheckStatusRequest(credential_status_id=cred_status_id)
    try:
        trinsic_response = await trinsic_wallet.credential.check_status(
            request=request)
        return {"revoked": trinsic_response.revoked}
    except Exception as e:
        error_message = f"Failed to retrieve revocation status: {str(e)}"
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post("/credential/revocation/update", tags=[cred_tag])
async def update_revocation_status(is_revoked: bool, wallet_auth_token: str, cred_status_id: str) -> dict:
    trinsic_wallet = TrinsicService(server_config=trinsic_config(auth_token=wallet_auth_token))
    request = UpdateStatusRequest(credential_status_id=cred_status_id, revoked=is_revoked)
    try:
        trinsic_response = await trinsic_wallet.credential.update_status(request=request)
        return trinsic_response.to_dict()
    except Exception as e:
        error_message = f"Failed to update revocation status: {str(e)}"
        raise HTTPException(status_code=status_code, detail=error_message)
