# Household Services Management Application

**Household Services Management Application** is a multi-user platform linking customers with service professionals. 

- **Admins** manage users, approvals, and services.
- **Customers** can search, request services, and give feedback.
- **Service Professionals** handle requests and updates.

Built with Flask, VueJS, and Redis, the application includes role-based features, automated reminders, and exportable reports for seamless management.

Welcome to open work! This project is open to contributions from the community. Any changes or recommendations are highly encouraged and appreciated.

## Installation Instructions

Follow the steps below to set up and run the application:

### 1. Change Directory Ownership
Ensure you have write permissions for the project directory. Replace `/path/to/your/project` with the actual path where you set up the project:
```bash
sudo chown -R $(whoami) /path/to/your/project
```

### 2. Install NPM Packages
Navigate to the frontend directory and install the required NPM packages:
```bash
npm install 

cd Frontend

npm install
```

### 3. Set Up Virtual Environment
Create and activate a Python virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate
```

### 4. Install Python Dependencies
Install all required Python libraries from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 5. Start Supporting Services
Start the required supporting services:
- **MailHog**:
  ```bash
  ~/go/bin/MailHog
  ```
- **Redis Server**:
  ```bash
  sudo service redis-server start
  ```
- **Celery Worker**:
  ```bash
  celery -A app.celery_app worker --loglevel=INFO
  ```

### 6. Run the Application
Finally, start the application:
```bash
python app.py
```
