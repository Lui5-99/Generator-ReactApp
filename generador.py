import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

contenido_tailwind_js = """
/** @type {import('tailwindcss').Config} */
export default {
  content: ["index.html", "src/**/*.{vue,js,ts,jsx,tsx}", "public/index.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""

contenido_index = """
import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="bg-black h-screen flex flex-col justify-center items-center text-white text-center gap-y-4">
      <div className="flex">
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="h-20 w-auto" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank" className="animate-spin">
          <img src={reactLogo} className="h-20 w-auto" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div>
        <button
          className="bg-teal-500 rounded-lg px-4 py-2 text-white font-semibold"
          onClick={() => setCount((count) => count + 1)}
        >
          count is {count}
        </button>
        <p className="mt-2">
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <p>Powered by Ing. Software Luis Arellano</p>
    </div>
  );
}

export default App;

"""

def select_path():
  path = filedialog.askdirectory()
  entry_path.delete(0, tk.END)
  entry_path.insert(0, path)

def set_name_project(name_project):
  name_project = name_project.lower()
  # If name project contains spaces, replace them with underscores
  name_project = name_project.replace(" ", "_")

  # if name is only one point(.), (-), (_) or (/), asign name to project_react
  if name_project in [".", "-", "_", "/"]:
    name_project = "project_react"
  return name_project

def generator_react(name_project, path):
  name_project = set_name_project(name_project)
  
  os.chdir(path)

  #Create folder with name project
  os.makedirs(name_project, exist_ok=True)
  os.chdir(name_project)

  # Verify if node is installed in the system if not, install it, depending on the OS
  try:
    subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  except FileNotFoundError:
    messagebox.showinfo("Info", "Node is not installed in the system. Please install it.")
    return
  
  command_create_project = f"npm create vite@latest . -- --template react && npm install && exit" 

  # Execute commands
  subprocess.run(command_create_project, shell=True)

  messagebox.showinfo("Info", "Project created successfully, please configure Tailwind")

def configure_tailwind(path, name_project):
  name_project = set_name_project(name_project)

  os.chdir(path)
  os.chdir(name_project)

  command_install_tailwind =  "npm install -D tailwindcss@latest postcss@latest autoprefixer@latest"
  command_install_tailwind_cli = "npx tailwindcss init -p"
  command_open_vscode = "code ."

  # Execute commands
  subprocess.run(command_install_tailwind, shell=True)
  subprocess.run(command_install_tailwind_cli, shell=True)

  if os.path.exists("tailwind.config.js"):
    # Open file in write mode
    with open("tailwind.config.js", "w") as file:
      # Delete the content of the file
      file.truncate(0)
      # Write the content of the file
      file.write(contenido_tailwind_js)
  else:
    # create file tailwind.config.js
    with open("tailwind.config.js", "w") as file:
      file.write(contenido_tailwind_js)
  
  os.chdir("src")

  if(os.path.exists("App.css")):
    with open("App.css", "w") as file:
      file.truncate(0)
      file.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")

  if(os.path.exists("index.css")):
    with open("index.css", "w") as file:
      file.truncate(0)

  if(os.path.exists("App.jsx")):
    with open("App.jsx", "w") as file:
      file.truncate(0)
      file.write(contenido_index)

  messagebox.showinfo("Info", "Tailwind configured successfully")
  os.chdir(path + "/" + name_project)
  subprocess.run(command_open_vscode, shell=True)


# Function to generate the project
def create_project():
  path = entry_path.get()
  # Check if the path is empty
  if path == '':
    messagebox.showerror('Error', 'Select a path')
    return
  name_project = entry_name.get()
  # Check if the name is empty
  if name_project == '':
    messagebox.showerror('Error', 'Enter a project name')
    return
  generator_react(name_project, path)

# Create a main window
window = tk.Tk()
window.title("React Generator")
window.geometry("400x400")
# Label and Entry for path
label_path = tk.Label(window, text='Path:')
label_path.pack(pady=5)
entry_path = tk.Entry(window)
entry_path.pack(pady=5)
button_path = tk.Button(window, text='Select path', command=select_path)
button_path.pack(pady=5)

# Label and Entry for project name
label_name = tk.Label(window, text='Project name:')
label_name.pack(pady=5)
entry_name = tk.Entry(window)
entry_name.pack(pady=5)

# Button to generate project
button_create = tk.Button(window, text='Generate project', command=create_project)
button_create.pack(pady=20)

# Button to configure tailwind
button_tailwind = tk.Button(window, text='Configure Tailwind', command=lambda: configure_tailwind(entry_path.get(), entry_name.get()))
button_tailwind.pack(pady=20)

# Show windows where appear the messages
window.withdraw()

# show window where indicate thats working in the background
window.deiconify()

# Run the main loop
window.mainloop()