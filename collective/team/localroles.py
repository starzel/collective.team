from zope.interface import implements
from zope.component import adapts

from borg.localrole.interfaces import ILocalRoleProvider
from collective.team.behaviors.team import ITeam

class LocalRoles(object):
    """Provide a local role manager for projects
    """
    implements(ILocalRoleProvider)
    adapts(ITeam)

    def __init__(self, context):
        self.context = context

    def getAllRoles(self):
        for m in self.context.members:
            yield(m, ('Editor','Contributor'))
        for m in self.context.managers:
            yield(m, ('Manager','Editor', 'Contributor'))

    def getRoles(self, principal_id):
        roles = set()
        if principal_id in (self.context.members or []):
            roles.add('Editor')
            roles.add('Contributor')
        if principal_id in (self.context.managers or []):
            roles.add('Editor')
            roles.add("Manager")
            roles.add('Contributor')
        return roles
