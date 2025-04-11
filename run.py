import click
from app.seeds.seed_data import seed_database
import uvicorn

@click.group()
def cli():
    pass

@cli.command()
def seed():
    """Populate the database with sample data"""
    seed_database()

@cli.command()
def run():
    """Run the FastAPI server"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    cli() 