import unittest

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('test')
    unittest.TextTestRunner(verbosity=2).run(suite)
