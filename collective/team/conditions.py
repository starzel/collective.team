from collective.team.behaviors.team import ITeam

class WithinTeamArea(object):
    """ check if we are within a team """

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def __call__(self):
        for team in self.request.PARENTS:
            if ITeam.providedBy(team):
                return True

