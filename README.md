# School Management System - "Amoozesh-Yar"

This project is a comprehensive school management system developed using Django. It is designed to handle the core administrative, financial, and educational processes of a typical educational institution, based on the detailed specifications provided in the `AGENTS.md` (SRS) document.

The system is built with a focus on the Iranian context, featuring full support for the Jalali calendar and adherence to local financial regulations for salary calculations.

## Core Features

*   **User Management**: Multi-role system (Admin, Teacher, Parent, Student) with distinct permissions.
*   **Course & Class Management**: Define courses and schedule specific classes with assigned instructors.
*   **Student Enrollment**: A complete workflow for enrolling students in classes.
*   **Finance Module**: Automated tuition fee generation, payment tracking (simulated), and a detailed teacher salary calculator compliant with Iranian labor laws.
*   **Communications**: Placeholder for SMS notifications for important events.
*   **Jalali Calendar Support**: All dates throughout the system are handled using the Jalali calendar.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### 1. Prerequisites

*   Python 3.11+
*   `pip` for package management
*   `virtualenv` (recommended)

### 2. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    The required packages are listed in `requirements.txt`. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    This will create the necessary tables in the SQLite database based on the models defined in the apps.
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser account:**
    This will allow you to access the Django admin panel. Follow the prompts to create your admin user.
    ```bash
    python manage.py createsuperuser
    ```

### 3. Seeding the Database (Optional, but Recommended)

To test the application with a set of realistic data, you can use the custom `seed_data` management command. This will populate the database with fake users, courses, classes, and enrollments.

```bash
python manage.py seed_data
```
This command will first delete all existing data before seeding. The default admin user created is `admin` with the password `adminpass`.

### 4. Running the Development Server

Once the setup is complete, you can run the development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.
The Django admin panel is available at `http://127.0.0.1:8000/admin/`.

### 5. Running Tests

To ensure that all parts of the application are working correctly, you can run the unit tests:

```bash
python manage.py test
```

This will run all the test suites defined in the `tests.py` files across all apps.
