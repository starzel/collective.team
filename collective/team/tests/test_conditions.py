from mock import Mock
import unittest2 as unittest

class TestWithinIntranetCondition(unittest.TestCase):
    def test_condition_not_in_intranet(self):
        from collective.team.conditions import WithinTeamAreaAndNotManager
        view = WithinTeamAreaAndNotManager(None, None)
        view.request = Mock()
        view.request.ACTUAL_URL = 'no_intranet'
        self.assertFalse(view())

    def test_condition_not_manager(self):
        from collective.team.conditions import WithinTeamAreaAndNotManager
        view = WithinTeamAreaAndNotManager(None, None)
        view.request = Mock()
        view.request.ACTUAL_URL = 'wissen/intranet/special-interest-groups'
        view.request.PARENTS = [None]
        view._sec_manager = Mock()
        self.assertFalse(view())

    def test_condition_manager(self):
        from collective.team.conditions import WithinTeamAreaAndNotManager
        view = WithinTeamAreaAndNotManager(None, None)
        view.request = Mock()
        view.request.ACTUAL_URL = 'wissen/intranet/special-interest-groups'
        view.request.PARENTS = [None]
        view._sec_manager = Mock()
        view._sec_manager.checkPermission = lambda a, b: False
        self.assertTrue(view())
    
