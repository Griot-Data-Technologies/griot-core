==========
Resolution
==========

Contract inheritance resolution and deep merge utilities.

ContractResolver
----------------

Resolves contract inheritance chains.

.. code-block:: python

   from griot_core.resolution import ContractResolver, InMemoryFetcher

   # Create resolver with fetcher
   fetcher = InMemoryFetcher()
   fetcher.register(parent_contract)

   resolver = ContractResolver(fetcher)

   # Resolve inheritance
   resolved = resolver.resolve(child_contract)

   # Access resolved definition
   print(resolved.resolved_definition)  # Merged result
   print(resolved.override_definition)  # Child's input
   print(resolved.inheritance_chain)    # Parent URIs

Deep Merge
----------

.. code-block:: python

   from griot_core.resolution import deep_merge

   parent = {"a": 1, "b": {"c": 2}}
   child = {"b": {"d": 3}}

   merged = deep_merge(parent, child)
   # {"a": 1, "b": {"c": 2, "d": 3}}

API Reference
-------------

.. automodule:: griot_core.resolution
   :members:
   :undoc-members:
