import os
import maya.cmds as cmds
import maya.mel as mel

global winWidth
global getfilepath
global export_to_filepath

global get_file_prefix
global prefixFieldGrp
global baseSceneFieldButtonGrp
global textFieldButtonGrp
global export_to_textFieldButtonGrp

global item_list_control

global layoutButtons

global file_path

global scene_name
global base_scene_path

button_list = []



def open_time_editor():
    # Открываем окно Time Editor через команды cmds
    if not cmds.window('timeEditorWindow', exists=True):
        cmds.TimeEditorWindow()


def import_ma_clip_into_time_editor(clip_file_path):
    try:
        raw_name, extension = os.path.splitext(clip_file_path)

        # Выполним MEL-скрипт для импорта клипа из файла .ma в Time Editor (не должно быть отличающихся неймспейсов в клипе и сцене!!!)
        #mel.eval(f'timeEditorClip -importOption connect -track "Composition1:0" -importMayaFile "{clip_file_path}" -startTime 0 "Emo_SlySmile"')
        cmds.timeEditorClip(raw_name, importOption="connect", track="Composition1:0", importMayaFile=clip_file_path, startTime=0)
        print("Clip and its Animation Source created.")
        print("The Time Editor now drives the clip's keyable attributes.")
    except Exception as e:
        print(f"Failed to import clip into Time Editor: {e}")


def bake_keys():
    cmds.select( 'root' )
    start_frame = cmds.playbackOptions(q = 1, min = 1)
    end_frame = cmds.playbackOptions(q = 1, max = 1)
    cmds.bakeResults(sm = True, t = (start_frame, end_frame), hi = "below")
    cmds.parent( 'root', world = True )


def delete_all_unnecessary():
    cmds.select( 'Group' )
    cmds.delete()


def prepare_to_export(clip_file_path):
    import_ma_clip_into_time_editor(clip_file_path)
    bake_keys()
    delete_all_unnecessary()


def reset_path():
    global getfilepath
    filename = cmds.file(q = True, sn = True)
    head = os.path.dirname(filename)
    print("head: " + head)
    getfilepath = head


def reset_path_button():
    set_folder_path_to_text_field()
    cmds.layout(layoutButtons, edit=True)
    update_list_contents()


def set_folder_path_to_text_field():
    global getfilepath
    # Открываем диалоговое окно проводника для выбора папки
    selected_folder = cmds.fileDialog2(dialogStyle=2, fileMode=3)
    if selected_folder:
        # Если папка выбрана, устанавливаем ее как текст в textFieldGrp
        cmds.textFieldButtonGrp(textFieldButtonGrp, edit=True, text=selected_folder[0])
    getfilepath = selected_folder[0]


def set_export_to_folder_path_to_text_field():
    global export_to_filepath
    # Открываем диалоговое окно проводника для выбора папки
    selected_folder = cmds.fileDialog2(dialogStyle=2, fileMode=3)
    if selected_folder:
        # Если папка выбрана, устанавливаем ее как текст в textFieldGrp
        cmds.textFieldButtonGrp(export_to_textFieldButtonGrp, edit=True, text=selected_folder[0])
    export_to_filepath = selected_folder[0]


def set_file_path_by_file(file):
    filepath = getfilepath + "/" + file
    return filepath


def make_lambda_for_button(arg):
    return lambda x: export_filename_method(arg)


def update_list_contents(*args):

    print("NewPath: " + getfilepath)
    global winWidth

    winWidth = 500
    get_item_list = get_ma_files(getfilepath)
    print(get_item_list)

    children = cmds.columnLayout(layoutButtons, query=True, childArray=True)
    if children:
        cmds.deleteUI(children)

    if get_item_list:
        for file in get_item_list:
            current_file_path=set_file_path_by_file(file)
            arg = current_file_path
            print(arg)
            button = cmds.button(label=file, parent=layoutButtons, width=winWidth, command=make_lambda_for_button(arg))
            button_list.append(button)
    else:
        cmds.text(label="No .mb files found in directory.")


def export(path):
    cmds.select( 'root' )

    cmds.file(path, force=True, options="v=0;", typ="FBX export", pr=True, es=True)
    

# Функция для получения списка файлов .mb в указанном каталоге
def get_ma_files(directory):
    ma_files = []
    if directory:
        for file in os.listdir(directory):
            if file.endswith(".ma"):
                ma_files.append(file)
    return ma_files


