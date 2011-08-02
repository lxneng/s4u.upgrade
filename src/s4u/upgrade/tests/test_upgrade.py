import unittest


class upgrade_contexts_tests(unittest.TestCase):
    def tearDown(self):
        from s4u.upgrade.testing import reset_upgrade_data
        reset_upgrade_data()

    def test_return_function_untouched(self):
        from s4u.upgrade import upgrade_context

        def func():
            pass

        self.assertTrue(upgrade_context('name')(func) is func)

    def test_basic_registration(self):
        from s4u.upgrade import upgrade_context
        from s4u.upgrade import _context_providers

        @upgrade_context('me')
        def func():
            pass

        self.assertTrue('me' in _context_providers)
        self.assertTrue(_context_providers['me'][0] is func)
        self.assertEqual(_context_providers['me'][1], [])

    def test_parameters(self):
        from s4u.upgrade import upgrade_context
        from s4u.upgrade import _context_providers

        @upgrade_context('me', ['one'])
        def func():
            pass

        self.assertTrue('me' in _context_providers)
        self.assertTrue(_context_providers['me'][0] is func)
        self.assertEqual(_context_providers['me'][1], ['one'])


class upgrade_step_tests(unittest.TestCase):
    def tearDown(self):
        from s4u.upgrade.testing import reset_upgrade_data
        reset_upgrade_data()

    def test_return_function_untouched(self):
        from s4u.upgrade import upgrade_step

        def func():
            pass

        self.assertTrue(upgrade_step()(func) is func)

    def test_basic_registration(self):
        from s4u.upgrade import upgrade_step
        from s4u.upgrade import _upgrade_steps

        @upgrade_step()
        def func():
            pass

        self.assertEqual(len(_upgrade_steps), 1)
        self.assertTrue((func, []) in _upgrade_steps)

    def test_with_single_requirement(self):
        from s4u.upgrade import upgrade_step
        from s4u.upgrade import _upgrade_steps

        @upgrade_step('sql')
        def func():
            pass

        self.assertTrue((func, ['sql']) in _upgrade_steps)
        self.assertEqual(len(_upgrade_steps), 1)

    def test_with_requirements(self):
        from s4u.upgrade import upgrade_step
        from s4u.upgrade import _upgrade_steps

        @upgrade_step(['sql', 'zodb'])
        def func():  # pragma: no coverage
            pass

        self.assertTrue((func, ['sql', 'zodb']) in _upgrade_steps)
        self.assertEqual(len(_upgrade_steps), 1)


class scan_tests(unittest.TestCase):
    def setUp(self):
        import sys
        self._path = sys.path

    def tearDown(self):
        from s4u.upgrade.testing import reset_upgrade_data
        import sys
        reset_upgrade_data()
        sys.path = self._path

    def add_data_to_path(self):
        import os
        import sys
        my_directory = os.path.dirname(__file__)
        test_dir = os.path.join(my_directory, 'tst-pkg')
        sys.path.insert(0, test_dir)

    def scan(self, *a, **kw):
        from s4u.upgrade import scan
        return scan(*a, **kw)

    def test_unknown_module(self):
        from s4u.upgrade import _upgrade_steps
        from s4u.upgrade import _context_providers
        self.assertEqual(self.scan(['s4u.upgrade.unknown']), False)
        self.assertEqual(len(_upgrade_steps), 0)
        self.assertEqual(len(_context_providers), 0)

    def test_broken_module(self):
        from s4u.upgrade import _upgrade_steps
        from s4u.upgrade import _context_providers
        self.add_data_to_path()
        self.assertEqual(self.scan(['broken']), False)
        self.assertEqual(len(_upgrade_steps), 0)
        self.assertEqual(len(_context_providers), 0)

    def test_scan_context_provider(self):
        from s4u.upgrade import _context_providers
        self.add_data_to_path()
        self.assertEqual(self.scan(['context']), True)
        self.assertEqual(len(_context_providers), 1)

    def test_scan_upgrade_step(self):
        from s4u.upgrade import _upgrade_steps
        self.add_data_to_path()
        self.assertEqual(self.scan(['step']), True)
        self.assertEqual(len(_upgrade_steps), 1)


class run_context_provider_tests(unittest.TestCase):
    def run_context_provider(self, *a, **kw):
        from s4u.upgrade import run_context_provider
        return run_context_provider(*a, **kw)

    def test_no_parameters_and_no_arguments(self):
        marker = []

        def func():
            return marker

        result = self.run_context_provider(func, [])
        self.assertTrue(result is marker)

    def test_no_parameters_with_arguments(self):
        marker = []

        def func(options):
            self.assertEqual(options.__dict__, {})
            return marker

        result = self.run_context_provider(func, [])
        self.assertTrue(result is marker)

    def test_parameter_default(self):
        def func(options):
            self.assertEqual(options.foo, 'bar')

        self.run_context_provider(func, [('--foo', {'default': 'bar'})])

    def test_parameter_commandline_option(self):
        import sys

        argv = sys.argv
        sys.argv = ['upgrade', '--foo', 'bar']

        try:

            def func(options):
                self.assertEqual(options.foo, 'bar')

            self.run_context_provider(func, [('--foo', {})])
        finally:
            sys.argv = argv


class build_environment_tests(unittest.TestCase):
    def tearDown(self):
        from s4u.upgrade.testing import reset_upgrade_data
        reset_upgrade_data()

    def build_environment(self, *a, **kw):
        from s4u.upgrade import build_environment
        return build_environment(*a, **kw)

    def test_no_requirements(self):
        self.assertEqual(self.build_environment(None, []), {})

    def test_valid_requirement(self):
        from s4u.upgrade import _context_providers

        def func(options):
            return {'foo': 'bar'}

        _context_providers['foo'] = (func, [])
        self.assertEqual(
                self.build_environment({}, ['foo']),
                {'foo': 'bar'})

    def test_invalid_requirement(self):
        self.assertRaises(KeyError,
                self.build_environment, {}, ['foo'])

    def test_cache_environments(self):
        from s4u.upgrade import _context_providers

        def func(options):
            return {'foo': 'bar'}

        _context_providers['foo'] = (func, [])
        cache = {}
        self.build_environment(cache, ['foo'])
        self.assertEqual(cache.keys(), ['foo'])
        self.assertEqual(cache['foo'], {'foo': 'bar'})

    def test_use_cached_environments(self):
        cache = {'one': {'one': []}, 'two': {'two': []}}
        environment = self.build_environment(cache, ['one', 'two'])
        self.assertTrue(environment['one'] is cache['one']['one'])
        self.assertTrue(environment['two'] is cache['two']['two'])
