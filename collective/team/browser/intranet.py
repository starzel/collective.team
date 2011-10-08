from Products.Five.browser import BrowserView
from collections import defaultdict
from zope.site.hooks import getSite

class StartPage(BrowserView):
    """A view to show the intranet
    """
    def __call__(self, site = None):
        if site is None:
            site = getSite()
        self.site = site
        return super(StartPage, self).__call__()

    @property
    def projects(self):
        localize = self.site.translation_service.ulocalized_time
        for count, obj in enumerate(self.context.values()):
            if obj.portal_type != 'team':
                continue
            sort_by_fullname = lambda x: x['username']
            admins = filter(lambda x:x, map(self.get_member_data, obj.managers))
            admins.sort(key=sort_by_fullname)
            members = filter(lambda x:x, map(self.get_member_data, obj.members))
            members.sort(key=sort_by_fullname)
            mtool = self.site.portal_membership
            gtool = self.site.portal_groups
            is_member = False
            if not mtool.isAnonymousUser():
                member = mtool.getAuthenticatedMember()
                member_id = member.getId()
                member_ids = [group.id for group in gtool.getGroupsByUserId(member_id)] 
                member_ids.append(member_id)
                if set(member_ids).intersection((obj.members + obj.managers)):
                    is_member = True
            project =  {'title': obj.title,
                        'description' : obj.description,
                        'path' : obj.absolute_url(),
                        'color': obj.color,
                        'admins' : admins,
                        'members' : members,
                        'is_member' : is_member,
                        'results': []}
            yield project
            
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

        
