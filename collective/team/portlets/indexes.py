from plone.indexer.decorator import indexer

from collective.team.behaviors.team import ITeam

@indexer(ITeam)
def getProjectMembers(obj):
    if getattr(obj, 'members'):
        return obj.members

@indexer(ITeam)
def getProjectManagers(obj):
    if getattr(obj, 'managers'):
        return obj.managers
