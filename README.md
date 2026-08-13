# Online Quiz Platform

A lightweight, extensible online quiz platform built with Flask and SQLAlchemy. It provides a simple admin interface for creating quizzes, questions and categories, and a student interface for taking quizzes and reviewing attempts.

## Highlights
- Admin and student roles with separate dashboards
- Multiple-choice question support with automated scoring
- Attempt tracking and detailed review
- SQLite by default, optional MySQL via env vars

## Quick Start

1. Clone the repo and enter the project folder:

```bash
git clone https://your.git.repo/Online_Quiz_Platform.git
cd Online_Quiz_Platform
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables (create a `.env` file):

```
SECRET_KEY=your-secret-key
# Optional MySQL configuration; if omitted the app uses SQLite at `online_quiz_platform.db`.
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

5. Run database migrations (if you want to apply the provided migrations):

```bash
# Using Flask-Migrate (if available)
flask db upgrade
# Or using Alembic directly
alembic upgrade head
```

6. Start the application:

```bash
python run.py
```

The app will be available at http://127.0.0.1:5000 by default.

## Environment Variables (from `app/config.py`)
- `SECRET_KEY` — Flask secret key (default: `'default-dev-key'` if unset)
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` — when all set, the app will connect to MySQL using these values; otherwise it falls back to a SQLite database file at the project root.

## Project Layout

- `run.py` — application entrypoint
- `app/` — Flask package (blueprints, models, forms, services)
- `migrations/` — Alembic migration scripts
- `requirements.txt` — Python dependencies
- `tests/` — test cases

## Running Tests

```bash
pytest
```

## Notes for Developers
- Config is loaded via `python-dotenv` in `app/config.py`.
- Default dev database is `online_quiz_platform.db` in project root when DB env vars are not set.
- If you add or modify models, generate migrations with Flask-Migrate / Alembic.

## Contributing
Contributions welcome. Please open issues or PRs; for significant changes, open an issue first to discuss.

## License
MIT — add a `LICENSE` file if you want to include the full text.

---

If you'd like, I can also:
- add a `.env.example` file with the variables above
- add a short developer script (`scripts/setup_dev.sh` / `setup_dev.ps1`) to automate venv + install + migrations

