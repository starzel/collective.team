import unittest2 as unittest

class TestAddWizard(unittest.TestCase):
    def test_call_does_nothing(self):
        from collective.team.browser.intranet import AddWizard
        view = AddWizard()
        called = False
        def called_method(self):
            called = True
        view.index = called_method
        view()