def get_file_name():
    filename = cmds.file(q = True, sn = True, shn = True)
    raw_name, extension = os.path.splitext(filename)
    return raw_name


def get_file():
    global scene_name
    base_scene_filename = cmds.file(q = True, sn = True, shn = True)
    scene_name = base_scene_filename
    return base_scene_filename

def get_current_scene_file_path():
    global base_scene_path
    path = cmds.file(q=True, sceneName=True)
    base_scene_path = path
        

def get_prefix():
    #prefix_name = cmds.textFieldGrp(label = "", text = "HeadBase@")
    prefix_name = cmds.textFieldGrp( 'PrefixField', query = True, text = True)

    return str(prefix_name)


def set_prefix(path):
    global get_file_prefix
    
    file_name_with_extension = os.path.basename(path)
    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
    combine_prefix = file_name_without_extension + "@"
    get_file_prefix = combine_prefix

def export_filename_method(value):
    global get_file_prefix
    #global get_main_path

    print("Get Clip and Export")
    print(value)
    prepare_to_export(value)

    file_name_with_extension = os.path.basename(value)
    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]

    print("get_name: " + file_name_without_extension)
    get_file_prefix = get_prefix()

    export_to = export_to_filepath + "/" + get_file_prefix + file_name_without_extension + ".fbx"
    print("Export to: " + export_to)
    export(export_to)


def batch_export_all_files_in_folder_method():
    get_item_list = get_ma_files(getfilepath)
    print(get_item_list)

    if get_item_list:
        for file in get_item_list:
            current_file_path=set_file_path_by_file(file)
            arg = current_file_path
            print(arg)
            export_filename_method(arg)
            reopen_scene()


def set_path_to_scene_base():
    global base_scene_path
    global get_file_prefix
    
    # Открываем диалоговое окно проводника для выбора папки
    selected_scene = cmds.fileDialog2(fileMode=1, dialogStyle=2, fm=1)
    if selected_scene:
        # Если папка выбрана, устанавливаем ее как текст в textFieldGrp
        cmds.textFieldButtonGrp(baseSceneFieldButtonGrp, edit=True, text=selected_scene[0])
        set_prefix(selected_scene[0])
        cmds.textFieldGrp(prefixFieldGrp, edit=True, text=get_file_prefix)
    base_scene_path = selected_scene[0]


def load_file(path):
    if os.path.exists(path):
        cmds.file(path, open=True, force=True)
        

def reopen_scene():
    load_file(base_scene_path)
    print(base_scene_path)


# Функция для создания окна с списком файлов
def create_window():
    global get_file_prefix
    global prefixFieldGrp
    global baseSceneFieldButtonGrp
    global textFieldButtonGrp
    global export_to_textFieldButtonGrp
    global button_list
    global layoutButtons
    global base_scene_path

    winWidth  = 500

    window_title = "Exporter"

    if cmds.window(window_title, exists=True):
        cmds.deleteUI(window_title, window=True)

    exporter_window = cmds.window(title="Anim Exporter", width = winWidth, sizeable=True)

    mainCL = cmds.columnLayout()
    cmds.text(label='Current Scene Block')



    #reset_path()

    tmpWidth = [winWidth*0.3, winWidth*0.5, winWidth*0.2]

    get_current_scene_file_path()
    baseSceneFieldButtonGrp  = cmds.textFieldButtonGrp(label='BaseScene', text = base_scene_path, width=winWidth, columnWidth3=tmpWidth, buttonLabel='Set base scene', buttonCommand = set_path_to_scene_base)
    set_prefix(base_scene_path)
    prefixFieldGrp = cmds.textFieldGrp('PrefixField', label='Префикс Name@', text =get_file_prefix, width=winWidth)
    
    cmds.text(label='')
    reset_path()
    textFieldButtonGrp  = cmds.textFieldButtonGrp(label='GetPathField', text = getfilepath, width=winWidth, columnWidth3=tmpWidth, buttonLabel='Dir to search', buttonCommand = reset_path_button)
    
    export_to_textFieldButtonGrp  = cmds.textFieldButtonGrp(label='SetExportPathField', text = getfilepath, width=winWidth, columnWidth3=tmpWidth, buttonLabel='Export to', buttonCommand = set_export_to_folder_path_to_text_field)

    cmds.text(label='')
    cmds.text(label='Batch Export Block')
    cmds.text(label='Click on button to import clip and export .fbx')

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


create_window()