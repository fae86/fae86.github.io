import xbmc
import xbmcgui
import shutil
import os
import zipfile
from zipfile import ZipFile
from pathlib import Path
from .addonvar import home, addon_profile, addon_path, setting, setting_set, translatePath, xbmcPath, addon_id, dp, local_string, addon_name, addon_icon, addon_fanart
from .utils import add_dir

p = Path(home)
backup_path = Path(translatePath(setting('backupfolder')))
backups = p / 'backups'
addons = p / 'addons'
media = p / 'media'
userdata = p / 'userdata'
wizard_path = Path(addon_path)
data_path = Path(addon_profile)
compression = zipfile.ZIP_DEFLATED

def log(_text, _var):
    xbmc.log(f'{_text} = {str(_var)}', xbmc.LOGINFO)

excludes = [p / 'addons/packages', p / 'addons/temp', p / 'userdata/Thumbnails', p / 'userdata/Database/Textures13.db', p / wizard_path]

def from_keyboard():
    kb = xbmc.Keyboard('', 'Ingrese el nombre del respaldo', False)
    kb.doModal()
    if (kb.isConfirmed()):
        return kb.getText()
    else:
        return False

def backup_build():
    backup_path.mkdir(parents=True, exist_ok=True)
    k = from_keyboard()
    if k is False:
        return xbmcgui.Dialog().ok('Respaldo', 'Respaldo cancelado')
    else:
        backup_name = backup_path / f'{k}.zip'
        
    addons_dirs, addons_files = ([x for x in addons.iterdir() if x.is_dir() and x not in excludes]), ([x for x in addons.iterdir() if x.is_file() and x not in excludes])

    media_dirs, media_files = ([x for x in media.iterdir() if x.is_dir() and x not in excludes]), ([x for x in media.iterdir() if x.is_file() and x not in excludes])

    userdata_dirs, userdata_files = ([x for x in userdata.iterdir() if x.is_dir() and x not in excludes]), ([x for x in userdata.iterdir() if x.is_file() and x not in excludes])
    
    zip_file = ZipFile(backup_name, 'w')
    xbmcgui.Dialog().notification(addon_name, 'Respaldo en progreso, por favor espere!', addon_icon, 3000)
    for x in sorted(addons_dirs):
        for z in sorted([y for y in x.rglob('*') if y not in excludes]):
            if '__pycache__' not in str(z):
                zip_file.write(z, str(z.relative_to(p)), compress_type=compression)
    for x in sorted(addons_files):
        zip_file.write(x, str(x.relative_to(p)), compress_type=compression)
    
    for x in sorted(media_dirs):
        for z in sorted([y for y in x.rglob('*') if y not in excludes]):
            zip_file.write(z, str(z.relative_to(p)), compress_type=compression)
    for x in sorted(media_files):
        zip_file.write(x, str(x.relative_to(p)), compress_type=compression)

    for x in sorted(userdata_dirs):
        for z in sorted([y for y in x.rglob('*') if y not in excludes]):
            zip_file.write(z, str(z.relative_to(p)), compress_type=compression)
    for x in sorted(userdata_files):
        zip_file.write(x, str(x.relative_to(p)), compress_type=compression)    
    zip_file.close()
    xbmcgui.Dialog().ok('Respaldo', 'Respaldo completo')

excludes_freshstart = [addon_id, 'backups',  'Addons33.db', 'kodi.log']

def fresh_start_restore():
    for root, dirs, files in os.walk(xbmcPath, topdown=True):
        dirs[:] = [d for d in dirs if d not in excludes_freshstart]
        for name in files:
            if name not in excludes_freshstart:
                try:
                    os.unlink(os.path.join(root, name))
                except:
                    log('Error al eliminar', name)
                    
    for root, dirs, files in os.walk(xbmcPath, topdown=True):
        dirs[:] = [d for d in dirs if d not in excludes_freshstart]
        for name in dirs:
            if name not in ['addons', 'userdata', 'Database', 'addon_data', 'backups', 'temp']:
                try:
                    shutil.rmtree(os.path.join(root, name), ignore_errors=True, onerror=None)
                except:
                    log('Error al eliminar', name)

def get_backup_folder():
    dialog = xbmcgui.Dialog()
    fn = dialog.browseSingle(0, 'Kodi', 'local', '', False, False)
    setting_set('backupfolder', fn)

def reset_backup_folder():
    setting_set('backupfolder', 'special://home/backups')
    xbmcgui.Dialog().ok('Carpeta de respaldo', 'Ubicación de la carpeta de respaldo\nRestablecida a predeterminada')

def restore_menu():
    build_backups = ([x for x in backup_path.iterdir() if x.is_file() and str(x).endswith('.zip')])
    for build in build_backups:
        add_dir(str(build.stem), str(build), 15, addon_icon, addon_fanart, str(build.name), isFolder=False)

def restore_build(zippath):
    restore = xbmcgui.Dialog().yesno('Restaurar', '¿Está seguro de que desea borrar \nlos datos actuales y restaurar desde el respaldo?')
    if restore is True:
        fresh_start_restore()
        if os.path.exists(zippath):
            dp.create('Restaurar', local_string(30034))  # Extrayendo archivos
            dp.update(66, local_string(30034))
            zf = ZipFile(zippath)
            zf.extractall(path=home)
            dp.update(100, local_string(30035))  # Extracción completa
            zf.close()
            xbmcgui.Dialog().ok('Restaurar', 'Restauración completa')
            setting_set('firstrun', 'true')
            os._exit(1)
        else:
            xbmcgui.Dialog().ok('Restaurar', 'Respaldo no encontrado')
    else:
        return False
