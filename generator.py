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

class Generator(object):

	@staticmethod
	def generateUnittestCode(filepath, indent):
		indent = indent.replace('\\t', '\t')
		base_path = os.path.dirname(os.path.abspath(filepath))
		module_name = os.path.basename(filepath)
		output = 'import unittest\n\n'
		if module_name.endswith('.py'):
			module_name = module_name[:-3]
		try:
			sys.path.append(base_path)
			module = importlib.import_module(module_name)
			output += 'import %s\n\n' % module_name
		except ImportError as e:
			logger.error('Failed')
			logger.error('%s', traceback.format_exc())

		for (class_name, class_obj) in inspect.getmembers(module):
			if inspect.isclass(class_obj):
				logger.debug('Found class "%s".', class_name)
				output += 'class %sTest(unittest.TestCase):\n' % class_name
				output += '%sdef setUp(self):\n%s%spass \n\n' % (indent, indent,
						indent)
				for (func_name, func_obj) in inspect.getmembers(class_obj):
					if inspect.isfunction(func_obj) or inspect.ismethod(func_obj):
						logger.debug('Found function "%s".', func_name)
						output += ('%sdef test_%s(self):\n%s%spass'
								' # To be implemented.\n\n' %(indent, func_name,
										indent, indent))
			elif inspect.isfunction(class_obj):
				output += 'class GlobalMethod_%sTest(unittest.TestCase):\n' % (
						class_name)
				output += '%sdef test_%s(self):\n%s%spass # To be implemented.\n\n' %(
						indent, class_name, indent, indent)

		output += 'if __name__ == \'__main__\':\n%sunittest.main()' % indent
		print output



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filepath', dest='filepath',
			help='path of the python file')
	parser.add_argument('-i', '--indent', dest='indent',
			default='  ', help='indentation string (default: two whitespaces)')
	args = parser.parse_args()
	Generator.generateUnittestCode(args.filepath, args.indent)


if __name__ == '__main__':
	main()
