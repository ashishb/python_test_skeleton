#!/usr/bin/python
import argparse
import importlib
import inspect
import logging
import os
import sys
import traceback

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

# All classes performing the test must have this as the suffix.
# So, a test for class HelloWorld should be named, HelloWorldTest.
# In future, I will try to improve it to allow different format names to be
# provided.
_TEST_CLASS_SUFFIX = 'Test'
_TEST_METHOD_PREFIX = 'test_'

class Generator(object):

	@staticmethod
	def generateUnittestCode(filepath, indent, test_filepath=None):
		tested_methods = set()
		if test_filepath:
			tested_methods = Generator.getTestedMethods(test_filepath)
		indent = indent.replace('\\t', '\t')
		base_path = os.path.dirname(os.path.abspath(filepath))
		module_name = os.path.basename(filepath)
		error_message = ''
		output = 'import unittest\n\n'
		if module_name.endswith('.py'):
			module_name = module_name[:-3]
		elif module_name.endswith('.pyc'):
			module_name = module_name[:-4]
		try:
			sys.path.append(base_path)
			module = importlib.import_module(module_name)
			output += 'import %s\n\n' % module_name
		except ImportError as e:
			logger.error('Failed')
			logger.error('%s', traceback.format_exc())

		for (name, obj) in inspect.getmembers(module):
			if inspect.isclass(obj):
				# Only consider classes from this module, ignore the classes imported
				# from other modules.
				if not str(obj.__module__).endswith(module_name):
					continue
				logger.debug('Found class "%s".', name)
				output += 'class %s%s(unittest.TestCase):\n' % (
						name,	_TEST_CLASS_SUFFIX)
				output += '%sdef setUp(self):\n%s%spass \n\n' % (indent, indent,
						indent)
				for (func_name, func_obj) in inspect.getmembers(obj):
					if inspect.isfunction(func_obj) or inspect.ismethod(func_obj):
						logger.debug('Found function "%s".', func_name)
						test_name1 = '%s%s.%s%s' % (
								name, _TEST_CLASS_SUFFIX, _TEST_METHOD_PREFIX, func_name)
						test_name2 = test_name1.replace('__', '_')
						# Either format is acceptable.
						if (test_name1 not in tested_methods) and (
								test_name2 not in	tested_methods):
							if test_name1 != test_name2:
								error_message += 'Please add test %s or %s.\n' % (
										test_name1, test_name2)
							else:
								error_message += 'Please add test %s.\n' % (test_name1)
							output += ('%sdef %s%s(self):\n%s%spass'
									' # To be implemented.\n\n' %(indent, _TEST_METHOD_PREFIX,
											func_name, indent, indent))
			elif inspect.isfunction(obj):
				output += 'class GlobalMethod_%s%s(unittest.TestCase):\n' % (
						name, _TEST_CLASS_SUFFIX)
				output += '%sdef %s%s(self):\n%s%spass # To be implemented.\n\n' %(
						indent, _TEST_METHOD_PREFIX, name, indent, indent)

		output += 'if __name__ == \'__main__\':\n%sunittest.main()' % indent
		if error_message:
			print error_message
			print
		print output

	@staticmethod
	def getTestedMethods(test_filepath):
		tested_methods = set()
		base_path = os.path.dirname(os.path.abspath(test_filepath))
		module_name = os.path.basename(test_filepath)
		if module_name.endswith('.py'):
			module_name = module_name[:-3]
		elif module_name.endswith('.pyc'):
			module_name = module_name[:-4]
		try:
			sys.path.append(base_path)
			module = importlib.import_module(module_name)
		except ImportError as e:
			logger.error('Failed')
			logger.error('%s', traceback.format_exc())
		for (name, obj) in inspect.getmembers(module,
				predicate=inspect.isclass):
			if inspect.isclass(obj):
				logger.debug('Found class "%s".', name)
				if name.endswith(_TEST_CLASS_SUFFIX):
					for (func_name, func_obj) in inspect.getmembers(obj):
						if inspect.isfunction(func_obj) or inspect.ismethod(func_obj):
							if func_name.startswith(_TEST_METHOD_PREFIX):
								logger.debug('Found function "%s.%s".', name, func_name)
								tested_methods.add('%s.%s' % (name, func_name))
		return tested_methods


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filepath', dest='filepath',
			help='path of the python file')
	parser.add_argument('-t', '--test_filepath', dest='test_filepath',
			help='path og the test file(optional)')
	parser.add_argument('-i', '--indent', dest='indent',
			default='  ', help='indentation string (default: two whitespaces)')
	parser.add_argument('-v', '--verbose', dest='verbose',
			default=False, action='store_true', help='verbose output')

	args = parser.parse_args()
	if args.verbose:
		logger.setLevel(logging.DEBUG)
	Generator.generateUnittestCode(args.filepath, args.indent,
			test_filepath=args.test_filepath)


if __name__ == '__main__':
	main()
