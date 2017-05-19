#ifndef ACPYTHON_H
#define ACPYTHON_H

#include <Python.h>
#include "structmember.h"
#include "ahoCorasick.h"

// -----------------------------------------------------------------------------
/**
    An extension of python wrapping a C++ implementation of the Aho-Corasick algorithm.
    Extension is written strictly for Python 3 and does not include support for
    Python 2 or non-ASCII strings.
*/
// -----------------------------------------------------------------------------

// Trie wrapper object, note: simply storage from the python point of view
typedef struct {
    PyObject_HEAD
    wordChars** words;
    trieData   trie;
} trieObj;

// Convenience function to raise proper exceptions and exit gracefully if an error occurs
static PyObject* trieObj_abort(PyObject* exceptionType, const char * exceptionString);

// Destructor for the wrapper object, frees dynamically allocated memory of trie
static void trieObj_dealloc(trieObj* self);

// Constructor for the wrapper object, allocates memory and builds the trie
// Words may not be added to the trie once it has been constructed
static PyObject* trieObj_new(PyTypeObject *type, PyObject* args, PyObject* kwds);

// Required initialization function for the wrapper, does nothing
static int trieObj_init(trieObj* self, PyObject* args, PyObject* kwds);

// Search a string for the substrings that were used to populate the trie
static PyObject* trieObj_query(trieObj* self, PyObject* args);

// Assign the method to perform the substring search to the wrapper object
static PyMethodDef trieMethods[] = {
    {"query", (PyCFunction) trieObj_query, METH_VARARGS,
        "Search string for keywords."},
    {NULL, NULL, 0, NULL}     /* Sentinel */
};

// Wrapper object has no members that are directly accessable from python
static PyMemberDef trieMembers[] = {
    {NULL, NULL, 0, NULL}  /* Sentinel */
};

// Define wrapper object as a fundamental python type
static PyTypeObject trieObjType = {
    PyObject_HEAD_INIT(NULL)
    "ahoCorasick.trie",                        /* tp_name*/
    sizeof(trieObj),                           /* tp_basicsize*/
    0,                                         /* tp_itemsize*/
    (destructor) trieObj_dealloc,              /* tp_dealloc*/
    0,                                         /* tp_print*/
    0,                                         /* tp_getattr*/
    0,                                         /* tp_setattr*/
    0,                                         /* tp_reserved*/
    0,                                         /* tp_repr*/
    0,                                         /* tp_as_number*/
    0,                                         /* tp_as_sequence*/
    0,                                         /* tp_as_mapping*/
    0,                                         /* tp_hash */
    0,                                         /* tp_call*/
    0,                                         /* tp_str*/
    0,                                         /* tp_getattro*/
    0,                                         /* tp_setattro*/
    0,                                         /* tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,  /* tp_flags*/
    "trie() -> new efficient string matching", /* tp_doc */
    0,                                         /* tp_traverse */
    0,                                         /* tp_clear */
    0,                                         /* tp_richcompare */
    0,                                         /* tp_weaklistoffset */
    0,                                         /* tp_iter */
    0,                                         /* tp_iternext */
    trieMethods,                               /* tp_methods */
    trieMembers,                               /* tp_members */
    0,                                         /* tp_getset */
    0,                                         /* tp_base */
    0,                                         /* tp_dict */
    0,                                         /* tp_descr_get */
    0,                                         /* tp_descr_set */
    0,                                         /* tp_dictoffset */
    (initproc) trieObj_init,                   /* tp_init */
    0,                                         /* tp_alloc */
    trieObj_new,                               /* tp_new */
    0,                                         /* tp_free */
    0,                                         /* tp_is_gc */
    0,                                         /* tp_bases */
    0,                                         /* tp_mro */
    0,                                         /* tp_cache */
    0,                                         /* tp_subclasses */
    0,                                         /* tp_weaklist */
    0,                                         /* tp_del */
    0,                                         /* tp_version_tag */
    0                                          /* tp_finalize */
};

// Module defines no methods, only the wrapper object type
static PyMethodDef AhoCorasickMethods[] = {
    {NULL, NULL, 0, NULL} /* Sentinel */
};

// Define the module
static struct PyModuleDef ahocorasickmodule = {
    PyModuleDef_HEAD_INIT,
    "ahocorasick",
    NULL,
    -1,
    AhoCorasickMethods
};


#endif // ACPYTHON_H
