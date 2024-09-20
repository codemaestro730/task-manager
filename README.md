# Task Manager Project
This project is a Task Manager application built with Django, utilizing PostgreSQL for database storage, Redis for caching, and Nginx as a reverse proxy server. It features both GraphQL and REST APIs for managing tasks.

## Setup Project with Docker
### Prerequisites
Before you begin, ensure you have Docker and Docker Compose installed on your system. For installation instructions, please refer to the official Docker documentation.

### Installation
#### Setup Environment variables
1. Copy the .env.example file to a new file named .env.
```bash
cp .env.example .env
```
2. Open the .env file in your favorite text editor and update the environment variables to match your setup.

#### Build and Run the containers
```bash
docker-compose up --build -d
```

### Run Migrations
After starting the containers, you need to run migrations to set up your database schema:
```bash
docker-compose exec web python manage.py migrate
```

### Seeding the Database
To seed the database with initial data, run:
```bash
docker-compose exec web python manage.py seed_users
```
This command adds a default user to the database.
   - username: admin, email: admin@test.com  pass: Test!2345, role: super_user

### Accessing the Application
- The GraphQL API endpoint is available at http://localhost:8000/graphql/.
- The REST API endpoints are accessible under http://localhost:8000/api/.


### Additional Information
- **Customizing Nginx Configuration:**: 
The Nginx configuration can be found and modified in ./config/nginx/app.conf. After making changes, you'll need to restart the Nginx container for the changes to take effect.


## Additional Setup: Systemd Service for Startup Management
### Creating a Systemd Service File
1. **Create the Service File:**
Create a new systemd service file named `test.service` in the `/etc/systemd/system` directory.
```bash
sudo nano /etc/systemd/system/test.service
```

2. **Add the Following Content:**
```ini
[Unit]
Description=Docker Composed Test Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```
Replace /path/to/your/project with the actual path to your project directory.
For example: **/home/administrator/Documents/projects/task-manager/task_manager**

3. **Reload systemd, Enable and Start the Sevice.**
```bash
sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl start test.service
```
This setup ensures your Docker containers managed by Docker Compose are started automatically.

## Setting Up on a Blank Ubuntu Server
1. **Install Docker and Docker Compose:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
```

2. **Enable and start Docker:**
```bash
sudo systemctl enable docker
sudo systemctl start docker
```

3. **Setup your project:**
- Transfer your project to the server.
- Ensure .env is correctly configured.

4. **Enable and start your systemd service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl start test.service
```

## Setup Project on Local
### Prerequisites
Before you begin, ensure you have the following installed:

- Python 3.12
- Poetry (for dependency management)

### Setup
1. **Install the project dependencies**
```bash
poetry install --no-root
```

2. **Activate the virtual environment created by Poetry**
```bash
poetry shell
```

3. **Setup environment variable**
- Create .env file from .env.example.
- Add variables in .env.
```
DB_NAME=test_db
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
```

4. **Run Migration**
```bash
python manage.py migrate
```

5. **Run Seed**
```bash
python manage.py seed_users
```

There is a default user added from the seed:
   - username: admin, email: admin@test.com  pass: Test!2345, role: super_user


### Running the App
To run the application manually, use the following command:
```bash
python manage.py runserver
```
The app will be available at [http://localhost:8000](http://localhost:8000).

## Features
- **GraphQL API:** http://localhost:8000/graphql/
- **REST API:** http://localhost:8000/api/
  - **Login API:** http://localhost:8000/api/auth/login/ [POST]
  - **Task List API:** http://localhost:8000/api/tasks/ [GET]
  - **Task Get API:** http://localhost:8000/api/tasks/:id/ [GET]
  - **Task Create API:** http://localhost:8000/api/tasks/ [POST]
  - **Task Update API:** http://localhost:8000/api/tasks/ [PUT]
  - **Task Delete API:** http://localhost:8000/api/tasks/:id/ [DELETE]

## Examples
### 1. Login (Get Token)
Request body is following as
```json
{
    "username": "admin",
    "password": "Test!2345"
}
```
Then you can get token from this api.
For task REST API ang GraphQL API, you need to add authorization params to the request header

```
Authorization Token <token>
```

### 2. Get task list REST API with pagination and filter with is_completed status
```
http://localhost:8000/api/tasks/?is_completed=true&page=1&page_size=5
```

### 3. Create Task REST API
Request body is following as
```json
{
    "title": "Test",
    "description": "Test description",
    "is_completed": true
}
```

### 4. Get task list GraphQL API with filter with is_completed status
Example Query:
```graphql
query AllTasks {
    allTasks(isCompleted: true) {
        id
        title
        description
        isCompleted
        createdAt
        updatedAt
    }
}
```

### 5. Create a task GraphQL API
Example Mutation:
```graphql
mutation CreateTask {
    createTask(
        input: { title: "Test", description: "Description", isCompleted: true }
    ) {
        task {
            id
            title
            description
            isCompleted
            createdAt
            updatedAt
        }
    }
}
```