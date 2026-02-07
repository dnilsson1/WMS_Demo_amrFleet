Here is the master specification designed for an Agentic Coding Assistant (like GitHub Copilot Workspace, Devin, or Cursor). You can copy-paste this directly into the agent's prompt window.

---

# Project Specification: Warehouse Middleware "Production-Readiness" Upgrade

**Role:** Senior Full-Stack Developer / Systems Architect
**Objective:** Upgrade the existing "WMS Demo" PoC into a functional Warehouse Control System (WCS) capable of reliable daily operations.
**Tech Stack Constraints:**

* **Backend:** Python 3.11, FastAPI, SQLModel (SQLite), SQLAlchemy.
* **Frontend:** SvelteKit (Node adapter), Skeleton UI, Tailwind CSS.
* **Protocol:** HTTP/JSON for internal APIs; VDA 5050 / Custom REST for KUKA Fleet integration.

---

## Prioritized Development Backlog (1-10)

### Phase 1: Closing the Operational Loop (High Priority)

#### Task 1: [x] Implement Inbound "Goods Receipt" Workflow

**Context:** Currently, stock is added via raw API calls without validation. We need a UI for operators to physically receive goods.

* **Backend (`main.py`, `schemas.py`):**
* Create endpoint `POST /receiving/scan`.
* Input: `product_sku` (string), `quantity` (int), `container_code` (string).
* Logic: Verify `container_code` exists. If `product_sku` is new, prompt for creation or reject based on config. Update `Product.current_stock` and create an `InventoryMovement` record with `type="inbound"`.


* **Frontend (`/routes/receiving/+page.svelte`):**
* Create a new page "Inbound".
* Form fields: Product SKU (auto-focus), Quantity, Target Container.
* Visual feedback: Green flash on success, Red modal on error.


* **Acceptance Criteria:** A user can scan a barcode and immediately see the stock count increase in the `/products` view.

#### Task 2: [x] Mission Lifecycle Background Worker

**Context:** `submit_mission` is currently fire-and-forget. We have no visibility if the robot fails.

* **Backend (`services/mission_monitor.py`):**
* Implement a background loop (using `asyncio` or `FastAPI.on_event("startup")`) that runs every 5 seconds.
* Logic: Query KUKA Fleet `GET /mission/status` for all active orders.
* Update local `Order.status` in `models.py` based on response: `EXECUTING` → `COMPLETED` or `FAILED`.


* **Frontend (`/routes/orders/+page.svelte`):**
* Update the Order list to show live status badges (e.g., "Robot Moving" vs "Done") instead of just static "Picking".


* **Acceptance Criteria:** If I manually cancel a mission in the KUKA interface, the Local Dashboard updates the order to "Failed" within 10 seconds.

#### Task 3: [x] Soft Allocation Logic (Inventory Reservation)

**Context:** Stock is deducted immediately upon order creation. If a mission fails, stock is lost data-wise.

* **Backend (`models.py`, `main.py`):**
* Modify `Product` model: Add `allocated_stock` (int).
* Refactor `create_order`: Increment `allocated_stock` instead of decrementing `current_stock`.
* Refactor `complete_order`: Decrement `current_stock` and decrement `allocated_stock`.
* Refactor `cancel_order`: Decrement `allocated_stock`.


* **Acceptance Criteria:** Creating an order for 5 items (Total 10) shows: "Available: 5, Allocated: 5, Total: 10".

---

### Phase 2: Safety & Reliability

#### Task 4: [x] Basic User Authentication

**Context:** The system is currently open to any network user.

* **Backend (`auth.py`, `main.py`):**
* Add `User` model (username, password_hash, role).
* Implement `OAuth2PasswordBearer` (FastAPI) for token generation.
* Protect `/settings`, `/orders/create`, and `/receiving` endpoints.


* **Frontend (`hooks.server.js`):**
* Implement a protected route guard. Redirect unauthenticated users to a new `/login` page.


* **Acceptance Criteria:** A user in an Incognito window cannot trigger a robot mission without logging in.

#### Task 5: [x] Exception Handling & Manual Cancellation

**Context:** Operators need a "Stop" button when things go wrong.

* **Backend (`main.py`):**
* Create endpoint `POST /orders/{id}/cancel`.
* Logic:
1. Check Order status.
2. Send `cancelMission` command to KUKA API.
3. Revert `allocated_stock`.
4. Mark Order as `CANCELLED`.




* **Frontend:**
* Add a red "Cancel" button to active orders in the Order List.


* **Acceptance Criteria:** Pressing cancel stops the robot and returns the inventory numbers to their previous state.

#### Task 6: [x] FIFO (First-In-First-Out) Picking Strategy

**Context:** Current logic blindly picks the first container found.

* **Backend (`main.py` - `find_containers_with_product`):**
* Update the SQL query to join `InventoryMovement` or track `last_updated` on `Container` contents.
* Sort results by `entry_date ASC`.


* **Acceptance Criteria:** If "Milk" is in Container A (added yesterday) and Container B (added today), the system MUST generate a mission for Container A first.

---

### Phase 3: Efficiency & Usability

#### Task 7: [x] Barcode Scanner Focus Handling

**Context:** Handheld scanners act as keyboards. The UI must capture input efficiently.

* **Frontend (`actions/scanner.js`):**
* Create a Svelte action to listen for global `keydown`.
* Detect rapid input ending in `Enter` (simulating a scanner).
* Auto-populate the active input field or trigger the "Submit" button.


* **Acceptance Criteria:** Scanning a barcode while not focused on the input box still populates the correct field.

#### Task 8: [x] Container Capacity Constraints

**Context:** Prevent overflowing bins.

* **Backend (`models.py`):**
* Add `max_capacity` (int) to `ContainerType`.


* **Backend (`main.py`):**
* In `receiving/scan`, check: `Current_Qty + New_Qty <= Max_Capacity`.
* Return HTTP 400 "Container Full" if exceeded.


* **Acceptance Criteria:** Trying to add the 11th item to a 10-item bin returns a specific error message.

#### Task 9: [x] Label Printing Integration

**Context:** Operators need physical labels for tracking.

* **Backend (`services/label_printer.py`):**
* Create a utility to generate a ZPL string (Zebra Programming Language) or a simple PDF.
* Endpoint `GET /products/{id}/label`.


* **Frontend:**
* Add "Print Label" button to the Receiving success modal.


* **Acceptance Criteria:** Clicking print opens a new tab with a generated PDF barcode of the SKU.

#### Task 10: [x] Operational Analytics Dashboard

**Context:** Visualizing throughput.

* **Backend (`routes/analytics.py`):**
* Endpoint `GET /analytics/throughput`.
* Logic: Aggregate `InventoryMovement` count grouped by hour for the last 24h.


* **Frontend (`/routes/+page.svelte`):**
* Replace the static "Welcome" text with a chart (e.g., using `chart.js` or `layerchart`) showing "Movements per Hour".


* **Acceptance Criteria:** The homepage displays a graph that updates when new orders are completed.