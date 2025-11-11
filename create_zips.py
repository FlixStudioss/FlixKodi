#!/usr/bin/env python3
"""
Script to create properly formatted Kodi addon zip files
"""
import os
import zipfile
import hashlib
from pathlib import Path

def create_addon_zip(source_dir, output_dir, addon_id, version):
    """Create a zip file for a Kodi addon with proper structure"""
    zip_name = f"{addon_id}-{version}.zip"
    zip_path = os.path.join(output_dir, zip_name)
    
    # Remove old zip if exists
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    print(f"Creating {zip_name}...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Skip __pycache__ and .git directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.github']]
            
            for file in files:
                if file.endswith('.pyc'):
                    continue
                    
                file_path = os.path.join(root, file)
                # Create archive path with addon_id as root folder
                arcname = os.path.join(addon_id, os.path.relpath(file_path, source_dir))
                zipf.write(file_path, arcname)
    
    print(f"Created: {zip_path}")
    return zip_path

def create_addons_xml(repo_dir, addons):
    """Create addons.xml file"""
    addons_xml_path = os.path.join(repo_dir, 'addons.xml')
    
    print("Creating addons.xml...")
    
    with open(addons_xml_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<addons>\n')
        
        for addon_dir in addons:
            addon_xml = os.path.join(addon_dir, 'addon.xml')
            if os.path.exists(addon_xml):
                with open(addon_xml, 'r', encoding='utf-8') as addon_f:
                    # Skip XML declaration
                    lines = addon_f.readlines()
                    for line in lines:
                        if not line.strip().startswith('<?xml'):
                            f.write(line)
        
        f.write('</addons>\n')
    
    print(f"Created: {addons_xml_path}")
    
    # Create MD5 checksum
    md5_path = addons_xml_path + '.md5'
    with open(addons_xml_path, 'rb') as f:
        md5_hash = hashlib.md5(f.read()).hexdigest()
    
    with open(md5_path, 'w') as f:
        f.write(md5_hash)
    
    print(f"Created: {md5_path}")

def main():
    # Paths
    base_dir = Path(__file__).parent
    flixkodi_dir = base_dir / 'FlixKodi'
    zips_dir = base_dir / 'zips'
    
    # Create zips directory structure
    repo_zip_dir = zips_dir / 'repository.flixkodi'
    wizard_zip_dir = zips_dir / 'plugin.program.flixwizard'
    flixgen_zip_dir = zips_dir / 'plugin.program.flixgen'
    balkan_zip_dir = zips_dir / 'plugin.video.flixbalkan'
    stalker_zip_dir = zips_dir / 'plugin.video.flixstalker'
    resolveurl_zip_dir = zips_dir / 'script.module.resolveurl'
    
    repo_zip_dir.mkdir(parents=True, exist_ok=True)
    wizard_zip_dir.mkdir(parents=True, exist_ok=True)
    flixgen_zip_dir.mkdir(parents=True, exist_ok=True)
    balkan_zip_dir.mkdir(parents=True, exist_ok=True)
    stalker_zip_dir.mkdir(parents=True, exist_ok=True)
    resolveurl_zip_dir.mkdir(parents=True, exist_ok=True)
    
    # Create repository zip
    repo_source = flixkodi_dir / 'repository.flixkodi'
    create_addon_zip(
        str(repo_source),
        str(repo_zip_dir),
        'repository.flixkodi',
        '1.0.2'
    )
    
    # Create wizard zip
    wizard_source = flixkodi_dir / 'plugin.program.flixwizard'
    create_addon_zip(
        str(wizard_source),
        str(wizard_zip_dir),
        'plugin.program.flixwizard',
        '1.0.0'
    )
    
    # Create FlixGen zip
    flixgen_source = flixkodi_dir / 'plugin.program.flixgen'
    create_addon_zip(
        str(flixgen_source),
        str(flixgen_zip_dir),
        'plugin.program.flixgen',
        '1.0.0'
    )
    
    # Create FlixBalkan zip
    balkan_source = flixkodi_dir / 'plugin.video.flixbalkan'
    create_addon_zip(
        str(balkan_source),
        str(balkan_zip_dir),
        'plugin.video.flixbalkan',
        '2.0.0'
    )
    
    # Create FlixStalker zip
    stalker_source = flixkodi_dir / 'plugin.video.flixstalker'
    create_addon_zip(
        str(stalker_source),
        str(stalker_zip_dir),
        'plugin.video.flixstalker',
        '1.0.1'
    )
    
    # Create ResolveURL zip
    resolveurl_source = flixkodi_dir / 'script.module.resolveurl'
    create_addon_zip(
        str(resolveurl_source),
        str(resolveurl_zip_dir),
        'script.module.resolveurl',
        '5.1.185'
    )
    
    # Copy addon.xml and icon.png to zip directories
    import shutil
    
    # Repository files
    shutil.copy(repo_source / 'addon.xml', repo_zip_dir / 'addon.xml')
    shutil.copy(repo_source / 'icon.png', repo_zip_dir / 'icon.png')
    
    # Wizard files
    shutil.copy(wizard_source / 'addon.xml', wizard_zip_dir / 'addon.xml')
    shutil.copy(wizard_source / 'icon.png', wizard_zip_dir / 'icon.png')
    
    # FlixGen files
    shutil.copy(flixgen_source / 'addon.xml', flixgen_zip_dir / 'addon.xml')
    if (flixgen_source / 'icon.png').exists():
        shutil.copy(flixgen_source / 'icon.png', flixgen_zip_dir / 'icon.png')
    
    # FlixBalkan files
    shutil.copy(balkan_source / 'addon.xml', balkan_zip_dir / 'addon.xml')
    if (balkan_source / 'icon.png').exists():
        shutil.copy(balkan_source / 'icon.png', balkan_zip_dir / 'icon.png')
    
    # FlixStalker files
    shutil.copy(stalker_source / 'addon.xml', stalker_zip_dir / 'addon.xml')
    if (stalker_source / 'icon.png').exists():
        shutil.copy(stalker_source / 'icon.png', stalker_zip_dir / 'icon.png')
    
    # ResolveURL files
    shutil.copy(resolveurl_source / 'addon.xml', resolveurl_zip_dir / 'addon.xml')
    if (resolveurl_source / 'icon.png').exists():
        shutil.copy(resolveurl_source / 'icon.png', resolveurl_zip_dir / 'icon.png')
    
    # Create addons.xml
    create_addons_xml(
        str(zips_dir),
        [str(repo_source), str(wizard_source), str(flixgen_source), str(balkan_source), str(stalker_source), str(resolveurl_source)]
    )
    
    print("\nAll done! Upload the 'zips' folder to GitHub.")

if __name__ == '__main__':
    main()
