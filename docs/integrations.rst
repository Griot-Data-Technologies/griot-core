============
Integrations
============

Orchestrator integrations for Airflow, Prefect, and Dagster.

Airflow
-------

.. code-block:: python

   from griot_core.integrations.airflow import GriotValidateOperator

   validate_task = GriotValidateOperator(
       task_id="validate_users",
       contract_id="users-contract",
       profile="data_engineering",
       fail_on_invalid=True,
   )

Prefect
-------

.. code-block:: python

   from griot_core.integrations.prefect import griot_validate

   @flow
   def my_flow():
       result = griot_validate(
           contract_id="users-contract",
           profile="data_engineering",
       )

Dagster
-------

.. code-block:: python

   from griot_core.integrations.dagster import GriotResource

   @asset
   def users(griot: GriotResource):
       result = griot.validate("users-contract")
       ...

API Reference
-------------

.. automodule:: griot_core.integrations
   :members:
   :undoc-members:
