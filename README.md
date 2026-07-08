# 🌐 NetCraft - Enterprise ISP & Telecom Management SaaS

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-092E20.svg)
![DRF](https://img.shields.io/badge/Django_REST_Framework-red.svg)
![JWT](https://img.shields.io/badge/Authentication-SimpleJWT-black.svg)
![Status](https://img.shields.io/badge/Status-Backend_Ready-success.svg)

**NetCraft** is a highly modular, B2B-focused Enterprise ISP (Internet Service Provider) and Telecom Network Management backend system. It is designed to manage complex ISP architectures including Downstream ISPs, Enterprise Clients, Dark Fiber networks, and Cross-Connects. 

This robust API engine serves as the foundation for a fully customizable, drag-and-drop SaaS platform for ISPs.

---

## 🚀 Key Features

* **🛡️ Hardware-Locked SaaS Security:** Custom built Middleware and Licensing module (7-day trial to Lifetime plans) that strictly guards the API access.
* **🔐 JWT Authentication:** Enterprise-grade security using JSON Web Tokens.
* **🏗️ Multi-Tenant Modular Architecture:** Clean separation of concerns with 6 dedicated micro-apps.
* **📡 Complex Telecom Modeling:** Built-in logic for Bandwidth Modifications, Circuit Shiftings, and L2POI capacities.
* **🏷️ Dynamic White-Labeling:** Auto-generation of IDs (Circuits, DxR, Tenants) based on the specific Company's short code (e.g., `DIPL/CORE-BW/2026/001`).
* **📦 OTA Update Ready:** Built-in system version tracking designed for Over-The-Air software patching.

---

## 🧩 System Modules (The 6 Pillars)

1. **`app_core`**: The brain of the system. Handles Company Profiles, Pop Locations, System Logs, OTA Update tracking, System Licensing, and Employee Profiles.
2. **`app_crm`**: Manages B2B Enterprise Customers, Downstream ISPs, Corporate Clients, and their KYC/SLA attachments.
3. **`app_circuit`**: The core network engine. Manages Circuits (B2B, B2C, Core BW), Tenants, Terminations (A/B Ends), Bandwidth upgrades/downgrades, and site shifting.
4. **`app_dxr`**: Manages Data Exchange & Routing (DxR), Dark Fiber deployments, Rack Spaces, and X-Connects.
5. **`app_network`**: Handles BTS (Towers/Base Stations) and L2POI (Layer 2 Point of Interconnect) profiles.
6. **`app_provider`**: Manages upstream Telcos, bandwidth providers, and external provider networks.

---

## 💻 Tech Stack

* **Backend Framework:** Django & Django REST Framework (DRF)
* **Authentication:** djangorestframework-simplejwt
* **Database:** SQLite (Development) / PostgreSQL (Production ready)
* **Environment:** Compatible with PC, Cloud VPS, and Mobile environments (e.g., Termux)

---

## 🛠️ Local Setup & Installation

Follow these steps to get the API engine running on your local machine or terminal emulator:

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/netcraft-backend.git](https://github.com/yourusername/netcraft-backend.git)
cd netcraft-backend
