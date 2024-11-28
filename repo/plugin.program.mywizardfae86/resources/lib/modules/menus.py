import sys
import json
import xbmc
import xbmcplugin
import os
from .addonvar import addon_name
from .utils import add_dir
from .parser import Parser
from .dropbox import DownloadFile
from uservar import buildfile
from .addonvar import addon_icon, addon_fanart, local_string, build_file, authorize
from .colors import colors

# Ruta del script actual
current_path = os.path.dirname(__file__)  
icon_path = os.path.join(current_path, "Icon")  # Carpeta Icon

HANDLE = int(sys.argv[1])
COLOR1 = colors.color_text1
COLOR2 = colors.color_text2

def main_menu():
    xbmcplugin.setPluginCategory(HANDLE, COLOR1('Menú Principal'))
    
    # Menú principal con su ícono
    add_dir(COLOR1(f'Bienvenido a {addon_name}'), '', '', 
            os.path.join(icon_path, "bienvenido.png"),  # Ruta al ícono
            addon_fanart, COLOR1(f'***Bienvenido a {addon_name}***'), isFolder=False)
    
    # Menú de Builds con su ícono
    add_dir(COLOR2(local_string(30010)), '', 1, 
            os.path.join(icon_path, "builds.png"),  # Ruta al ícono
            addon_fanart, COLOR2(local_string(30001)), isFolder=True)
    
    # Menú de Mantenimiento con su ícono
    add_dir(COLOR2(local_string(30011)), '', 5, 
            os.path.join(icon_path, "mantenimiento.png"),  # Ruta al ícono
            addon_fanart, COLOR2(local_string(30002)), isFolder=True)
    
    # Configuración con su ícono
    add_dir(COLOR2(local_string(30015)), '', 9, 
            os.path.join(icon_path, "configuracion.png"),  # Ruta al ícono
            addon_fanart, COLOR2(local_string(30016)), isFolder=False)

    # Finalizar la creación de la lista de directorios
    xbmcplugin.endOfDirectory(HANDLE)

def build_menu():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    xbmcplugin.setPluginCategory(HANDLE, local_string(30010))
    if buildfile.startswith('https://www.dropbox.com'):
        DownloadFile(buildfile, build_file)
        try:
            builds = json.load(open(build_file,'r')).get('builds')
        except:
            xml = Parser(build_file)
            builds = json.loads(xml.get_list2())['builds']
    elif not buildfile.endswith('.xml') and not buildfile.endswith('.json'):
        add_dir(local_string(30017),'','',addon_icon,addon_fanart,local_string(30017),isFolder=False)  # URL de Build Inválida
        return
    else:
        p = Parser(buildfile)
        builds = json.loads(p.get_list())['builds']
    
    for build in builds:
        name = (build.get('name', local_string(30018)))  # Nombre Desconocido
        version = (build.get('version', '0'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        description = (build.get('description', local_string(30019)))  # Descripción No Disponible
        preview = (build.get('preview',None))
        
        if url.endswith('.xml') or url.endswith('.json'):
            add_dir(COLOR2(name),url,1,icon,fanart,COLOR2(description),name2=name,version=version,isFolder=True)
        add_dir(COLOR2(f'{name} {local_string(30020)} {version}'), url, 3, icon, fanart, description, name2=name, version=version, isFolder=False)  # Versión
        if preview is not None:
            add_dir(COLOR1(local_string(30021) + ' ' + name + ' ' + local_string(30020) + ' ' + version), preview, 2, icon, fanart, COLOR2(description), name2=name, version=version, isFolder=False)  # Vista previa del video

def submenu_maintenance():
    xbmcplugin.setPluginCategory(HANDLE, COLOR1(local_string(30022)))  # Mantenimiento
    
    # Enlazar cada menú con su icono
    add_dir(COLOR1('Mantenimiento'), '', '', 
            os.path.join(icon_path, "mantenimiento.png"), 
            addon_fanart, COLOR1('***Mantenimiento***'), isFolder=False)
    
    add_dir(COLOR2(local_string(30023)), '', 6, 
            os.path.join(icon_path, "limpiar_paquetes.png"), 
            addon_fanart, COLOR1(local_string(30005)), isFolder=False)  # Limpiar Paquetes
    
    add_dir(COLOR2(local_string(30024)), '', 7, 
            os.path.join(icon_path, "limpiar_miniaturas.png"), 
            addon_fanart, COLOR2(local_string(30008)), isFolder=False)  # Limpiar Miniaturas
    
    add_dir(COLOR2(local_string(30012)), '', 4, 
            os.path.join(icon_path, "restaurar_configuracion.png"), 
            addon_fanart, COLOR2(local_string(30003)), isFolder=False)  # Restaurar Configuración
    
    add_dir(COLOR2(local_string(30025)), '', 8, 
            os.path.join(icon_path, "configuracion_avanzada.png"), 
            addon_fanart, COLOR2(local_string(30009)), isFolder=False)  # Configuración Avanzada
    
    add_dir(COLOR2(local_string(30064)), '', 11, 
            os.path.join(icon_path, "editar_whitelist.png"), 
            addon_fanart, COLOR2(local_string(30064)), isFolder=False)  # Editar Whitelist
    
    add_dir(COLOR2('Restaurar GUI/Skin'), '', 19, 
            os.path.join(icon_path, "restaurar_gui.png"), 
            addon_fanart, COLOR2('Restaurar Configuración GUI y Skin'))
    
    add_dir(COLOR2('Cerrar Kody'), '', 18, 
            os.path.join(icon_path, "cerrar_forzado.png"), 
            addon_fanart, COLOR2('Cerrar Forzadamente Kodi'))
    
    add_dir(COLOR2('Test Velocidad'), '', 27, 
            os.path.join(icon_path, "prueba_velocidad.png"), 
            addon_fanart, COLOR2('Prueba de Velocidad'), isFolder=False)

def authorize_menu():  ### deprecated use authorize.py methods
    xbmcplugin.setPluginCategory(HANDLE, local_string(30027))  # Autorizar Servicios
    p = Parser(authorize)
    builds = json.loads(p.get_list())['items']
    for build in builds:
        name = (build.get('name', 'Desconocido'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        add_dir(name,url,2,icon,fanart,name,name2=name,version='' ,isFolder=False)
