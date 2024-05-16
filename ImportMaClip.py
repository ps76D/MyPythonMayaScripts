import os
import maya.mel as mel
import maya.cmds as cmds

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

# Укажите путь к вашему .ma файлу
clip_file_path = "C:/Users/HYPERPC/YandexDisk/MyProjects/ProjectX/Models/Anims/FaceAnim/Emo/Emo_SlySmile.ma"

# Импортируем клип в Time Editor
import_ma_clip_into_time_editor(clip_file_path)



