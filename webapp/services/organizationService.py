from webapp.models.organizations import Organization


class OrganizationService:

    def __init__(self, organization_repository: Organization) -> None:
        self._repository: Organization = organization_repository

    def create_organization(self, organization_name: str) -> Organization:
        return self._repository.add(name=organization_name)

    def delete_organization_by_id(self, organization_id: int) -> None:
        return self._repository.delete_by_id(organization_id)
