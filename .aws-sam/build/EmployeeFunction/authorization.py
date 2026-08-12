def get_user_claims(event):

    try:
        return (
            event
            .get("requestContext", {})
            .get("authorizer", {})
            .get("jwt", {})
            .get("claims", {})
        )

    except Exception:
        return {}



def get_user_role(event):

    claims = get_user_claims(event)

    return claims.get(
        "custom:role"
    )



def is_admin(event):

    role = get_user_role(event)

    return role == "admin"