import os
import shutil
import pathlib
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """
    Utility to clear various cache files and directories in the project.
    """

    @staticmethod
    def clear_pytest_cache(root_dir=None):
        if not root_dir:
            root_dir = os.getcwd()
        
        cache_dirs = [".pytest_cache", "__pycache__", ".ipynb_checkpoints"]
        exclude_dirs = [".venv", ".git", ".idea", ".pytest_cache"] # Avoid recursive deletion of some system/env folders
        
        for directory in pathlib.Path(root_dir).rglob("*"):
            # Skip if any part of the path is in exclude_dirs (like .venv)
            if any(part in exclude_dirs for part in directory.parts):
                continue
                
            if directory.is_dir() and directory.name in cache_dirs:
                try:
                    # Check if directory exists before trying to delete
                    if directory.exists():
                        logger.info(f"Removing cache directory: {directory}")
                        shutil.rmtree(directory, ignore_errors=True)
                except Exception as e:
                    pass

    @staticmethod
    def clear_reports(root_dir=None):
        if not root_dir:
            root_dir = os.getcwd()
        
        reports_dir = os.path.join(root_dir, "reports")
        if os.path.exists(reports_dir):
            try:
                logger.info(f"Clearing reports directory: {reports_dir}")
                for filename in os.listdir(reports_dir):
                    file_path = os.path.join(reports_dir, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error clearing reports: {e}")

if __name__ == "__main__":
    # Can be run as a standalone script
    cm = CacheManager()
    cm.clear_pytest_cache()
    print("Project cache cleared.")
