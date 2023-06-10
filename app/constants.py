import json
import os
import uvicorn
from fastapi import FastAPI
from trinsic.trinsic_service import TrinsicService
from trinsic.trinsic_util import trinsic_config
from typing import List, Dict
from trinsic.proto.services.verifiablecredentials.v1 import CheckStatusRequest, UpdateStatusRequest, IssueFromTemplateRequest, RevealTemplateAttributes, \
    CreateProofRequest, VerifyProofRequest
from fastapi import HTTPException
from pydantic import BaseModel
from trinsic.proto.services.verifiablecredentials.templates.v1 import FieldType, TemplateField, FieldOrdering, AppleWalletOptions, \
    CreateCredentialTemplateRequest, GetCredentialTemplateRequest, SearchCredentialTemplatesRequest
from fastapi import APIRouter
from trinsic.proto.services.universalwallet.v1 import IdentityProvider, AddExternalIdentityInitRequest, \
    AddExternalIdentityConfirmRequest, RemoveExternalIdentityRequest, CreateWalletRequest, SearchRequest, InsertItemRequest, \
    GetItemRequest, DeleteWalletRequest, AuthenticateInitRequest, AuthenticateConfirmRequest


from dotenv import load_dotenv

load_dotenv("../trins.env")
base_token = os.getenv("AUTH_TOKEN")
ecosystem_id = os.getenv("ECOSYSTEM_ID")
email = os.getenv("EMAIL")
wallet_tag = os.getenv("WALLET_TAG")
cred_tag = os.getenv("CREDENTIAL_TAG")
template_tag = os.getenv("TEMPLATE_TAG")
identity_tag = os.getenv("IDENTITY_TAG")
trust_registry_tag = os.getenv("TRUST_REGISTRY_TAG")
auth_tag = os.getenv("AUTH_TAG")
trinsic = TrinsicService(server_config=trinsic_config(auth_token=base_token))
status_code = 400
# print(base_token)