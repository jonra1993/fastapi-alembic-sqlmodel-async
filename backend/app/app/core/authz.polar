actor User {}

# This is the resource
resource Hero {
    permissions = ["read", "create", "push", "update", "delete"];
    roles = ["user", "manager", "admin"];

    # A user has the "read" permission if they have the
    # "user" role.
    "read" if "user";

    # A user has the "create" permission if they have the
    # "manager" role.
    "push" if "manager";

    # A user has the "create" permission if they have the
    # "manager" role.
    "create" if "manager";

    # A user has the "update" permission if they have the
    # "manager" role.
    "update" if "manager";

    # A user has the "delete" permission if they have the
    # "manager" role.
    "delete" if "admin";

    # A user has the "user" role if they have
    # the "manager" role.
    "user" if "manager";

    # A user has the "manager" role if they have
    # the "admin" role.
    "manager" if "admin";
}


# This rule tells Oso how to fetch data
has_permission(user: User, "read", heroe: Hero) if
    user.id = heroe.created_by_id;

allow(actor, action, resource) if
    has_permission(actor, action, resource);