import sys
import click
from functools import wraps
from sqlalchemy.exc import IntegrityError
from .app import create_app
from .database import db
from .models import User
from .services import pow_service
from .services import fib_service
from .services import fact_service

# ——— App and context decorator ———
app = create_app()


def with_app_context(f):
    """Run this command inside Flask’s app context."""

    @wraps(f)
    def wrapped(*args, **kwargs):
        with app.app_context():
            return f(*args, **kwargs)

    return wrapped


# ——— CLI group ———
@click.group()
def cli():
    """Math Service CLI"""
    pass


# ——— Math commands ———
@cli.command()
@click.argument("base", type=int)
@click.argument("exp", type=int)
@with_app_context
def power(base, exp):
    """Compute BASE raised to the EXP power."""
    click.echo(pow_service(base, exp))


@cli.command(name="fib")
@click.argument("n", type=int)
@with_app_context
def fibonacci(n):
    """Compute the N-th Fibonacci number."""
    click.echo(fib_service(n))


@cli.command(name="fact")
@click.argument("n", type=int)
@with_app_context
def factorial(n):
    """Compute N! (factorial)."""
    click.echo(fact_service(n))


# ——— Create user command ———
@cli.command("create-user")
@click.argument("username")
@with_app_context
def create_user(username):
    """Create a new user USERNAME; prompts for password."""
    pwd = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    user = User(username=username)
    user.set_password(pwd)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        click.echo(f"⚠️  User '{username}' already exists", err=True)
        sys.exit(1)
    click.echo(f"✅ User '{username}' created")


@cli.command("clear-db")
@with_app_context
def clear_db():
    """Drop & recreate all tables."""
    db.drop_all()
    db.create_all()
    click.echo("✅ Database cleared and schema re-created.")


# ——— Entry point ———
if __name__ == "__main__":
    cli()
