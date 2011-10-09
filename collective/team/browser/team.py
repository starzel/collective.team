from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from five import grok
from json import dumps
from DateTime.DateTime import DateTime
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.site.hooks import getSite

from collective.team.behaviors.team import ITeam

class View(grok.View):
    grok.context(ITeam)
    grok.require('zope2.View')

    def __call__(self, site = None):
        if site is None:
            site = getSite()
        self.site = site
        return super(View, self).__call__()

    def latest_docs(self):
        localize = self.site.translation_service.ulocalized_time
        all_portal_types = self.site.portal_catalog\
            .uniqueValuesFor('portal_type')
        all_portal_types = filter(lambda x: x not in ('Folder', 'team', 'Topic', 'Collection', 'Event'),
                                  all_portal_types)
        newest_docs = self.site.portal_catalog(
            path="/".join(self.context.getPhysicalPath()),
            sort_on='modified',
            portal_type=all_portal_types,
            sort_limit=5,
            sort_order='descending')[:5]
        return newest_docs

    def next_events(self):
        subject = ''
        if self.context.subject:
            subject = self.context.subject[0]
        next_events = self.site.portal_catalog(
            Subject = subject,
            sort_on='start',
            portal_type='Event',
            end={'query': DateTime(),
                 'range': 'min'},
            sort_limit=3,)[:3]
        return next_events


    def team_members(self):
            sort_by_fullname = lambda x: x['username']
            admins = filter(lambda x:x, map(self.get_member_data, self.context.managers))
            admins.sort(key=sort_by_fullname)
            members = filter(lambda x:x, map(self.get_member_data, self.context.members))
            members.sort(key=sort_by_fullname)
            team_members =  {'admins' : admins,
                                'members' : members,}
            return team_members

    def get_member_data(self, userid):
        member = self.site.acl_users.getUserById(userid)
        group = self.site.acl_users.getGroupById(userid)
        if member:
            username = member.getProperty("fullname") or member.getUserName()
            email = member.getProperty("email")
            membertype = 'user'
        if group:
            username = group.getGroupName()
            email = group.getProperty("email")
            membertype = 'group'
        if not group and not member:
            return member
        return dict(username=username, email=email, membertype=membertype)

