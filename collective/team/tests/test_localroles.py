from mock import Mock
import unittest2 as unittest

class TestLocalRoles(unittest.TestCase):
    def testGetAllRoles(self):
        from collective.team.localroles import LocalRoles
        test_ob = LocalRoles(None)
        test_ob.context = Mock()
        test_ob.context.members = ['member1', 'member2']
        test_ob.context.managers = ['manager1', 'manager2']
        self.assertEquals([('member1', ('Editor', 'Contributor')),
                           ('member2', ('Editor', 'Contributor')),
                           ('manager1', ('Manager', 'Editor', 'Contributor')),
                           ('manager2', ('Manager', 'Editor', 'Contributor'))],
                          list(test_ob.getAllRoles()))

    def testGetRoles(self):
        from collective.team.localroles import LocalRoles
        test_ob = LocalRoles(None)
        test_ob.context = Mock()
        test_ob.context.members = ['member1']
        test_ob.context.managers = ['manager1']
        self.assertEquals(set(['Contributor', 'Editor']), set(test_ob.getRoles('member1')))
        self.assertEquals(set(['Manager', 'Editor', 'Contributor']),
                          set(test_ob.getRoles('manager1')))
