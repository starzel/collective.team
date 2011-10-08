import unittest2 as unittest
from mock import Mock
        
class TestStartPage(unittest.TestCase):
    def test_projects(self):
        from collective.team.browser import intranet
        context = Mock()
        folder_contents = [Mock()]
        folder_contents[0].absolute_url = lambda: 'path1'
        folder_contents[0].title = 'Title1'
        folder_contents[0].managers = 'a'
        folder_contents[0].members = 'a'
        folder_contents[0].portal_type = 'team'
        context.values = lambda: folder_contents
        view = intranet.StartPage(context, None)
        view.get_member_data = lambda x:{'username': 'a'}
        view.site = Mock()
        self.assertEquals([{'color': '',
                            'path': 'path1',
                            'results': [],
                            'admins': [{'username': 'a'}],
                            'members': [{'username': 'a'}],
                            'title': 'Title1'}],
                          [x for x in view.projects])

    def test_get_member_data(self):
        from collective.team.browser import intranet
        view = intranet.StartPage(None, None)
        view.site = Mock()
        member = Mock()
        view.site.acl_users.getUserById.return_value = member
        view.site.acl_users.getGroupById.return_value = None
        member.getProperty = lambda x:x
        member.getGroupName = lambda: "Groupname"
        self.assertEquals({'username': 'fullname',
                           'email': 'email',
                           'membertype' : 'user'},
                          view.get_member_data('userid'))
        self.assertEquals((('userid',), {}),
                          view.site.acl_users.getUserById.call_args) 
        view.site.acl_users.getUserById.return_value = None
        view.site.acl_users.getGroupById.return_value = member
        self.assertEquals({'username': 'Groupname',
                           'email': 'email',
                           'membertype' : 'group'},
                          view.get_member_data('userid'))
        self.assertEquals((('userid',), {}),
                          view.site.acl_users.getGroupById.call_args) 
        
