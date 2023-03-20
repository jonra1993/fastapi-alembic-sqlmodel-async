allow(actor, action, resource) if
  has_permission(actor, action, resource);

actor User {}

resource Repository {
  permissions = ["read", "push", "delete"];
  roles = ["contributor", "maintainer", "admin"];

  "read" if "contributor";
  "push" if "maintainer";
  "delete" if "admin";

  "maintainer" if "admin";
  "contributor" if "maintainer";
}

# This rule tells Oso how to fetch roles for a repository
has_role(actor: User, role_name: String, repository: Repository) if
  role in actor.roles and
  role_name = role.name and
  repository = role.repository;