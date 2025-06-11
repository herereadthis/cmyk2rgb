"""
File Notes

typer is a CLI framework for Python. It helps you make command-line interfaces.
"""
import typer
from typing import Optional
from cmyk2rgb.converter import cmyk_to_rgb

app = typer.Typer()

PROFILE_MAP = {
    "fogra": "Coated_Fogra39L_VIGC_300.icc",
    "japan": "JapanColor2011Coated.icc",
    "swop": "SWOP2006_Coated3v2.icc",
}

def prompt_profile() -> str:
    typer.echo("Select an ICC profile:")
    typer.echo("1) FOGRA39 (European coated)")
    typer.echo("2) Japan Color 2011 Coated")
    typer.echo("3) US Web Coated SWOP v2")
    choice = typer.prompt("Enter choice (1/2/3)")
    mapping = {"1": "fogra", "2": "japan", "3": "swop"}
    return mapping.get(choice, "fogra")

@app.command()
def convert(
    c: int,
    m: int,
    y: int,
    k: int,
    profile: Optional[str] = typer.Option(
        None,
        help="ICC profile alias: fogra, japan, swop"
    )
):
    """Convert CMYK to RGB using specified ICC profile."""
    if profile is None:
        profile = prompt_profile()

    profile_file = PROFILE_MAP.get(profile.lower())
    if not profile_file:
        typer.echo(f"Unknown profile '{profile}'. Using FOGRA39 by default.")
        profile_file = PROFILE_MAP["fogra"]

    typer.echo(f"Using profile: {profile_file}")
    rgb = cmyk_to_rgb(c, m, y, k, profile_file)
    typer.echo(f"RGB: {rgb}")

@app.command()
def convert_batch():
    """Converts a .csv file of CMYK values to RGB."""
    print("Batch conversion is not implemented yet.")

def main():
    app()

if __name__ == "__main__":
    main()
