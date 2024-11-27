import glob
import os
import sqlite3
import xbmc
import xbmcaddon
from xbmc import log
from xml.dom.minidom import parse
from .addonvar import addons_path, addons_db, installed_date

addon_xmls = []

def enable_addons():
    for name in glob.glob(os.path.join(addons_path,'*/addon.xml')):
        addon_xmls.append(name)
    addon_xmls.sort()
    addon_ids =[]
    for xml in addon_xmls:
        try:
            root = parse(xml)
            tag = root.documentElement
            _id = tag.getAttribute('id')
            addon_ids.append(_id)
        except:
            pass
    habilitados = []
    deshabilitados = []
    for x in addon_ids:
        try:
            xbmcaddon.Addon(id = x)
            habilitados.append(x)
        except:
            deshabilitados.append(x)
    for y in deshabilitados:
        try:
            enable_db(y)
        except:
            pass
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('UpdateAddonRepos')
    
def enable_db(d_addon):
    """ crea una conexión a una base de datos SQLite """
    conn = None
    conn = sqlite3.connect(addons_db)
    c = conn.cursor()
    try:
        c.execute("SELECT id, addonID, enabled FROM installed WHERE addonID = ?", (d_addon,))
        encontrado = c.fetchone()
        if encontrado == None:
            # Insertar una fila de datos
            c.execute('INSERT INTO installed (addonID , enabled, installDate) VALUES (?,?,?)', (d_addon, '1', installed_date))
        else:
            c.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (1, d_addon,))
    except Exception as e:
        log('No se pudo habilitar %s. Razón: %s' % (d_addon, e), xbmc.LOGINFO)
    conn.commit()
    conn.close()
