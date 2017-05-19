#include <exception>
#include <string.h>
#include "acPython.h"

static PyObject*
trieObj_abort(PyObject* exceptionType, const char * exceptionString) {
    // Raise exception with the description provided
    PyErr_SetString(exceptionType, exceptionString);
    return NULL;
}

static void
trieObj_dealloc(trieObj* self) {
    // Free internal string copies
    if (self->trie.numWords != 0)
    {
        for (defaultIndex i = 0; i < self->trie.numWords; ++i)
        {
            delete[] self->words[i];
        }
        delete[] self->words;
    }

    // Free dynamically allocated memory held by the trie
    indexArray().swap(self->trie.trie);
    indexArray().swap(self->trie.failureFunc);
    outputOfState().swap(self->trie.outputs);

    Py_TYPE(self)->tp_free((PyObject*) self);
}

static PyObject*
trieObj_new(PyTypeObject *type, PyObject* args, PyObject* kwds) {
    trieObj* self;

    defaultSize listSize = 0;

    PyObject* listObj;
    PyObject* strObj;
    char* strCharObj;

    // Make sure provided argument is a list object
    if(!PyArg_ParseTuple(args, "O!", &PyList_Type, &listObj))
    {
        return trieObj_abort(PyExc_ValueError,  "Argument is not a list");
    }

    listSize = (defaultSize) PyList_Size(listObj);

    // Make the list is not empty
    if(listSize < 1)
    {
        return trieObj_abort(PyExc_ValueError, "List must have at least 1 element");
    }

    // Attempt to allocate a wrapper type object
    self = (trieObj*) type->tp_alloc(type, 0);

    if (self != NULL) {
        // Create internal array of copies of the strings provided in the list
        if (!(self->words = new wordChars* [listSize]))
        {
            self->trie.numWords = 0;
            Py_DECREF(self);
            return trieObj_abort(PyExc_MemoryError, "Memory allocation failed");
        }

        // Copy strings provided in passed list into the internal array
        for (defaultIndex i = 0; i < listSize; ++i)
        {
            // Make sure that objects in list are strings and can be ASCII encoded
            if(!(strObj = PyUnicode_AsEncodedString(PyList_GetItem(listObj, i), "ascii", "strict")))
            {
                self->trie.numWords = i;
                Py_DECREF(self);
                return trieObj_abort(PyExc_ValueError, "String encoding to ascii failed");
            }

            // Cannot fail
            strCharObj = PyBytes_AsString(strObj);

            // Allocate space for copy of string
            if(!((self->words)[i] = new wordChars [PyBytes_Size(strObj) + 1]))
            {
                self->trie.numWords = i;
                Py_DECREF(self);
                return trieObj_abort(PyExc_MemoryError, "Memory allocation failed");
            }

            // Copy string
            memcpy(self->words[i], strCharObj, (PyBytes_Size(strObj) + 1) * sizeof(wordChars));
        }

        // Build trie structure from the copied array of words, catch any errors
        try
        {
            buildTrie(self->words, listSize, self->trie);
        }
        catch (std::exception& e)
        {
            self->trie.numWords = listSize;
            Py_DECREF(self);
            return trieObj_abort(PyExc_RuntimeError, e.what());
        }
    }
    else
    {
        return trieObj_abort(PyExc_RuntimeError, "Could not allocate new trie object");
    }

    return (PyObject*) self;
}

static int
trieObj_init(trieObj* self, PyObject* args, PyObject* kwds) {
    return 0;
}

static PyObject*
trieObj_query(trieObj* self, PyObject* args) {
    wordChars* targetString = NULL;
    int useIndexes = 0;

    // Make sure a string has been provided as the first argument
    if ( ! PyArg_ParseTuple(args, "sp", &targetString, &useIndexes)) {
        return trieObj_abort(PyExc_ValueError, "Argument is not a string");
    }

    matches foundSubStrings;

    // Find all substring matches and return the results, catch any errors
    try
    {
        foundSubStrings = searchString(targetString, self->trie);
    }
    catch (std::exception& e)
    {
        return trieObj_abort(PyExc_RuntimeError, e.what());
    }

    if (foundSubStrings.size() == 0)
    {
        Py_RETURN_NONE;
    }

    // Python list of results to return
    PyObject* results = PyList_New(0);

    if(!results)
    {
        return trieObj_abort(PyExc_MemoryError, "Memory allocation failed");
    }

    // Create a list of results, iterate backward to create a list ordered by lowest index of discovery
    for (matches::reverse_iterator iter = foundSubStrings.rbegin(); iter != foundSubStrings.rend(); ++iter)
    {
        if(useIndexes)
        {
            if(PyList_Append(results,
               PyTuple_Pack(2, PyLong_FromUnsignedLong((*iter).first),
                               PyLong_FromUnsignedLong((*iter).second))) == -1)
            {
                Py_DECREF(results);
                return trieObj_abort(PyExc_MemoryError, "Memory allocation failed");
            }
        }
        else
        {
            if(PyList_Append(results,
               PyTuple_Pack(2, PyUnicode_FromFormat("%s", self->words[(*iter).first]),
                               PyLong_FromUnsignedLong((*iter).second))) == -1)
            {
                Py_DECREF(results);
                return trieObj_abort(PyExc_MemoryError, "Memory allocation failed");
            }
        }
    }

    return results;
}

PyMODINIT_FUNC
PyInit_ahoCorasick(void)
{
    PyObject* m;

    // Make sure wrapper type is ready
    if (PyType_Ready(&trieObjType) < 0)
        return NULL;

    m = PyModule_Create(&ahocorasickmodule);

    if (m == NULL) {
        return NULL;
    }

    // Need to DECREF?
    Py_INCREF(&trieObjType);
    PyModule_AddObject(m, "trie", (PyObject *)&trieObjType);
    return m;
}
