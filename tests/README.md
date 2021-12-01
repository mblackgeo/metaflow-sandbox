# Testing Meta"flows"

It appears that there is not an easy way to run an isolated step from a flow for unit testing. For example, the [testing philosophy page](https://docs.metaflow.org/internals-of-metaflow/testing-philosophy) of the Metaflow docs actually only explains how Metaflow itself is tested, not how to implement tests for your own custom flows. Metaflows has no module level API, and is only accessible from the command line. In fact, Neflix went as far as to say[^1] the strategies for unit testing your flows should be as follows:

* You can separate out business logic from steps in separate Python modules, which you can test with any (unit) testing package for Python.
* You can do integration testing for the whole flow by running the flow (e.g. as a part of a CI/CD pipeline like Jenkins) and then checking that the results are expected by inspecting its artifacts using the Client API (or dump in CLI).

It appears that the better option is to use point 2 and that approach is what is implemented in this small example.

[^1]: https://github.com/Netflix/metaflow/issues/140