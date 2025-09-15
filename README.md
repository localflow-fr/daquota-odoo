# Daquota Connector for Odoo

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0-brightgreen.svg)](https://www.odoo.com)  
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)  

**Version:** 17.0.1.0.0  
**License:** LGPL-3  
**Author:** LocalFlow 
**Website:** [https://localflow.fr](https://localflow.fr)

---

## Overview

The **Daquota Connector** allows Odoo users to seamlessly open and interact with **Daquota apps** directly from within Odoo.  
It includes free access to **LocalFlow Maps** and integrates with Odoo's existing geolocation features.

---

## Features

- Open Daquota web applications from Odoo.
- Dedicated configuration menu for Daquota settings.
- Security rules for controlled access.
- Access to LocalFlow Maps for Odoo (free, no registration required) - [https://localflow.fr/maps](https://localflow.fr/maps).
- Integration with `partner_geolocalize` for location-based data.

---

## Requirements

- Odoo **17.0** (community or enterprise).
- The Odoo module **`partner_geolocalize`** must be available (automatically handled via manifest).
- Internet access for connecting to Daquota services (https://apps.daquota.io, https://backoffice.daquota.io).

---

## Installation

### 1. From GitHub

1. Clone this repository into your Odoo `addons` folder:
   ```bash
   cd /path/to/odoo/addons
   git clone https://github.com/<your-org>/daquota-odoo.git
   ```

2. Restart your Odoo server:
   ```bash
   ./odoo-bin -c /etc/odoo.conf -d <your-database> -u base
   ```

3. Activate developer mode in Odoo (⚙️ → Settings → Activate Developer Mode).

4. Go to **Apps**, search for **Daquota Connector**, and click **Install**.

### 2. From Odoo Apps Store

(Coming soon)

Simply search for **Daquota Connector** in Odoo Apps and install with one click.

---

## Configuration

1. Navigate to **Daquota → Configuration** in the Odoo Settings.
2. Enter your credentials and settings.
   - Your Odoo database name
   - Select an integration method (login/password or API key)
   - If login/password, pick an integration user with appropriate permissions and fill in the login and password to allow Daquota to access your Odoo database.
   - If API key, enter the API key (it will use the current user).
3. Save and test the connection.
   - Open the Odoo menu and click **LocalFlow Maps**.
   - If the connection is successful, you should see a map of your Odoo database (contacts, partners, etc.).

---

## Usage

From the Odoo's menu, launch available Daquota applications (e.g., LocalFlow Maps).

---

## Upgrade Process

When upgrading to a new version of the Daquota Connector:

1. Pull the latest code from GitHub:
   ```bash
   cd /path/to/odoo/addons/daquota-odoo
   git pull origin main
   ```

2. Restart your Odoo server.

3. In Odoo, activate developer mode and go to **Apps**.

4. Click **Upgrade** next to the **Daquota Connector** module.

⚠️ **Note:** Always back up your database before upgrading to ensure data safety.

---

## Contributing

Contributions are welcome!  
- Fork the repository
- Create a feature branch
- Submit a pull request

---

## License

This module is licensed under the **LGPL-3** license. See [LICENSE](LICENSE) for more details.
