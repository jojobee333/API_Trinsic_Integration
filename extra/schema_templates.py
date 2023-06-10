from trinsic.proto.services.verifiablecredentials.templates.v1 import FieldOrdering, AppleWalletOptions, TemplateField, \
    FieldType, CreateCredentialTemplateRequest

fields = [("firstName", "First Name", "Given name of holder", FieldType.STRING, "Name"),
          ("lastName", "Last Name", "Given name of holder", FieldType.STRING, "Name")]
apple = ["firstName", ["lastName"], ["locationName"]]







ticketing_schema_template = CreateCredentialTemplateRequest(
    name=f"Ticketing Sample",
    title="Example Credential",
    description="A json_object for Trinsic's SDK samples",
    allow_additional_fields=True,
    fields={
        "firstName": TemplateField(title="First Name", description="Given name of holder"),
        "lastName": TemplateField(title="Last Name", description="Surname of holder", ),
        "ticketNumber": TemplateField(title="Ticket Number", description="Issued Ticket Number", type=FieldType.NUMBER),
        "credType": TemplateField(title="Type", description="The type of json_object", ),
        "eventName": TemplateField(title="Event Name", description="Name of Event", ),
        "locationName": TemplateField(title="Location Name", description="Name of location", ),
        "locationAddress": TemplateField(title="Location Address", description="Address of location", ),
        "addressRegion": TemplateField(title="Address Region", description="Address Region"),
        "addressPostalCode": TemplateField(title="Zip Code", description="Zip/Postal Code of Event Location",
                                           type=FieldType.NUMBER),
        "country": TemplateField(title="Country", description="Country of Event"),
        "eventDate": TemplateField(title="Event Date", description="Date of Event", type=FieldType.DATETIME)
    },
    field_ordering={
        "firstName": FieldOrdering(order=0, section="Name"),
        "lastName": FieldOrdering(order=1, section="Name"),
        "ticketNumber": FieldOrdering(order=2, section="Details"),
        "credType": FieldOrdering(order=3, section="Details"),
        "eventName": FieldOrdering(order=4, section="Event"),
        "locationName": FieldOrdering(order=5, section="Event"),
        "locationAddress": FieldOrdering(order=6, section="Event"),
        "addressRegion": FieldOrdering(order=7, section="Event"),
        "addressPostalCode": FieldOrdering(order=8, section="Event"),
        "country": FieldOrdering(order=9, section="Event"),
        "eventDate": FieldOrdering(order=10, section="Event"),

    },
    apple_wallet_options=AppleWalletOptions(primary_field="eventName", secondary_fields=["eventDate"], auxiliary_fields=["locationName"], ),
)
