"""
Smart File Manager - Backend Operations
Provides clean functions for file CRUD operations.
"""

from pathlib import Path


def create_file(name: str, data: str) -> dict:
    """Create a new file with given content."""
    try:
        path = Path(name)
        if path.exists():
            return {"success": False, "message": f"File '{name}' already exists."}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")
        return {"success": True, "message": f"File '{name}' created successfully."}
    except Exception as err:
        return {"success": False, "message": f"Error: {err}"}


def read_file(name: str) -> dict:
    """Read and return content of a file."""
    try:
        path = Path(name)
        if not path.exists():
            return {"success": False, "message": f"File '{name}' does not exist."}
        content = path.read_text(encoding="utf-8")
        return {"success": True, "content": content, "message": "File read successfully."}
    except Exception as err:
        return {"success": False, "message": f"Error: {err}"}


def rename_file(old_name: str, new_name: str) -> dict:
    """Rename a file."""
    try:
        old_path = Path(old_name)
        new_path = Path(new_name)
        if not old_path.exists():
            return {"success": False, "message": f"File '{old_name}' does not exist."}
        if new_path.exists():
            return {"success": False, "message": f"File '{new_name}' already exists."}
        old_path.rename(new_path)
        return {"success": True, "message": f"File renamed to '{new_name}' successfully."}
    except Exception as err:
        return {"success": False, "message": f"Error: {err}"}


def append_file(name: str, data: str) -> dict:
    """Append content to an existing file."""
    try:
        path = Path(name)
        if not path.exists():
            return {"success": False, "message": f"File '{name}' does not exist."}
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n" + data)
        return {"success": True, "message": f"Content appended to '{name}' successfully."}
    except Exception as err:
        return {"success": False, "message": f"Error: {err}"}


def overwrite_file(name: str, data: str) -> dict:
    """Overwrite file content."""
    try:
        path = Path(name)
        if not path.exists():
            return {"success": False, "message": f"File '{name}' does not exist."}
        path.write_text(data, encoding="utf-8")
        return {"success": True, "message": f"File '{name}' overwritten successfully."}
    except Exception as err:
        return {"success": False, "message": f"Error: {err}"}


def delete_file(name: str) -> dict:
    """Delete a file."""
    try:
        path = Path(name)
        if not path.exists():
            return {"success": False, "message": f"File '{name}' does not exist."}
        path.unlink()
        return {"success": True, "message": f"File '{name}' deleted successfully."}
    except Exception as err:
        return {"success": False, "message": f"Error: {err}"}
