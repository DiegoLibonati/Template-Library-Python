# Template-Library-Python

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Getting Started

1. Clone the repository
2. Go to the repository folder and execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.dev.txt`
7. Execute: `pip install -r requirements.test.txt`
8. Install the package in editable mode: `pip install -e .`
9. Run the project:
    1. From CLI: `python -m template_library_python.template`
    2. Or import as a library in Python: `from template_library_python import Template`

### Pre-Commit for Development

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Description

Personal template for developing an library with python.

## Technologies used

1. Python >= 3.11

## Libraries used

#### Requirements.txt

```
pydantic==2.11.9
```

#### Requirements.dev.txt

```
pre-commit==4.3.0
pip-audit==2.7.3
```

#### Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Template-Library-Python`](https://www.diegolibonati.com.ar/#/project/Template-Library-Python)

## Testing

1. Go to the repository folder
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.test.txt`
7. Install the package in editable mode: `pip install -e .`
8. Execute: `pytest --log-cli-level=INFO`

## Security Audit

You can check your dependencies for known vulnerabilities using **pip-audit**.

1. Go to the repository folder
2. Activate your virtual environment
3. Execute: `pip install -r requirements.dev.txt`
4. Execute: `pip-audit -r requirements.txt`

## Env Keys

This template does not use environment variables by default. However, if your library requires external configuration such as API keys, secrets, or service URLs, you can add them to the `.env` file following the `.env.example` structure.

```
# Example
MY_LIBRARY_API_KEY=your_api_key_here
MY_LIBRARY_BASE_URL=https://api.example.com
```

The consuming application is responsible for loading the `.env` file (e.g. using `python-dotenv`). The library itself should only read from `os.environ` via `os.getenv`.

## Project Structure

```
Template-Library-Python/
├── src/
│   └── template_library_python/
│       ├── __init__.py
│       ├── template.py
│       ├── configs/
│       │   ├── __init__.py
│       │   └── logger_config.py
│       ├── constants/
│       │   ├── __init__.py
│       │   ├── codes.py
│       │   └── messages.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── template_model.py
│       └── utils/
│           ├── __init__.py
│           └── exceptions.py
├── test/
│   ├── configs/
│   │   ├── __init__.py
│   │   └── test_logger_config.py
│   ├── constants/
│   │   ├── __init__.py
│   │   ├── test_codes.py
│   │   └── test_messages.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── test_template_model.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── test_exceptions.py
│   ├── __init__.py
│   ├── conftest.py
│   └── test_template.py
├── .env
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements.dev.txt
└── requirements.test.txt
```

1. `src/template_library_python` -> Root directory of the source code. Contains the full library logic following a **layered architecture** pattern.
2. `configs` -> Contains **logging setup** and any shared configuration utilities used across the library.
3. `constants` -> Holds **static values** such as error codes and user-facing messages, centralized to ensure consistency across the codebase.
4. `models` -> Defines **Pydantic models** for data validation and serialization.
5. `utils` -> Contains the **custom exception hierarchy** and other shared utilities used across multiple modules.
6. `template.py` -> The **main public class** of the library. This is the entry point that consumers interact with.
7. `test` -> Contains **tests** organized to mirror the `src/` structure.
8. `conftest.py` -> Defines **shared pytest fixtures** used across all test modules.
9. `pyproject.toml` -> **Unified project configuration** for setuptools, pytest, and ruff.
10. `requirements.txt` -> Lists **production dependencies**.
11. `requirements.dev.txt` -> Lists **development dependencies** (pre-commit, pip-audit).
12. `requirements.test.txt` -> Lists **testing dependencies** (pytest and plugins).

## Architecture & Design Patterns

### Layered Architecture

The library follows a **bottom-up layered architecture** where each layer depends only on the layers below it. This enforces clear separation of concerns and makes each layer independently testable.

```
┌─────────────────────────────────────┐
│         Template (Public API)       │  ← Layer 5: Business logic
├─────────────────────────────────────┤
│            models/                  │  ← Layer 4: Data validation (Pydantic)
├─────────────────────────────────────┤
│            configs/                 │  ← Layer 3: Infrastructure (logging)
├─────────────────────────────────────┤
│             utils/                  │  ← Layer 2: Exception hierarchy
├─────────────────────────────────────┤
│           constants/                │  ← Layer 1: Error codes & messages
└─────────────────────────────────────┘
```

**Layer 1 — `constants/`**: Single source of truth for all error codes (`codes.py`) and human-readable messages (`messages.py`). No other logic lives here; no imports from upper layers.

**Layer 2 — `utils/exceptions.py`**: Custom exception hierarchy rooted at `BaseError`. Each exception carries a `code` and a `message` pulled from the constants layer. Subclasses (`ValidationError`, `NotFoundError`, `AuthenticationError`, `ConflictError`, `BusinessError`, `InternalError`) represent distinct semantic error categories.

**Layer 3 — `configs/logger_config.py`**: Infrastructure setup. Exposes `setup_logger()`, which configures a `logging.Logger` with a consistent format and output stream. Depends only on the constants layer.

**Layer 4 — `models/`**: Pydantic `BaseModel` subclasses for declarative input validation. Validation rules (field constraints, type coercion) are declared here rather than scattered through business logic.

**Layer 5 — `template.py`**: The main `Template` class. This is the only public API surface (`__all__ = ["Template"]`). It composes all lower layers: uses the logger factory, raises typed exceptions, and validates inputs through models.

---

### Design Patterns

#### Factory Method — `setup_logger()`
`setup_logger(name)` is a factory function that creates and returns a fully configured `logging.Logger`. Consumers never instantiate loggers directly, ensuring a consistent format, level, and output stream across all modules.

#### Guard / Idempotent Initialization
Inside `setup_logger()`, the guard `if not logger.handlers:` prevents duplicate handlers from being attached when the function is called more than once with the same name. This is a common pattern when module-level loggers are used in libraries.

#### Custom Exception Hierarchy
All exceptions extend `BaseError`, which carries both a machine-readable `code` and a human-readable `message`. This enables callers to catch specific exception types (`except NotFoundError`) or the entire hierarchy (`except BaseError`), and to inspect structured error information programmatically.

```
Exception
└── BaseError
    ├── ValidationError
    ├── AuthenticationError
    ├── NotFoundError
    ├── ConflictError
    ├── BusinessError
    └── InternalError
```

#### Composition
The `Template` class does not inherit from lower-layer components. Instead, it **composes** them: the logger is obtained via `setup_logger()`, exceptions are raised using the exception hierarchy, and input validation is delegated to Pydantic models. This keeps the class focused on business logic and makes dependencies explicit.

#### Centralized Constants
Error codes and messages are defined once in `constants/` and imported wherever needed. This prevents magic strings from spreading through the codebase and makes updates (e.g., changing an error message) a single-file change.

#### Declarative Validation (Pydantic)
Input validation rules are expressed as field annotations on Pydantic models rather than imperative checks inside methods. This keeps the `Template` class lean and makes validation rules easy to read, test, and extend.

---

### Module Interaction Flow

```
Consumer Code
      │
      ▼
Template  ──► TemplateModel (validates input)
      │
      ├──► setup_logger()   (logging infrastructure)
      │
      ├──► NotFoundError / ValidationError / ...  (typed exceptions)
      │         └──► CODE_* / MESSAGE_*  (constants)
      │
      └──► CODE_* / MESSAGE_*  (constants, used directly when raising)
```

---

### Public API

Only `Template` is exported. All other modules (`constants`, `utils`, `configs`, `models`) are internal implementation details and should not be imported directly by consumers.

```python
from template_library_python import Template
```

## Known Issues

None at the moment.