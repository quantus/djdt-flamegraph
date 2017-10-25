
===============================
Flask Debugtoobar Flame Graph
===============================

Based on the awesome [djdt-flamegraph](https://github.com/23andMe/djdt-flamegraph) project.

Get a flame graph of the current request.

.. image:: https://travis-ci.org/23andMe/djdt-flamegraph.svg?branch=master
        :target: https://travis-ci.org/23andMe/djdt-flamegraph

.. image:: https://img.shields.io/pypi/v/djdt_flamegraph.svg
        :target: https://pypi.python.org/pypi/djdt_flamegraph

Screenshot
----------

.. image:: https://raw.githubusercontent.com/23andMe/djdt-flamegraph/master/flamegraph-screenshot.png

Features
--------

* Uses https://github.com/brendangregg/FlameGraph to generate a flamegraph right in the debug panel.

Install
-------
* Add ``flask_debugtoolbar_flamegraph`` to your ``requirements.txt``.
* Add ``flask_debugtoolbar_flamegraph.FlamegraphPanel`` to ``DEBUG_TB_PANELS``.
* Run your server with ``python manage.py runserver --nothreading --noreload``

Notes
-----
* ``ValueError at /: signal only works in main thread``: Flame graphs can only be generated in a single threaded server.
* Flame graphs are disabled by default. You'll have to enable it by clicking the checkbox next to it in the Debug Toolbar.
* Probably won't work on Windows.
