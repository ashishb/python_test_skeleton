Python Test Skeleton Generator
====================

Python unittest skeleton generator.
```
usage: generator.py [-h] [-f FILEPATH] [-t TEST_FILEPATH] [-i INDENT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filepath FILEPATH
                        path of the python file
  -t TEST_FILEPATH, --test_filepath TEST_FILEPATH
                        path of the test file(optional)
  -i INDENT, --indent INDENT
                        indentation string (default: two whitespaces)
  -v, --verbose         verbose output
```

If hello_world.py contains 
```
class HelloWorld(object):

	def hello(self):
		print 'Hello'


def main():
	hw = HelloWorld()
	hw.hello()

if __name__ == '__main__':
	main()
```

then
```
python generator.py -f hello_world.py -i '\t' > hello_world_test_tab.py
```

will generate
```
import unittest

import hello_world

class HelloWorldTest(unittest.TestCase):
	def setUp(self):
		pass 

	def test_hello(self):
		pass # To be implemented.

class GlobalMethod_mainTest(unittest.TestCase):
	def test_main(self):
		pass # To be implemented.

if __name__ == '__main__':
	unittest.main()
```


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/ashishb/python_test_skeleton/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

