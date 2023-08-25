import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import subprocess

root = tk.Tk()
root.title("Gnuplot Script Editor")
dynamicEntryWidgets = []


def launch_gnuplot(script_file):
    # Launch Gnuplot in a separate process and detach it
    subprocess.Popen(['gnuplot', script_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False)


def chooseScriptFile():
    global gnuplotScriptFile
    gnuplotScriptFile = filedialog.askopenfilename(filetypes=[("Gnuplot Script", "*.gp")])
    if gnuplotScriptFile:
        script_name = os.path.basename(gnuplotScriptFile)
        currentScriptLabel.config(text=script_name)
        # root.title(script_name)


def updateScript():
    # Get the new variables and call edit_gnuplot_script
    new_variables = {}
    for i in range(1, len(dynamicEntryWidgets), 4):
        variable = dynamicEntryWidgets[i].get()
        value = dynamicEntryWidgets[i+2].get()
        new_variables[variable] = value

    if gnuplotScriptFile:
        script_content = None
        with open(gnuplotScriptFile, 'r') as file:
            script_content = file.read()

        for variable_name in new_variables.keys():
            if variable_name not in script_content:
                messagebox.showerror("Variable Not Found", "Variable '{}' not found in script.".format(variable_name))    
                return
            
        new_script_file = edit_gnuplot_script(gnuplotScriptFile, new_variables)
        messagebox.showinfo("Script Updated", "The script has been updated. Modified script file: {}".format(new_script_file))    
        # new_script_file = edit_gnuplot_script(gnuplotScriptFile, new_variables)
        # messagebox.showinfo("Script Updated", "The script has been updated. Modified script file: {}".format(new_script_file))


def edit_gnuplot_script(script_file, new_variables):
    # Read the contents of the Gnuplot script
    with open(script_file, 'r') as file:
        script_content = file.read()

    # Make the necessary modifications to the script content
    modified_script_content = script_content
    for variable_name, new_value in new_variables.items():
        pattern = r'(?<!#)\b{}=(\d+\.\d+)\n'.format(variable_name)
        modified_script_content = re.sub(pattern, '{}={}\n'.format(variable_name, new_value), modified_script_content)

    # Write the modified content to a new script file
    new_script_file = os.path.splitext(script_file)[0] + "_modified.gp"
    with open(new_script_file, 'w') as file:
        file.write(modified_script_content)

    return new_script_file


def getPreviousVariable(script_content, variable_name):
    pattern = r'(?<!#)\b{}=(\d+\.\d+)\n'.format(variable_name)
    match = re.search(pattern, script_content)
    if match:
        return match.group(1)
    else:
        raise ValueError("{} value not found in script content.".format(variable_name))


def removeTextFieldPair():
    if len(dynamicEntryWidgets) >= 4:
        for _ in range(4):
            widget = dynamicEntryWidgets.pop()
            widget.destroy()


def addTextFieldPair():
    variableLabel = tk.Label(root, text="Variable:")
    variableLabel.pack(padx=10, pady=1)
    variableEntry = tk.Entry(root)
    variableEntry.pack(padx=10, pady=1)
    valueLabel = tk.Label(root, text="Value:")
    valueLabel.pack(padx=10, pady=1)
    valueEntry = tk.Entry(root)
    valueEntry.pack(padx=10, pady=1)

    dynamicEntryWidgets.extend([variableLabel, variableEntry, valueLabel, valueEntry])


def runScript():
    if gnuplotScriptFile:
        new_script_file = os.path.splitext(gnuplotScriptFile)[0] + "_modified.gp"
        print(new_script_file)
        launch_gnuplot(new_script_file)



# addLable = tk.Label(root, text="add new Pair of Text Fields")
# addLable.grid(row=0, column=0)

currentScriptLabel = tk.Label(root, text="Current Script")
currentScriptLabel.pack(padx=10, pady=10)
chooseButton = tk.Button(root, text="Choose Gnuplot Script", command=chooseScriptFile)
chooseButton.pack(side=tk.TOP , padx=10, pady=10)
addTextFieldPairButton = tk.Button(root, text="+", command=addTextFieldPair)
addTextFieldPairButton.pack(padx=10, pady=10)
removeTextFieldPairButton = tk.Button(root, text="-", command=removeTextFieldPair)
removeTextFieldPairButton.pack(padx=10, pady=10)
updateButton = tk.Button(root, text="Update", command=updateScript)
updateButton.pack(padx=10, pady=10)
runButton = tk.Button(root, text="Run", command=runScript)
runButton.pack(side=tk.TOP , padx=10, pady=10)



root.mainloop()
