import os
import maya.cmds as cmds

global winWidth

global get_name
global get_file_prefix
global get_main_path
global getfilepath

global item_list_control
global item_list

global textFieldButtonGrp

global layoutButtons

button_list = []



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


def export_method():
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


def reset_path_button():
    set_folder_path_to_text_field()
    cmds.layout(layoutButtons, edit=True)
    update_list_contents()
    #reset_path()
    #cmds.textFieldGrp('PathField', edit=True, text = filepath)


def set_folder_path_to_text_field():
    global getfilepath
    # Открываем диалоговое окно проводника для выбора папки
    selected_folder = cmds.fileDialog2(dialogStyle=2, fileMode=3)
    if selected_folder:
        # Если папка выбрана, устанавливаем ее как текст в textFieldGrp
        cmds.textFieldButtonGrp(textFieldButtonGrp, edit=True, text=selected_folder[0])
    filepath = selected_folder[0]


# Функция для получения списка файлов .mb в указанном каталоге
def get_mb_files(directory):
    mb_files = []
    for file in os.listdir(directory):
        if file.endswith(".mb"):
            mb_files.append(file)
    return mb_files


# Функция для создания окна с списком файлов
def create_window():
    global get_file_prefix
    global textFieldButtonGrp
    global button_list
    global layoutButtons
    
    winWidth  = 500
    
    window_title = "Exporter"

    if cmds.window(window_title, exists=True):
        cmds.deleteUI(window_title, window=True)

    exporter_window = cmds.window(title="Anim Exporter", width = winWidth, sizeable=True)
    
    mainCL = cmds.columnLayout()
    cmds.text(label='Current Scene Block')

    #tmpThreeRowWidth = [winWidth*0.4, winWidth*0.6]
    
    #layout1 = cmds.rowLayout(nc=2, columnWidth2=tmpThreeRowWidth)
    
    #cmds.text(label = "Префикс для файла Name@", width=tmpThreeRowWidth[0])
    cmds.textFieldGrp('PrefixField', label='Префикс Name@', text = "HeadBase@", width=winWidth)
    
    #cmds.setParent('..')
    
    #layout2 = cmds.rowLayout(nc=2, columnWidth2=tmpThreeRowWidth)

    reset_path()
    #cmds.button(label = "Set dir", command = reset_path_button, width=tmpThreeRowWidth[0])
    tmpWidth = [winWidth*0.3, winWidth*0.5, winWidth*0.2]
    textFieldButtonGrp  = cmds.textFieldButtonGrp(label='PathField', text = getfilepath, width=winWidth, columnWidth3=tmpWidth, buttonLabel='Set dir', buttonCommand = reset_path_button)

    cmds.button(label = "Export Current Scene", command = lambda x: export_method(), width=winWidth)

    cmds.text(label='')
    cmds.text(label='Batch Export Block')
    cmds.text(label='Click on button to open and export file')
    
    tmpTwoRowWidth = [winWidth*0.5, winWidth*0.5]

    layoutButtons = cmds.columnLayout(adjustableColumn=True, columnWidth=winWidth)
    
    global item_list_control
    update_list_contents()
            
    cmds.setParent('..')

    cmds.text(label='')

    cmds.button(label = "Batch Export All Files in Folder", command=lambda x: batch_export_all_files_in_folder_method(), width=winWidth, height=80)

    cmds.text(label='')
    cmds.text(label='')

    cmds.showWindow(exporter_window)


def update_list_contents(*args):
    print("NewPath: " + getfilepath)
    global winWidth

    winWidth = 500
    get_item_list = get_mb_files(getfilepath)
    print(get_item_list)

    children = cmds.columnLayout(layoutButtons, query=True, childArray=True)
    if children:
        cmds.deleteUI(children)
        
    if get_item_list:       
        for file in get_item_list:
            button = cmds.button(label=file, parent=layoutButtons, width=winWidth, command=lambda x: export_filename_method(file))
            button_list.append(button)
    else:
        cmds.text(label="No .mb files found in directory.")


def load_file(file_name):
    file_path = os.path.join(getfilepath, file_name)
    if os.path.exists(file_path):
        cmds.file(file_path, open=True, force=True)
    else:
        print("File not found:", file_name)


def export_filename_method(value):
    load_file(value)
    export_method_for_batch()


def batch_export_all_files_in_folder_method():
    if button_list:
        for button in button_list:
            file = cmds.button(button, query=True, label=True)
            print(file)
            export_filename_method(file)
            
            
def export_method_for_batch():
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
    
    
create_window()