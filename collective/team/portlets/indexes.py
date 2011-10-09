from plone.indexer.decorator import indexer

from collective.team.behaviors.team import ITeam

@indexer(ITeam)
def getTeamMembers(obj):
    if getattr(obj, 'members'):
        return obj.members

@indexer(ITeam)
def getTeamManagers(obj):
    if getattr(obj, 'managers'):
        return obj.managers
