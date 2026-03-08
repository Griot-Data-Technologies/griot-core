=======
Privacy
=======

PII patterns and validators for privacy compliance.

PIIPattern
----------

.. code-block:: python

   from griot_core.privacy import PIIPattern
   from griot_core.models.enums import PIIType, ComplianceFramework

   pattern = PIIPattern(
       name="Kenya National ID",
       pii_type=PIIType.NATIONAL_ID,
       pattern=r"^\d{8}$",
       description="Kenya 8-digit national ID",
       confidence=0.95,
       validator=kenya_id_check,
       frameworks=[ComplianceFramework.KENYA_DPA],
       region="KE",
   )

Built-in Patterns
-----------------

**Kenya Patterns:**

- National ID
- KRA PIN
- Phone numbers
- M-PESA transaction codes

**EU Patterns:**

- IBAN
- VAT numbers
- German Personal ID

**Universal Patterns:**

- Email
- Credit card
- IPv4 address
- MAC address
- SSN
- Date of birth
- Passport number

Validators
----------

.. code-block:: python

   from griot_core.privacy.patterns import (
       luhn_check,
       iban_check,
       kenya_id_check,
       kra_pin_check,
   )

   # Credit card validation
   assert luhn_check("4111111111111111") == True

   # IBAN validation
   assert iban_check("DE89370400440532013000") == True

API Reference
-------------

.. automodule:: griot_core.privacy
   :members:
   :undoc-members:
