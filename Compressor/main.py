import PySimpleGUI as sg
import compressor

label1 = sg.Text("Select files to compress")
label2 = sg.Text("Select destination folder")

input1 = sg.Input()
input2 = sg.Input()

sg.theme("black")
choose_box1 = sg.FilesBrowse("Choose",key="filechoose")
choose_box2 = sg.FolderBrowse("Choose",key="folderchoose")
button = sg.Button(button_text="Compress")
output_label = sg.Text(key="output")
exit_button = sg.Button("Exit",key="exit")

window = sg.Window("File Zipper",
                   layout=[[label1,input1,choose_box1],[label2,input2,choose_box2],[button, output_label,exit_button]])


while True:
    event, values = window.read()
    # print(event, type(values["filechoose"]))
    # print(event, type(values["folderchoose"]))
    # if event == sg.WIN_CLOSED or event == "exit":
    #     break
    filepaths = values["filechoose"].split(';')
    folderpath = values["folderchoose"]
    print(len(filepaths), len(folderpath))
    
    if event == 'Compress': 
        if len(filepaths)>=1 and len(folderpath)!=0:
            compressor.make_archive(filepaths=filepaths,dest_dir=folderpath)# if user closes window or clicks cancel
            print("Compressed")
            window["output"].update("Compression is finished")
    elif event == "exit":
        break

window.close()

