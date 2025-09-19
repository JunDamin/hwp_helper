"""Template management service."""

import shutil
from pathlib import Path
from time import sleep
from typing import Dict, List, Tuple, Iterator, Optional

from hwpapi.core import App

from ..utils.file_utils import prettify_filename
from ..utils.image_utils import crop_background


class TemplateService:
    """Service for managing HWP templates."""
    
    def __init__(self):
        self.templates_dir = Path("templates")
        self.images_dir = Path("images")
        self.temp_dir = Path("temp")
    
    def get_categories(self) -> Dict[str, List[Tuple[str, Path, str, int]]]:
        """Get template categories from image files."""
        if not self.images_dir.exists():
            return {}
        
        images = list(self.images_dir.glob("*"))
        categories = {}
        
        for image in images:
            parts = image.stem.split("_")
            if len(parts) == 1:
                parts = [parts[0], "None", "0"]
            
            key, value, n = parts[0], parts[1], parts[2]
            filename = f"{key}_{value}" if value != "None" else key
            
            components = categories.get(key, [])
            components.append((value, image, filename, int(n)))
            categories[key] = components
        
        return categories
    
    def update_templates(self) -> Iterator[Tuple[int, int]]:
        """Update all templates from templates folder."""
        # Clean up old files
        if self.images_dir.exists():
            shutil.rmtree(self.images_dir)
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        
        # Create directories
        self.temp_dir.mkdir()
        self.images_dir.mkdir()
        
        # Get all template files
        if not self.templates_dir.exists():
            return
        
        hwp_files = list(self.templates_dir.glob("*.hwp"))
        total_files = len(hwp_files)
        
        if total_files == 0:
            return
        
        # Process templates
        app = App(new_app=True, is_visible=False)
        try:
            for i, hwp_file in enumerate(hwp_files):
                self._update_single_template(app, hwp_file)
                yield i, total_files
        finally:
            app.quit()
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
    
    def _update_single_template(self, app: App, hwp_path: Path) -> Optional[Path]:
        """Update a single template file."""
        try:
            app.open(hwp_path)
            app.actions.MoveDocEnd().run()
            
            # Add blank line if not ending with one
            if app.get_text() != "\r\n":
                app.actions.BreakPara().run()
                app.save()
            
            _, n, _ = app.api.GetPos()
            temp_image_path = self.temp_dir / f"{hwp_path.stem}_{n}.png"
            
            # Delete master page info
            app.api.SetMessageBoxMode(0x00010001)
            master_page_delete = app.actions.MasterPageDelete()
            master_page_delete.pset.Duplicate = 0
            master_page_delete.pset.Front = 0
            master_page_delete.pset.type = 0
            master_page_delete.run()
            
            sleep(0.1)
            app.save()
            app.api.SetMessageBoxMode(0xf0000)
            
            # Save as image
            app.save(temp_image_path)
            temp_png_path = self.temp_dir / f"{temp_image_path.stem}001.png"
            
            if temp_png_path.exists():
                cropped = crop_background(str(temp_png_path))
                if cropped:
                    final_image_path = self.images_dir / f"{hwp_path.stem}_{n}.png"
                    cropped.save(final_image_path)
            
            return hwp_path
            
        except Exception as e:
            print(f"Error updating template {hwp_path}: {e}")
            return None
    
    def add_template(self, app: App, category: str, name: str) -> bool:
        """Add a new template from selected content."""
        try:
            # Create temp directory
            self.temp_dir.mkdir(exist_ok=True)
            temp_path = self.temp_dir / "temp.hwp"
            
            # Save selected content
            app.save_block(temp_path)
            
            # Create final filename
            filename = prettify_filename(f"{category}_{name}")
            destination = self.templates_dir / f"{filename}.hwp"
            
            if destination.exists():
                return False
            
            # Move file to templates
            temp_path.rename(destination)
            
            # Clean up
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            
            return True
            
        except Exception as e:
            print(f"Error adding template: {e}")
            return False
    
    def delete_template(self, template_path: str, image_path: str) -> bool:
        """Delete a template and its associated image."""
        try:
            Path(template_path).unlink(missing_ok=True)
            Path(image_path).unlink(missing_ok=True)
            return True
        except Exception:
            return False
    
    def rename_template(self, old_template_path: str, old_image_path: str, 
                       new_category: str, new_name: str) -> bool:
        """Rename a template and its associated image."""
        try:
            new_filename = prettify_filename(f"{new_category}_{new_name}")
            
            # Extract image number from old path
            old_image = Path(old_image_path)
            n = old_image.stem.split("_")[-1]
            
            # Create new paths
            new_template_path = self.templates_dir / f"{new_filename}.hwp"
            new_image_path = self.images_dir / f"{new_filename}_{n}.png"
            
            if new_template_path.exists():
                return False
            
            # Rename files
            Path(old_template_path).rename(new_template_path)
            Path(old_image_path).rename(new_image_path)
            
            return True
            
        except Exception:
            return False
