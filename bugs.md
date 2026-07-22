# Bug Log & Edge Cases

This file tracks discrepancies, validation issues, and API quirks discovered during the development of the automated test suite.

---

## [BUG-001] API Response Key Casing Discrepancy
* **Severity:** Medium (Breaks strict schema validation / contract testing)
* **Status:** Open

### Description
There is an inconsistency in key casing between the customer creation payload and the customer retrieval payload. The creation API expects camelCase, whereas the search/retrieval API returns lowercase.

* **Sent Payload (POST at /customers):** `firstName`
* **Received Payload (GET at /customers/search):** `firstname`

### Impact
Forces the API client or assertion library to use dynamic mapping (`field_name.lower()`) to match sent and received data, increasing client complexity and risking validation failures in strict deserializers (like Pydantic).

---

## [BUG-002] UI / Backend Validation Mismatch (Hyphens in Names)
* **Severity:** Low / UI-UX Polish
* **Status:** Open

### Description
The user registration UI helper text and error messages do not state that hyphens (`-`) are allowed in first and last names. However, the backend API fully permits and successfully saves names containing hyphens (e.g., `Jean-Luc`).

### Impact
Users with hyphenated names may self-censor and register with incorrect spellings of their names, assuming the platform blocks special characters due to incomplete UI hints.

---

## [BUG-003] Inconsistent Whitespace Sanitization (API vs. Admin Panel)
* **Severity:** Low / Data Integrity
* **Status:** Open

### Description
The Admin Panel back-office automatically strips leading and trailing whitespaces from customer names upon saving. However, the Customer API accepts, saves, and returns names with leading/trailing whitespaces completely unstripped (e.g., `" John "`).

### Impact
Leads to inconsistent data formatting in the database depending on the registration source. This can cause rendering issues on storefront documents (invoices, emails) and potential search discrepancies in downstream systems.