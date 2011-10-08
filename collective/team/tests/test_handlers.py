from mock import Mock
import unittest2 as unittest
from collections import defaultdict

class TestHelpers(unittest.TestCase):
    def test_get_role_permission_for_fti(self):
        from collective.team.handlers import _get_role_permission_for_fti
        context = Mock()
        context.manage_addProduct = defaultdict(Mock())
        fti = Mock()
        fti.factory = "factory1"
        Mock.factory1__roles__ = "roles1"
        self.assertFalse(None == _get_role_permission_for_fti(context, fti))

    def test_get_role_permissions_for_fti_returning_none(self):
        from collective.team.handlers import _get_role_permission_for_fti
        context = Mock()
        product_instance = Mock()
        factory_method = Mock()
        product_instance.factory1 = factory_method
        context.manage_addProduct = defaultdict(lambda: product_instance)
        fti = Mock()
        fti.factory = "factory1"
        Mock.factory1__roles__ = None
        self.assertTrue(None == _get_role_permission_for_fti(context, fti))
        factory_method.im_self = None
        self.assertTrue(None == _get_role_permission_for_fti(context, fti))
        product_instance.factory1 = None
        self.assertTrue(None == _get_role_permission_for_fti(context, fti))
        context.manage_addProduct = defaultdict(lambda: None.attribute_error)
        self.assertTrue(None == _get_role_permission_for_fti(context, fti))
        fti.factory = None
        self.assertTrue(None == _get_role_permission_for_fti(context, fti))

    def test_get_factory_permission(self):
        from collective.team.handlers import get_factory_permission
        context = Mock()
        context.manage_addProduct = defaultdict(Mock())
        fti = Mock()
        fti.factory = "factory1"
        Mock.factory1__roles__ = Mock()
        Mock.factory1__roles__.__name__ = 'permission'
        self.assertNotEquals(None, get_factory_permission(context, fti))

    def test_get_factory_permission_returns_none(self):
        from collective.team.handlers import get_factory_permission
        context = Mock()
        context.manage_addProduct = defaultdict(Mock())
        fti = Mock()
        fti.factory = None
        Mock.factory1__roles__ = Mock()
        Mock.factory1__roles__.__name__ = None
        self.assertEquals(None, get_factory_permission(context, fti))

    def test_update_indexed_security(self):
        from collective.team.handlers import updateIndexedSecurity
        team = Mock()
        updateIndexedSecurity(team, None)
        self.assertEquals([('reindexObjectSecurity', (), {'skip_self': True})],
                          team.method_calls)

    def test_enable_addable_types(self):
        from collective.team import handlers
        original_get_factory_permission = handlers.get_factory_permission
        try:
            handlers.get_factory_permission = lambda a, b: ['view_permission']
            project = Mock()
            project.portal_types = Mock()
            project.permission_settings = lambda x: [{'acquire' : True}]
            project.rolesOfPermission = lambda x:[{'name' : 'Manager', 'selected' : True}]
            type_info = [Mock()]
            project.portal_types.listTypeInfo = lambda: type_info
            event = Mock()
            handlers.enable_addable_types(project, event)
            self.assertEquals([('manage_permission', (['view_permission'],
                                                      ['Manager',
                                                       'Editor',
                                                       'Reviewer'], True), {})],
                              project.method_calls)
        finally:
            handlers.get_factory_permission = original_get_factory_permission

    def test_add_default_folders(self):
        from collective.team.handlers import add_default_folders
        class Folder(dict):
            def invokeFactory(self, id, type_name):
                return id
        project = Folder()
        project['bilder'] = Mock()
        project['dokumente'] = Mock()
        project['termine'] = Mock()
        add_default_folders(project, None)
        self.assertEquals([('reindexObject', (), {})],
                          project['bilder'].method_calls)
        self.assertEquals([('reindexObject', (), {})],
                          project['dokumente'].method_calls)
        self.assertEquals([('reindexObject', (), {})],
                          project['termine'].method_calls)
            
