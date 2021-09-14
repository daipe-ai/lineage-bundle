import os
import unittest
from pathlib import Path
from daipecore.lineage.InputDecorator import InputDecorator
from daipecore.lineage.argument.FunctionCallAttribute import FunctionCallAttribute
from daipecore.lineage.argument.FunctionLink import FunctionLink
from datalakebundle.notebook.lineage.TableWriter import TableWriter
from datalakebundle.notebook.lineage.argument.ReadTable import ReadTable
from datalakebundle.notebook.lineage.argument.TableParams import TableParams
from pyfonycore.bootstrap import bootstrapped_container
from lineagebundle.notebook.NotebookParser import NotebookParser
from lineagebundle.notebook.decorator.Function import Function


class NotebookParserTest(unittest.TestCase):

    __notebook_parser: NotebookParser

    def setUp(self):
        container = bootstrapped_container.init("test")

        self.__notebook_parser = container.get(NotebookParser)

    def test_read_table(self):
        directory = os.path.dirname(__file__)
        notebook_path = Path(os.path.join(directory, "NotebookParserTest_sample/read_table_sample.py"))
        functions = self.__notebook_parser.parse(notebook_path)

        self.assertEqual(1, len(functions))
        table_loader = functions[0]
        self.assertIsInstance(table_loader, Function)
        self.assertEqual("table_loader", table_loader.name)

        self.assertEqual(1, len(table_loader.decorators))
        transformation = table_loader.decorators[0]
        self.assertIsInstance(transformation, InputDecorator)

        self.assertEqual(1, len(transformation.args))
        read_table = transformation.args[0]
        self.assertIsInstance(read_table, ReadTable)
        self.assertEqual("sample_db.sample_table", read_table.full_table_name)

    def test_table_params(self):
        directory = os.path.dirname(__file__)
        notebook_path = Path(os.path.join(directory, "NotebookParserTest_sample/table_params_sample.py"))
        functions = self.__notebook_parser.parse(notebook_path)

        self.assertEqual(1, len(functions))
        load_sample_table = functions[0]
        self.assertIsInstance(load_sample_table, Function)
        self.assertEqual("load_sample_table", load_sample_table.name)

        self.assertEqual(1, len(load_sample_table.decorators))
        notebook_function = load_sample_table.decorators[0]
        self.assertIsInstance(notebook_function, InputDecorator)

        self.assertEqual(1, len(notebook_function.args))
        function_call_attribute = notebook_function.args[0]
        self.assertIsInstance(function_call_attribute, FunctionCallAttribute)
        self.assertIsInstance(function_call_attribute.function, TableParams)
        self.assertEqual("bronze_covid.tbl_template_2_confirmed_cases", function_call_attribute.function.table_name)
        self.assertEqual("base_date", function_call_attribute.attribute_name)

    def test_linked_function(self):
        directory = os.path.dirname(__file__)
        notebook_path = Path(os.path.join(directory, "NotebookParserTest_sample/linked_function_sample.py"))
        functions = self.__notebook_parser.parse(notebook_path)

        self.assertEqual(2, len(functions))

        add_timestamp = functions[1]
        self.assertIsInstance(add_timestamp, Function)
        self.assertEqual("add_timestamp", add_timestamp.name)

        self.assertEqual(1, len(add_timestamp.decorators))
        transformation = add_timestamp.decorators[0]
        self.assertIsInstance(transformation, InputDecorator)

        self.assertEqual(1, len(transformation.args))
        linked_function = transformation.args[0]
        self.assertIsInstance(linked_function, FunctionLink)
        self.assertEqual("load_sample_table", linked_function.linked_function)

    def test_table_writer(self):
        directory = os.path.dirname(__file__)
        notebook_path = Path(os.path.join(directory, "NotebookParserTest_sample/table_writer_sample.py"))
        functions = self.__notebook_parser.parse(notebook_path)

        self.assertEqual(1, len(functions))

        load_and_write = functions[0]
        self.assertIsInstance(load_and_write, Function)
        self.assertEqual("load_and_write", load_and_write.name)

        self.assertEqual(2, len(load_and_write.decorators))
        transformation = load_and_write.decorators[0]
        self.assertIsInstance(transformation, InputDecorator)
        table_writer = load_and_write.decorators[1]
        self.assertIsInstance(table_writer, TableWriter)
        self.assertEqual("overwrite", table_writer.mode)

        self.assertEqual("sample_db.sample_output_table2", table_writer.full_table_name)


if __name__ == "__main__":
    unittest.main()
