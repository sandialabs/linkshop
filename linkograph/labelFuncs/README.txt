These packages provide the labeler functions that are available to the
functionalLabeling system. To make your own functions available, do the
following.

Suppose you have a package newPackage.py with functions newFunc1 and
newFunc2.

1. Add newPackage to the labelFuncs directory.

2. Add the string 'newPackage' to list of loaded packages in the
load_package_config file.

3. In your newPacakge.py package file, add the variable declaration
absClassLabelers = [('newFunc1Name', newFunc1),
                    ('newFunc2Name', newFunc2)]
The strings 'newFunc1Name' and 'newFunc2Name' are the function names
you supply to activate newFunc1 and newFunc2, respectively.

Notes on functions:

1. Every function must return a list of labels. If no labels were
determined then an empty list ([]) should be returned.
