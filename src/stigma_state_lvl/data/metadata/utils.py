import frictionless as fl



def get_not_derived_fields(fields):
    filtered = []
    for field in fields:
        if isinstance(field,(fl.Field)):
            field = field.to_dict()
        if not field.get("derived") and not field.get("custom").get("derived"):
            filtered.append(field)
    
    return filtered