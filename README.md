# Scalable Agentic System Design

### **Author:** Sindhuja S

### **Version:** 1.0

---

## Overview

This project demonstrates the design of a **Scalable Agentic System** capable of handling a large number of tools efficiently.
It uses **LangGraph** for flow orchestration and **ChromaDB** for context-aware retrieval (RAG).
The system intelligently routes user queries to the appropriate tools through a modular, multi-layered architecture.

---

## ⚙️ How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/scalable_agent_system.git
cd scalable_agent_system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main_langgraph.py
```

### 4. Interact with the Agent

* Type your query in the console.
* Example: `Send an invoice through email
* Type `exit` or `quit` to close the program.

---

## Project Structure

```
scalable_agent_system/
│
├── main_langgraph.py
│
├── core/
│   └── config.py
│
├── graph/
│   ├── graph_builder.py
│   ├── state_schema.py
│   └── nodes/
│       ├── tool_router_node.py
│       ├── tool_layer_node.py
│       └── output_node.py
│
├── tools/
│   ├── paypal_tool.py
│   ├── email_tool.py
│   ├── rag_tool.py
│   └── system_search_tool.py
│
└── requirements.txt
```

---

##  Module Details

### **main_langgraph.py**

* Acts as the entry point of the system.
* Handles user input, initializes the graph, and displays responses.

### **core/config.py**

* Contains configuration settings and logs available tools.
* Manages initial setup for system capability listing.

### **graph/**

* Implements the LangGraph-based reasoning and routing pipeline.
* **graph_builder.py:** Builds and connects all nodes in the agent graph.
* **state_schema.py:** Defines data structure for agent states.
* **nodes/**

  * **tool_router_node.py:** Routes user queries to the appropriate tool.
  * **tool_layer_node.py:** Executes the selected tool (Email, PayPal, RAG, etc.).
  * **output_node.py:** Formats and returns the final response to the user.

### **tools/**

* Independent modules representing specific tool functionalities:

  * **email_tool.py:** Handles email operations.
  * **paypal_tool.py:** Interacts with PayPal APIs (e.g., invoices, payments).
  * **rag_tool.py:** Retrieves context from ChromaDB for RAG-based responses.
  * **system_search_tool.py:** Searches logs, available tools, or system data.

---

## Key Design Features

* **Separation of Concerns:**
  The *Tool Router Node* handles reasoning and selection logic, while the *Tool Layer Node* executes corresponding tool functions.
  This separation ensures scalability — adding new tools doesn’t impact routing performance.

* **Scalable Architecture:**
  Built with LangGraph to support modular expansion for 100+ tools.

* **State Management:**
  Maintains conversational context through structured `AgentState`.

* **Error Handling:**
  Graceful handling of missing tools, API failures, or retrieval issues to ensure stable execution.

---

## 🧾 Requirements

To install all dependencies:

```bash
pip install -r requirements.txt
```
## 💡 Example Queries

* “Send an invoice of INV-1001 through email
* “Search system capabilities.”
* “Retrieve documentation about PayPal invoices.”

---
