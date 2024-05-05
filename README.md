# Assignment ProjectEGM722v2
# Elevation Profile Creator

input: Polygon shape file for the area of interest.  
outputs: Geotiff of the shapefile polygon area  
         PNG image file of the Geotiff file  
         CSV of the data generated to create the elevation profile from the geotiff  
         PNG image file of the generated elevation profile  
         PDF of the generated elevation profile 

A python script that creates an elevation profile between 2 user specified points, from a geotiff image generated from 
NASA earthdata for an area specified by a polygon shapefile.

The Python code, data files and repository can be accessed here: <http://github.com/KiriJB/ProjectEGM722v2>

Guide to setting up Anaconda with GitHub and creating an environment from an environment.yml file: 
## <a name="_toc165815484"></a>Install Anaconda: 
- Download and install Anaconda from the [[official website](https://www.anaconda.com/products/distribution)].
- Follow the installation instructions for your operating system. 
## <a name="_toc165815485"></a>Set up GitHub: 
- If you don't have a GitHub account, sign up for one at [[GitHub](https://github.com)] 
## <a name="_toc165815486"></a>Install GitHub desktop:
- This is not a prerequisite, but I find the GitHub desktop interface more user-friendly and intuitive.
## <a name="_toc165815487"></a>Fork and Clone your GitHub repository: 

- Click the fork button to fork ![](RMImages\Aspose.Words.3fa6b31d-e2dc-438a-a73a-454b6a711682.001.png) the repository at http://github.com/KiriJB/ProjectEGM722v2 and have a copy in your own GitHub repository.
- There should only be one branch named "main", which is the branch you need to fork. After clicking on the fork button and the new branch is created, please take note of its new location, which should look something like [http://www.github.com/<your_name>/ProjectEGM722v2](http://www.github.com/%3cyour_name%3e/ProjectEGM722v2).
- To clone the repository so you have a copy stored locally on your device. Open a terminal (Command Prompt on Windows or Terminal on macOS/Linux). 
- Navigate to the directory where you want to clone your repository.

  ![](RMImages\Aspose.Words.3fa6b31d-e2dc-438a-a73a-454b6a711682.002.png)

- Clone your repository using the following command: 

  ![](RMImages\Aspose.Words.3fa6b31d-e2dc-438a-a73a-454b6a711682.003.png)

- Replace <your\_name> with your GitHub username. 

## <a name="_toc165815488"></a>Create and activate a new environment from environment.yml: 
- Open the Anaconda <base> command prompt from the start menu and navigate to your local project directory in the terminal: ![ref1]
- Create the conda environment from the environment.yml file (Figure 2). This should create a new environment with the name specified in the file and all the necessary dependencies installed: ![](RMImages\ENV.png)

- <a name="_toc165815512"></a>Activate the environment: ![](RMImages\Aspose.Words.3fa6b31d-e2dc-438a-a73a-454b6a711682.007.png)
- Replace `ProjectEGM722v2` with the name you specified in your environment.yml file if you changed it. 

## <a name="_toc165815489"></a>Verify that the environment was created successfully: 
- Check that your environment is listed: ![](RMImages\Aspose.Words.3fa6b31d-e2dc-438a-a73a-454b6a711682.008.png)
- You should see a list of environments, including the one you just created; you should also see the new environment in the environment list in the Anaconda Navigator desktop application.
## <a name="_toc165815490"></a>Install Command Prompt:
- In the Anaconda Navigator Application, under ‘Home,’ select the environment you created from the dropdown. Look for the CMD.exe Prompt and install it in the environment.
## <a name="_toc165815491"></a>**IMPORTANT** Check for Anaconda Extension Libraries: 
- You must also check that the Anaconda extensions libraries have been installed. To do this, in the Anaconda navigator, select Environments, highlight the environment you have just created, and view the installed packages.
- The following packages should be the first five libraries in the list; if they are not present, click on ‘Not Installed’ from the drop-down menu and check the tick boxes next to them. Then click to install.

  aext-assistant
  aext-assistant-server
  aext-core
  aext-core-server
  aext-shared

- When the environment is created, these files should be installed from the default channel listed in the environment.yml file. However, this does not seem to occur.
## ` `<a name="_toc165815492"></a>To access NASA EarthData: 
- To access NASA EarthData, you will need a NASA EarthData account. To create an account, go to <https://urs.earthdata.nasa.gov>. Please save your username and password, as you will need it for the next step—setting up the .netrc file.
- To create the file, open **Notepad** or your text editor of choice and enter the following line:

  machine urs.earthdata.nasa.gov login <username> password <password>

- Replacing <username> with your NASA EarthData username and <password> with your NASA EarthData password.
- Save the file as .netrc to your **Home** directory (on Windows, this should be C:\Users\<your\_username>). Be sure to select **All Files** for **Save as type**:
- You should then change the permissions of the new netrc file so other users cannot access it.
## <a name="_toc165815493"></a>Test Data
In the 'Data' folder located at C:\Users\<your\_name>\ProjectEGM722v2\Data, you can find several shape files that have already been saved for test purposes (Table 1). Alternatively, if you prefer, you can use your own polygon shapefile of an area of your choice. However, it's **important** to note that the shape file and its associated files should be saved in the 'Data' folder. This is necessary for the Python script to locate the shape file.
If you want to change the location of the shapefile you will need to comment out lines 31,32,and 38
and uncomment line 39, adding the path to your shape file between the ''.

|Name of Shapefile|Description of Shapefile|
| :-: | :-: |
|Andorra\_Country\_Boundary.shp|Outline of the Mountainous European Country, Andorra|
|Counties.shp|Outline of the Country, Northern Ireland|
|Djibouti\_Country\_Boundary.shp|Outline of the East African Country, Djibouti|
|IOM\_Boundary.shp|Outline of the Isle of Man|
|Liechtenstein\_Country\_Boundary.shp|Outline of the Mountainous European Country, Liechtenstein|
|Maine\_State\_Boundary.shp|Outline of the small Eastern US State of Maine|
|Purbeck\_Boundary.shp|Outline of the Purbeck Coastal Area in the County of Dorset|

<a name="_toc165815517"></a>*Table 1 – Shapefiles available in the data folder*


That's it! You've set up your project on GitHub, created a conda environment, installed dependencies from the `environment.yml` file and should have access to NASA EarthData. You're ready to run/edit the scripts.
The code was developed in the PyCharm IDE and runs successfully using PyCharm. However, it has also been tested in Spyder and can be run directly from the Conda Command Prompt, provided the environment has been created correctly.
## <a name="_toc165815494"></a>Install Pycharm and run the script

- If PyCharm is not already installed, visit [PyCharm](https://www.jetbrains.com/pycharm/download/) to download the appropriate version for your Operating System and follow the installation instructions. 
- When PyCharm is installed, open it and select “Create a new project”. (Note this is the set-up for Windows 10; it may differ for other Operating Systems)
- The New Project Window will open
- To set up a Python interpreter, use the conda environment you created earlier. Select:
1. Location - Save the project in the same location as the cloned ProjectEGM722v2 repository  c:\Users\<user\_name>\ProjectEGM722v2
1. Interpreter type - “Custom environment”
1. Environment - “Select existing”
1. Type – “Conda”
1. Path to Conda - C:\Users\<user\_name>\anaconda3\Scripts\conda.exe
1. Environment – From the dropdown, select the conda environment you created earlier
- Press  “Create” 
- Select “index.py” from the side menu, and press “run” or shift+F10 to run the script. 
## <a name="_toc165815495"></a>Run the script from the command prompt
To run the script from the command prompt:

- Open the CMD.exe prompt from the Anaconda Application, ensuring you are in the environment you created earlier.
- Change the directory to the cloned repository![ref2]
- To run the code, type and press enter:![ref3]

[ref1]: RMImages\Aspose.Words.3fa6b31d-e2dc-438a-a73a-454b6a711682.004.png
[ref2]: RMImages\Aspose.Words.3fa6b31d-e2dc-438a-a73a-454b6a711682.009.png
[ref3]: RMImages\Aspose.Words.3fa6b31d-e2dc-438a-a73a-454b6a711682.010.png

## License

[MIT](https://choosealicense.com/licenses/mit/)
