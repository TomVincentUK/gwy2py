"""
Designed to be run from within Gwyddion's internal Python terminal.

Takes all map and volume data in all open files and saves them as
numpy .npy files.
"""
import gwy, gwyutils, os, numpy as np

# For all open files
for container in gwy.gwy_app_data_browser_get_containers():
    # Get the filename and directory
    fullPath = os.path.normpath(container['/filename'])
    directory, file = os.path.split(fullPath)
    fPref, fSuff = os.path.splitext(file)
    
    rootDir = os.path.join(directory, fPref + ' - numpy')
    if not os.path.exists(rootDir):
        os.makedirs(rootDir)
    
    # For all map data
    mTitle = 'Maps'
    mDir = os.path.join(rootDir, mTitle)
    for i in gwy.gwy_app_data_browser_get_data_ids(container):
        # Get map data and title
        data_field = container[gwy_app_get_data_key_for_id(i)]
        try:
            title = container[gwy_app_get_data_title_key_for_id(i)]
        except KeyError:
            title = 'Unknown channel {}'.format(i+1)
        
        # Convert to numpy array
        data_fieldArray = gwyutils.data_field_data_as_array(data_field)
        
        # Create 1D arrays corresponding to dimensions
        x = np.linspace(0, data_field.get_xreal(),
                        data_field.get_xres()) + data_field.get_xoffset()
        y = np.linspace(0, data_field.get_yreal(),
                        data_field.get_yres()) + data_field.get_yoffset()
        
        # Save files in Maps subdirectory
        if not os.path.exists(mDir):
            os.makedirs(mDir)
        np.save(os.path.join(mDir, title), data_fieldArray)
        np.save(os.path.join(mDir, title + ' - x'), x)
        np.save(os.path.join(mDir, title + ' - y'), y)
    
    # For all volume data
    vTitle = 'Volume'
    vDir = os.path.join(rootDir, vTitle)
    for i in gwy.gwy_app_data_browser_get_volume_ids(container):
        # Get data brick and title
        brick = container[gwy_app_get_brick_key_for_id(i)]
        try:
            title = container[gwy_app_get_brick_title_key_for_id(i)]
        except KeyError:
            title = 'Unknown channel {}'.format(i+1)
        
        # Convert to numpy array
        brickArray = gwyutils.brick_data_as_array(brick)
        
        # Create 1D arrays corresponding to dimensions
        x = np.linspace(0, brick.get_xreal(),
                        brick.get_xres()) + brick.get_xoffset()
        y = np.linspace(0, brick.get_yreal(),
                        brick.get_yres()) + brick.get_yoffset()
        z = gwyutils.data_line_data_as_array(brick.get_zcalibration())
        
        # Save files in Volume subdirectory
        if not os.path.exists(vDir):
            os.makedirs(vDir)
        np.save(os.path.join(vDir, title), brickArray)
        np.save(os.path.join(vDir, title + ' - x'), x)
        np.save(os.path.join(vDir, title + ' - y'), y)
        np.save(os.path.join(vDir, title + ' - z'), z)
