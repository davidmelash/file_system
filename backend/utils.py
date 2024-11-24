import os
import uuid

def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename to prevent file overwriting
    
    Args:
        original_filename (str): Original filename with extension
    
    Returns:
        str: Unique filename preserving original extension
    """

    name, ext = os.path.splitext(original_filename)
    

    unique_id = uuid.uuid4().hex[:8]
    

    unique_filename = f"{name}_{unique_id}{ext}"
    
    return unique_filename

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security risks
    
    Args:
        filename (str): Original filename
    
    Returns:
        str: Sanitized filename
    """

    filename = os.path.basename(filename)
    

    filename = "".join(
        char for char in filename 
        if char.isalnum() or char in ['.', '_', '-']
    )
    
    return filename

def get_file_size(filepath: str) -> int:
    """
    Get the size of a file in bytes
    
    Args:
        filepath (str): Path to the file
    
    Returns:
        int: File size in bytes
    """
    return os.path.getsize(filepath)

def create_upload_directory(base_path: str = "uploads") -> str:
    """
    Create upload directory if it doesn't exist
    
    Args:
        base_path (str, optional): Base directory for uploads. Defaults to "uploads".
    
    Returns:
        str: Path to the created upload directory
    """
    os.makedirs(base_path, exist_ok=True)
    return base_path