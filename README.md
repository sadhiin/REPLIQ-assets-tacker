"# REPLIQ-assets-tacker"


## API Documentation: Asset Tracker System

This API provides functionalities for managing assets (devices) within a company structure. It includes features for user authentication, company and employee registration, device creation and assignment, checkout logs, and filtering assigned/available devices.

**Authentication:**

The API utilizes Django's built-in token-based authentication system. To authenticate, send a POST request to the `/login/` endpoint with the following data:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

A successful login response will include a token in the `key` field:

```json
{
  "token": "your_authentication_token"
}
```

Include this token in the `Authorization` header of subsequent requests using the `Bearer` scheme:

```
Authorization: Bearer your_authentication_token
```

**Permissions:**

- **`IsAuthenticated`:** Required for most endpoints except login and user creation (`/users/`).
- **`IsAdminUser`:** Required for creating users (`/users/`).

**Endpoints:**

**1. User Management:**

- **`/login/` (POST):** Authenticate a user and obtain a token for subsequent requests.

**2. Company Management (Requires Authentication):**

- **`/companies/` (GET):** List all companies associated with the authenticated user (if admin) or the user's company (if not admin).
- **`/companies/` (POST):** Create a new company (requires admin privileges).
- **`/companies/<int:pk>/` (GET):** Retrieve details of a specific company.
- **`/companies/<int:pk>/` (PUT):** Update details of a company (requires admin privileges).

**3. User Creation (Requires Admin Privileges):**

- **`/users/` (POST):** Create a new user with appropriate permissions.

**4. Employee Management (Requires Authentication):**

- **`/companies/<int:company_pk>/employees/` (GET):** List all employees belonging to a specific company (restricted to the authenticated user's company).
- **`/companies/<int:company_pk>/employees/` (POST):** Create a new employee associated with the given company (requires admin privileges within the company).

**5. Device Management (Requires Authentication):**

- **`/devices/` (GET, POST):** List all devices or create a new device (requires admin privileges).
- **`/devices/<int:pk>/` (GET, PUT):** Retrieve details of a specific device or update its information (requires admin privileges).

**6. Checkout Logs (Requires Authentication):**

- **`/checkouts/` (GET, POST):** List all checkout logs or create a new checkout record (requires admin privileges).

**Filtering:**

- You can filter devices by their assigned status (assigned/available) using a query parameter:

  ```
  /devices/?assigned_to__isnull=true  // List available devices (not assigned to any employee)
  /devices/?assigned_to__isnull=false // List assigned devices
  ```

**Serializers:**

The API utilizes Django REST Framework serializers to represent model data in JSON format. These serializers define the fields included in the response and handle data validation during creation and updates.

**Additional Notes:**

- Refer to the Django REST Framework documentation for advanced usage and customization options: [https://www.django-rest-framework.org/topics/browsable-api/](https://www.django-rest-framework.org/topics/browsable-api/)
- Consider implementing error handling with appropriate status codes (e.g., 400 for bad requests, 401 for unauthorized access) in your views.
- Explore best practices for securing your API, such as using HTTPS and implementing rate limiting.


