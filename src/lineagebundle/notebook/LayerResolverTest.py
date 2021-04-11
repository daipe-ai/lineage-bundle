import unittest
from lineagebundle.notebook.LayerResolver import LayerResolver


class LayerResolverTest(unittest.TestCase):
    def setUp(self):
        self.__layer_resolver = LayerResolver("^myproject/{layer}")

    def test_basic(self):
        layer = self.__layer_resolver.resolve("myproject/bronze/foo/bar.py")

        self.assertEqual("bronze", layer)

    def test_custom_placeholder(self):
        layer_resolver = LayerResolver("^myproject/([^/]+)")

        layer = layer_resolver.resolve("myproject/bronze/foo/bar.py")

        self.assertEqual("bronze", layer)


if __name__ == "__main__":
    unittest.main()
