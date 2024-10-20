# Backend of Puzzles Project

RestAPI with Python's FastAPI, for the backend of Puzzles Project.

The front-end repository is [here](https://github.com/witch-puzzles/frontend-puzzles).


## License

This project is licensed under the `GNU GPL-3.0` license.

Although everything is free to use, modify and distribute, credit is always appreciated.


## Setup

### Dependencies

The project is written in Python 3.12.4. Create a virtual environment and activate it.

```bash
python -m venv venv
source venv/bin/activate
```

To install the dependencies, run:

```bash
pip install -r requirements.txt
## or
make init
```

---

The rest will be written as the project progresses.


##  Directory Structure

The current project structure is designed as below. Components may change as the project evolves.

```bash
app/
├── core/                # Core configuration and initialization (settings, dependencies, etc.)
├── crud/                # CRUD (Create, Read, Update, Delete) operations for database models
├── libs/                # External libraries and shared utilities
├── entities/            # Database table entities/schema
├── routers/             # API endpoints (routers) grouped by functionality
├── schemes/             # Pydantic models for request/response validation
├── services/            # Business logic and service layer
├── utils/               # Helper functions and utilities
├── main.py              # Entry point for the FastAPI app
tests/                   # Unit and integration tests
alembic/                 # Alembic configuration and database migration scripts
alembic.ini              # Alembic settings for database migrations
.env                     # Environment variables for configuration
.env.example             # Example environment variables file
requirements-test.txt    # Testing dependencies
requirements.txt         # Project dependencies
Makefile                 # Automation of commands like testing, running, etc.
.gitignore               # Git configuration to ignore specified files and folders
README.md                # Project documentation
LICENSE                  # Project license file
```


## Conventions

**Branches**: `main` is the main branch, for the stable version of the project. `dev` is the development branch, where the new features are implemented.

For the branch names, use the following pattern: `type/description`. For example, `feature/login`, `fix/bug-in-register` or `docs/update-readme`.

**Commits**: We are using conventional commits. For more information, check [this site](https://www.conventionalcommits.org/en/v1.0.0/).

Basically, the commit message should be like this: `<type>[optional scope]: <description>`

Generaly used types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Pull Requests**: The PRs should be made to the `dev` branch. The PRs should have a title and a description, explaining what was done and why.

**Python Syntax**: We are using PEP8 for the Python syntax. For more information, check [this site](https://peps.python.org/pep-0008/).

Basically we will use:
- camelCase for functions 
- snake_case for variables
- UpperCamelCase for classes
- UPPER_CASE for constants
- 2 spaces for indentation
