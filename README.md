# Store Manager System - System Design Documentation

An integrated financial and inventory management ecosystem designed for high-integrity warehouse operations and real-time accounting. This system focuses on synchronizing supply chain logistics with financial reporting through event-driven data consistency.

---
<img width="1920" height="1032" alt="main" src="https://github.com/user-attachments/assets/599de778-d1f7-43ee-8292-7c565c09136e" />

## 1. Architectural Strategy & Design Philosophy

The system is built on a **Modular Integration Strategy**, where the core engine bridges the gap between physical inventory and financial ledgers. The primary design goal is to ensure that no financial transaction occurs without a corresponding inventory update, and vice-versa.

### A. Event-Driven Inventory Synchronization
Instead of manual stock adjustments, the system employs an automated event trigger strategy:
* **Procurement Influx:** Confirming a purchase invoice triggers an automated stock increment event.
* **Sales Deduction:** Successful invoice generation executes a real-time deduction from the warehouse database.
* **Integrity Checks:** Transactions are staged in a "Pending" state (e.g., a Shopping Basket) before being committed to the database, ensuring that stock levels are only altered upon valid financial confirmation.

### B. State-Based Financial Ledger Strategy
The system handles complex cash flow scenarios through a multi-state payment tracking logic:
* **Triple-State Invoicing:** Moving beyond binary (Paid/Unpaid) states, the system implements a **Fully Paid / Partially Paid / Unpaid** logic.
* **Relational Debt Mapping:** The system tracks "Creditor" and "Debtor" relationships. Each invoice is mapped to a specific entity ID (Customer or Supplier), allowing the system to aggregate "Total Remaining Debt" across multiple historical transactions.
* **Automatic Debt Deduction:** A strategy is implemented to allow lump-sum payments to be automatically distributed across existing unpaid invoices to clear oldest debts first.

### C. Analytical & Search Strategies
To ensure system performance and usability for large-scale data, specific retrieval strategies were implemented:
* **Multi-Attribute Smart Search:** A filtering algorithm that allows for concurrent queries (e.g., searching by product name and size dimensions simultaneously) to handle specialized inventory like tires or mechanical parts.
* **Temporal Profit Filtering:** A data-slicing strategy that allows the system to calculate "Net Profit" and "Average Profit" over dynamic date ranges, rather than just static monthly reports.

## 2. Core System Modules

### Inventory & Warehouse Engine
* **Capital Valuation Logic:** Calculates the total warehouse value based on the delta between "Purchase Price" and "Sales Price" across the entire stock.
* **Normalization:** Centralized storage of product attributes to ensure consistency across the Sales and Import modules.

### Procurement & Supply Chain (Importing)
* **Supplier Accounting:** A specialized ledger for managing supplier relationships, tracking total imports versus total payments made to vendors.
* **Import History Persistence:** Dedicated record-keeping for every stock influx for audit purposes.

### Sales & Billing System
* **Dynamic Client Profiling:** A strategy that distinguishes between "New" and "Existing" clients to determine whether to create a new credit ledger or update an existing one.
* **Invoice Rendering:** A document generation strategy that transforms relational database records into standardized PDF invoices for the end-user.

### Financial Analysis Dashboard
* **Profit Analysis:** Compares the cost of goods sold (COGS) against total revenue to provide real-time gross margin visibility.
* **Sales Volume Tracking:** Monitors the total number of transactions and units sold within specified intervals.

## 3. Technical Implementation Details
* **Data Persistence:** CRUD operations are strictly managed to ensure transaction atomicity.
* **Document Logic:** Integrated PDF generation for "Customer Statements" and "Invoices."
* **UI/UX Strategy:** A dashboard-centric interface designed to minimize the number of clicks required for common operations like "Smart Search" or "Quick Sale."

---
**Lead Designer/Developer:** Shady Mayez
