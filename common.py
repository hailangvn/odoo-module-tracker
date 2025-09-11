import ast
import contextlib
import os
import requests
import pysqlite3 as sqlite3
import subprocess
import yaml


def run(cwd, *args, **kwargs):
    """Shortcut to run a command in a given directory."""
    kwargs.setdefault("check", True)
    kwargs.setdefault("cwd", cwd)
    return subprocess.run(args, **kwargs)


def run_read(cwd, *args, **kwargs):
    """Shortcut to run a command in a given directory."""
    return run(cwd, *args, **kwargs, stdout=subprocess.PIPE).stdout.decode("utf-8")


def get_repo(CLONE_DIRECTORY, org, repo, version):
    """Clone or update a repo to the given version."""
    path = CLONE_DIRECTORY / org / repo / version
    if path.exists():
        print(f"Updating {org}/{repo}@{version}")
        run(path, "git", "checkout", version)
        run(path, "git", "pull")
    else:
        print(f"Cloning {org}/{repo}@{version}")
        org_path = CLONE_DIRECTORY / org / repo
        path.mkdir(exist_ok=True, parents=True)
        run(org_path, "git", "clone", f"https://github.com/{org}/{repo}", version, "-b", version)
    return path


def analyse_module(path):
    """Analyse a module and return a dict of its data."""
    manifest = path / "__manifest__.py"
    if not manifest.exists():
        return
    with open(manifest, mode="r") as f:
        data = ast.literal_eval(f.read())

    if not data.get("installable", True):
        return
    description_path = path / "static" / "description" / "index.html"

    description = ""
    if description_path.exists():
        with open(description_path, "r") as f:
            description = f.read()

    return {
        "name": data["name"],
        "author": data.get("author"),
        "depends": data.get("depends", []),
        "maintainers": data.get("maintainers", []),
        "development_status": data.get("development_status"),
        "summary": data.get("summary"),
        "description": description,
        "last_version": data.get("version"),
    }


def analyse_repo(path, analyse_module):
    """Analyse a repo and return a dict of module name and its data."""
    return {
        module.name: result
        for module in path.iterdir()
        for result in [analyse_module(path / module)]
        if result
    }


def upsert_repo(db, org, repo):
    """Get the repo id from the database, or insert it if it doesn't exist."""
    return scalar(
        db,
        """
        INSERT INTO repo (org, repo)
        VALUES (?, ?)
        ON CONFLICT(org, repo)
        DO UPDATE SET
            org = EXCLUDED.org,
            repo = EXCLUDED.repo
        RETURNING id
        """,
        org,
        repo,
    )


def make_common_schema(db, with_module):
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS repo (
            id INTEGER PRIMARY KEY,
            org TEXT,
            repo TEXT,
            UNIQUE(org, repo)
        )
        """
    )
    if with_module:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS module (
                id INTEGER PRIMARY KEY,
                repo_id INTEGER,
                name TEXT,
                title TEXT,
                author TEXT,
                depends TEXT,
                maintainers TEXT,
                development_status TEXT,
                summary TEXT,
                last_version TEXT,
                dep_tree TEXT,
                FOREIGN KEY(repo_id) REFERENCES repo(id)
                UNIQUE(repo_id, name)
            )
            """
        )


def download(path, url):
    """Download a file from a url and write it to path."""
    print(f"Downloading {url}")
    response = requests.get(url)
    response.raise_for_status()
    with open(path, "wb") as f:
        f.write(response.content)


@contextlib.contextmanager
def sqlite_db(path, make_schema, clean=False, download_url=None):
    """Context manager for the sqlite database."""
    if clean and path.exists():
        path.unlink()
    if not clean and not path.exists() and download_url:
        # Try to download last published db version
        url = f"{download_url}/{path.name}"
        try:
            download(path, url)
        except Exception as e:
            print(f"Fail to download db {url} {e}")

    conn = sqlite3.connect(path)

    db = conn.cursor()
    make_schema(db)
    try:
        yield db
        conn.commit()
    finally:
        conn.close()


def fetch(db, query, *args):
    """Fetch a single row from the database."""
    return db.execute(query, args).fetchone()


def scalar(db, query, *args):
    """Fetch a single value from the database."""
    res = fetch(db, query, *args)
    return res[0] if res else None


def get_environ(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    version = os.environ.get("ODOO_VERSION", "17.0")
    restrict = {
        tuple(org_repo.strip().split("/", 1))
        for restrict_modules in [os.environ.get("RESTRICT_MODULES", "")]
        for org_repo in restrict_modules.split(",")
        if restrict_modules
    }
    clean_db = os.environ.get("CLEAN_DB")
    return config, version, restrict, clean_db


def analyse(db, CLONE_DIRECTORY, config, version, restrict, process_repo):
    result = {}
    for org, repos in config.items():
        result[org] = {}
        for repo in repos:
            if restrict and (org, repo) not in restrict:
                continue
            if CLONE_DIRECTORY:
                try:
                    path = get_repo(CLONE_DIRECTORY, org, repo, version)
                except Exception as e:
                    print("Fail to fetch repo skip it.", e)
                    continue
            else:
                path = None
            process_repo(db, org, repo, version, path, result)

    return result
