import os
import maya.cmds as cmds

global get_name
global get_file_prefix
global get_main_path
global getfilepath

    
def import_reference():  
    all_ref_paths = cmds.file(q = True, reference = True) or []  # Get a list of all top-level references in the scene.
    for ref_path in all_ref_paths:
        if cmds.referenceQuery(ref_path, isLoaded = True):  # Only import it if it's loaded, otherwise it would throw an error.
            cmds.file(ref_path, importReference = True)  # Import the reference.


def remove_namespaces():
    all_nodes = cmds.ls () # get everything!
    all_namespaces = []

    for node in all_nodes:
        if ':' in node: # check out for namespaces
            if node.split(':')[0] not in all_namespaces:
                all_namespaces.append(node.split(':')[0]) #only keep the name space name once

    for curNamespace in all_namespaces: # look through the namespaces
        cmds.namespace( removeNamespace = curNamespace, mergeNamespaceWithRoot = True) # remove the namespace and merge with root because the namespace won't be empty generally


def bake_keys():
    cmds.select( 'root' )
    start_frame = cmds.playbackOptions(q = 1, min = 1)
    end_frame = cmds.playbackOptions(q = 1, max = 1)
    cmds.bakeResults(sm = True, t = (start_frame, end_frame), hi = "below")
    cmds.parent( 'root', world = True )
    
    
def delete_all_unnecessary():
    cmds.select( 'Group' )
    cmds.delete()


def prepare_to_export():
    import_reference()
    remove_namespaces()
    bake_keys()
    delete_all_unnecessary()
    

def get_file_name():
    filename = cmds.file(q = True, sn = True, shn = True)
    raw_name, extension = os.path.splitext(filename)
    return raw_name


def get_prefix():
    #prefix_name = cmds.textFieldGrp(label = "", text = "HeadBase@")
    prefix_name = cmds.textFieldGrp( 'PrefixField', query = True, text = True)

    return str(prefix_name)


def get_save_name_path(name, prefix):
    global get_main_path
    #export_path = "C:/Users/HYPERPC/YandexDisk/MyProjects/ProjectX/Test"
    export_path = getfilepath
    main_path = export_path + "/" + prefix + name + ".fbx"
    get_main_path = main_path
        
        
def export(path):
    cmds.select( 'root' )
    
    cmds.file(path, force=True, options="v=0;", typ="FBX export", pr=True, es=True)


def export_method(args):
    global get_name
    global get_file_prefix
    global get_main_path

    prepare_to_export()

    get_name = get_file_name()

    get_file_prefix = get_prefix()

    print("get_file_prefix: " + get_file_prefix)

    get_save_name_path(get_name, get_file_prefix)
    
    print("Export to: " + get_main_path)
    export(get_main_path)

def reset_path():
    global getfilepath
    filename = cmds.file(q = True, sn = True)
    head = os.path.dirname(filename)
    print("head: " + head)
    filepath = head


def reset_path_button(args):
    set_folder_path_to_text_field()
    #reset_path()
    #cmds.textFieldGrp('PathField', edit=True, text = filepath)


def set_folder_path_to_text_field():
    global getfilepath
    # Открываем диалоговое окно проводника для выбора папки
    selected_folder = cmds.fileDialog2(dialogStyle=2, fileMode=3)
    if selected_folder:
        # Если папка выбрана, устанавливаем ее как текст в textFieldGrp
        cmds.textFieldGrp('PathField', edit=True, text=selected_folder[0])
    filepath = selected_folder[0]

    
def show_ui():
    global get_file_prefix
    exporter_window = cmds.window(title="Anim Exporter", widthHeight = (650,200))

    layout1 = cmds.rowColumnLayout(nc=3, columnWidth=[(1, 200), (2, 250), (3, 200)])
    
    cmds.text(label = "   ", parent=layout1)
    cmds.text(label = "   ", parent=layout1)
    cmds.text(label = "   ", parent=layout1)
    
    cmds.text(label = "Введите префикс для имени файла Name@", parent=layout1)
    cmds.textFieldGrp('PrefixField', text = "HeadBase@", parent=layout1)
    cmds.text(label = "   ", parent=layout1)
    
    cmds.text(label = "   ", parent=layout1)
    cmds.text(label = "   ", parent=layout1)
    cmds.text(label = "   ", parent=layout1)
    
    #layout2 = cmds.rowColumnLayout(nc=3, columnWidth=[(1, 400), (2, 400), (3, 400)])
    cmds.text(label = "Путь папки экспорта", parent=layout1)
    reset_path()
    cmds.textFieldGrp('PathField', text = getfilepath, parent=layout1)
    cmds.button(label = "Set dir", command = reset_path_button, parent=layout1)

    cmds.text(label = "   ", parent=layout1)
    cmds.text(label = "   ", parent=layout1)
    cmds.text(label = "   ", parent=layout1)
    cmds.text(label = "   ", parent=layout1)
    cmds.button(label = "Export", command = export_method, parent=layout1)
    cmds.text(label = "   ", parent=layout1)

    cmds.showWindow(exporter_window)
    
show_ui()


