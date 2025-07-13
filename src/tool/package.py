import zipfile
import tomllib
import json
from typing import Literal
from pathlib import Path

from global_variable import CWD, MAIN, GENERATED

PACKAGE_TYPE = Literal["data_pack", "resource_pack", "mod"]
SOURCE_TYPE = Literal["main", "generated"]


def get_metadata():
    if (forge_metadata := MAIN / "META-INF/mods.toml").is_file():
        with forge_metadata.open("rb") as file:
            return ("forge", tomllib.load(file))
    elif (neoforge_metadata := MAIN / "META-INF/neoforge.mods.toml").is_file():
        with neoforge_metadata.open("rb") as file:
            return ("neoforge", tomllib.load(file))
    elif (fabric_metadata := MAIN / "fabric.mod.json").is_file():
        with fabric_metadata.open("r", encoding="utf-8") as file:
            return ("fabric", json.load(file))
    else:
        raise FileNotFoundError(
            "No metadata file found. Please ensure META-INF/mods.toml, META-INF/neoforge.mods.toml or fabric.mod.json exists."
        )


def get_files(package_type: PACKAGE_TYPE, source_type: SOURCE_TYPE):
    """get files from src/main/ folder

    Args:
        type (str): type of file to get
    """
    files = []
    match package_type:
        case "data_pack":
            files = ["data/", "pack.png", "pack.mcmeta"]
        case "resource_pack":
            files = ["assets/", "pack.png", "pack.mcmeta"]
        case "mod":
            files = [
                "assets/",
                "data/",
                "META-INF/",
                "pack.png",
                "pack.mcmeta",
                "fabric.mod.json",
            ]
    return filter(
        lambda path: path.exists(),
        map(lambda path: (MAIN if source_type == "main" else GENERATED) / path, files),
    )


def get_version() -> str:
    """get version from src/main/META-INF/mods.toml"""
    type, metadata = get_metadata()

    if type in {"forge", "neoforge"}:
        return metadata["mods"][0]["version"]
    elif type == "fabric":
        return metadata["version"]
    else:
        raise FileNotFoundError(
            "No metadata file found. Please ensure META-INF/mods.toml, META-INF/neoforge.mods.toml or fabric.mod.json exists."
        )


def get_output_filename(type: PACKAGE_TYPE, version: str):
    """get extension for package

    Args:
        type (package_type): type of package to create
        version (str): version of package to create
    """
    loader_type, metadata = get_metadata()
    filename = ""

    if loader_type in {"forge", "neoforge"}:
        filename = metadata["mods"][0]["displayName"].replace(" ", "_")
    else:
        filename = metadata["name"].replace(" ", "_")

    suffix = {
        "data_pack": "data",
        "resource_pack": "resource",
        "mod": "mod",
    }
    extension = "jar" if type == "mod" else "zip"

    return f"{filename}-{suffix[type]}-{version}.{extension}"


def package(type: PACKAGE_TYPE):
    """package mod or data pack

    Args:
        type (str): type of package to create
    """
    version = get_version()
    output_filename = get_output_filename(type, version)
    main_files = get_files(type, "main")
    generated_files = get_files(type, "generated")

    output_path = CWD / "versions" / output_filename
    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, "w") as zip:

        def write_file(file: Path, relative_to: Path):
            if file.is_dir():
                for path in file.rglob("*"):
                    zip.write(path, path.relative_to(relative_to))
            else:
                zip.write(file, file.name)

        for file in main_files:
            write_file(file, MAIN)

        for file in generated_files:
            write_file(file, GENERATED)

        print(f"Packaged {type} for version {version} to {output_filename}")


def main():
    # package("data_pack")
    # package("resource_pack")
    package("mod")

main()
