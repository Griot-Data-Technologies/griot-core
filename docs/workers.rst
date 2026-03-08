=======
Workers
=======

Workers are execution units that receive validation jobs and run them
using the ValidationEngine. They're deployed to compute backends
(Lambda, K8s, Cloud Run).

.. note::

   Workers receive jobs from the :doc:`orchestration` module dispatchers.
   The orchestrator splits jobs by runtime type and dispatches to workers.

Overview
--------

.. code-block:: text

   ┌──────────────────┐
   │    Orchestrator  │
   │   (via registry) │
   └────────┬─────────┘
            │ dispatch
            ▼
   ┌──────────────────┐     callback     ┌──────────────┐
   │     Worker       │ ───────────────► │   Registry   │
   │  (Lambda/K8s/    │                  │ (store       │
   │   Cloud Run)     │                  │  results)    │
   └──────────────────┘                  └──────────────┘

WasmWorker
----------

Dedicated WASM-only worker for running inside containers.
Used by the orchestrator to avoid Docker-in-Docker.

.. code-block:: python

   from griot_core.workers import WasmWorker

   # Container entrypoint
   async def main():
       worker = WasmWorker()
       result = await worker.run()  # Reads spec from env vars

   # Or with explicit spec
   worker = WasmWorker()
   result = await worker.execute_wasm_checks(wasm_job_spec)

**Environment Variables:**

- ``GRIOT_JOB_SPEC``: JSON WasmJobSpec
- ``GRIOT_JOB_ID``: Job identifier
- ``GRIOT_CALLBACK_URL``: URL to POST results

LocalWorker
-----------

For development and testing.

.. code-block:: python

   from griot_core.workers import LocalWorker, run_local_validation

   # Quick validation
   result = await run_local_validation(
       contract=contract,
       data=arrow_data,
       profile="data_engineering",
   )

   # Or with worker
   worker = LocalWorker(config)
   result = await worker.execute(payload)

LambdaWorker
------------

AWS Lambda handler.

.. code-block:: python

   from griot_core.workers import lambda_handler

   # Lambda handler
   def handler(event, context):
       return lambda_handler(event, context)

**Deployment:**

.. code-block:: yaml

   # serverless.yml
   functions:
     griot-wasm-worker:
       handler: handler.handler
       timeout: 600
       memorySize: 1024
       environment:
         GRIOT_REGISTRY_URL: https://registry.example.com

KubernetesWorker
----------------

K8s Job execution.

.. code-block:: python

   from griot_core.workers import KubernetesWorker

   # Container entrypoint
   worker = KubernetesWorker(config)
   await worker.run()

**Environment Variables:**

- ``GRIOT_JOB_SPEC``: Job specification
- ``GRIOT_CALLBACK_URL``: Callback URL
- ``GRIOT_ARROW_DATA_PATH``: Path to mounted Arrow data

CloudRunWorker
--------------

Google Cloud Run HTTP handler.

.. code-block:: python

   from griot_core.workers import CloudRunWorker

   worker = CloudRunWorker(config)
   app = worker.create_flask_app()

   if __name__ == "__main__":
       app.run(host="0.0.0.0", port=8080)

Worker Types Comparison
-----------------------

+---------------+------------------+------------------+------------------+
| Feature       | Local            | Lambda           | K8s/Cloud Run    |
+===============+==================+==================+==================+
| Use case      | Development      | Serverless       | Production       |
+---------------+------------------+------------------+------------------+
| Scaling       | Single process   | Auto-scale       | Pod autoscaling  |
+---------------+------------------+------------------+------------------+
| Cold start    | None             | Can be slow      | Fast with pool   |
+---------------+------------------+------------------+------------------+
| Max runtime   | Unlimited        | 15 min           | Configurable     |
+---------------+------------------+------------------+------------------+
| Container     | Limited          | Lambda layers    | Full support     |
| checks        |                  |                  |                  |
+---------------+------------------+------------------+------------------+

API Reference
-------------

.. automodule:: griot_core.workers
   :members:
   :undoc-members:

.. automodule:: griot_core.workers.base
   :members:

.. automodule:: griot_core.workers.wasm_worker
   :members:

.. automodule:: griot_core.workers.local
   :members:

.. automodule:: griot_core.workers.lambda_worker
   :members:

.. automodule:: griot_core.workers.kubernetes
   :members:

.. automodule:: griot_core.workers.cloudrun
   :members:
