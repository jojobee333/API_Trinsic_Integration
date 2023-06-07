from app.models.constants import *
from app.models.models import TemplateInfo

router = APIRouter()


@router.get('/template/search', tags=[template_tag])
async def search_for_template() -> dict:
    """This function will return all templates from base wallet. Needs query specification added at the moment."""
    # API working |
    request = SearchCredentialTemplatesRequest(query=f"SELECT * FROM c")
    try:
        response = await trinsic.template.search(request=request)
        return {"response": json.loads(response.items_json)}
    except Exception as e:
        error_message = "Failed to find template: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.get('/template/get', tags=[template_tag])
async def get_template(template_id) -> dict:
    """Gets template based on template id."""
    # API Working |
    request = GetCredentialTemplateRequest(id=template_id)
    try:
        response = await trinsic.template.get(request=request)
        empty_json = {field: None for field in response.template.fields}
        return {response.template.id: response.template.fields,
                "empty_template": empty_json}
    except Exception as e:
        error_message = "Failed to access template: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)


@router.post('/template/create', tags=[template_tag])
def create_credential_template(template_info: TemplateInfo, allow_additional_fields: bool = False) -> dict:
    """Create a New Template for Credentials."""
    # Prepare the fields
    try:
        fields = {field.name: TemplateField(title=field.title, description=field.description, type=FieldType.STRING) for
                  field in template_info.fields}
        field_ordering = {field.name: FieldOrdering(section=field.section, order=count) for count, field in
                          enumerate(template_info.fields)}
        apple_options = AppleWalletOptions(primary_field=template_info.primary_field,
                                           secondary_fields=template_info.secondary_fields,
                                           auxiliary_fields=template_info.auxiliary_fields)
        request = CreateCredentialTemplateRequest(
            name=template_info.name,
            title=template_info.title,
            description=template_info.description,
            fields=fields,
            field_ordering=field_ordering,
            apple_wallet_options=apple_options,
            allow_additional_fields=allow_additional_fields
        )
        trinsic_response = trinsic.template.create(request=request)
        print(trinsic_response.data)
        return trinsic_response.data
    except Exception as e:
        error_message = "Failed to create template: " + str(e)
        raise HTTPException(status_code=status_code, detail=error_message)

