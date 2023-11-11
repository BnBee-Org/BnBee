from webapp.models.organizations import Organization


class OrganizationService:

    def __init__(self, organization_repository: Organization) -> None:
        self._repository: Organization = organization_repository

    def create_organization(self, organization_name: str, logged_user_email: str, user_ip: str) -> Organization:
        return self._repository.add(name=organization_name, logged_user_email=logged_user_email, user_ip=user_ip)

    def delete_organization_by_id(self, organization_id: int, logged_user_email: str, user_ip: str) -> None:
        return self._repository.delete_by_id(organization_id=organization_id, logged_user_email=logged_user_email,
                                             user_ip=user_ip)
