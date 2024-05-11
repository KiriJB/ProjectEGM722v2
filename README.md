# Assignment ProjectEGM722v2

<img src="RMImages\logo.png" width="550">

input: Polygon shape file for the area of interest.  
outputs: Geotiff of the shapefile polygon area  
         PNG image file of the Geotiff file  
         CSV of the data generated to create the elevation profile from the geotiff  
         PNG image file of the generated elevation profile  
         PDF of the generated elevation profile 

A python script that creates an elevation profile between 2 user specified points.
A polygon shapefile is used to get DEM data from NASA Earthdata, raster DEM data (GeoTIFF) is displayed using Matplotlib
the user can click 2 points on the DEM for the start and end points of the elevation profile,
the user is prompted to input the number of points to use along the elevation profile and to enter the distance to use 
to separate the profile into subplots.

The Python code, data files and repository can be accessed here: <http://github.com/KiriJB/ProjectEGM722v2>

Guide to setting up Anaconda with GitHub and creating an environment from an environment.yml file: 
## Install Anaconda: 
- Download and install Anaconda from the [[official website](https://www.anaconda.com/products/distribution)].
- Follow the installation instructions for your operating system. 
## Set up GitHub: 
- If you don't have a GitHub account, sign up for one at [[GitHub](https://github.com)]
## Install GitHub desktop
- This is not a prerequisite, but I find the GitHub desktop interface more user-friendly and intuitive.
- Follow the instructions here to download and install GitHub Desktop[[GitHub](https://docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop)]
## Fork and Clone your GitHub repository: 

- Click the fork button in GitHub web interface to fork ![ref1] the repository at http://github.com/KiriJB/ProjectEGM722v2 and have a copy in your own GitHub repository.
- There should only be one branch named "main", which is the branch you need to fork. After clicking on the fork button and the new branch is created, please take note of its new location, which should look something like [http://www.github.com/<your_name>/ProjectEGM722v2](http://www.github.com/%3cyour_name%3e/ProjectEGM722v2).
- To clone the repository so you have a copy stored locally on your device. Open a terminal (Command Prompt on Windows or Terminal on macOS/Linux). 
- Navigate to the directory where you want to clone your repository.
![ref2]
- Clone your repository using the following command:
![ref3]
- Replace <your\_name> with your GitHub username. 

## Create and activate a new environment from environment.yml: 
- Open the Anaconda <base> command prompt from the start menu and navigate to your local project directory in the terminal: ![ref4]
- Create the conda environment from the environment.yml file (Figure 2). This should create a new environment with the name specified in the file and all the necessary dependencies installed: ![ref5]  
<img src="RMImages\Image6.png" width="150">
- <a name="_toc165815512"></a>Activate the environment: ![ref7]
- Replace `ProjectEGM722v2` with the name you specified in your environment.yml file if you changed it. 

## Verify that the environment was created successfully: 
- Check that your environment is listed: ![ref8]
- You should see a list of environments, including the one you just created; you should also see the new environment in the environment list in the Anaconda Navigator desktop application.
## Install Command Prompt:
- In the Anaconda Navigator Application, under ‘Home,’ select the environment you created from the dropdown. Look for the CMD.exe Prompt and install it in the environment.
## **IMPORTANT** Check for Anaconda Extension Libraries: 
- You must also check that the Anaconda extensions libraries have been installed. To do this, in the Anaconda navigator, select Environments, highlight the environment you have just created, and view the installed packages.
- The following packages should be the first five libraries in the list; if they are not present, click on ‘Not Installed’ from the drop-down menu and check the tick boxes next to them. Then click to install.

  aext-assistant
  aext-assistant-server
  aext-core
  aext-core-server
  aext-shared

- When the environment is created, these files should be installed from the default channel listed in the environment.yml file. However, this does not seem to occur.
## To access NASA EarthData: 
- To access NASA EarthData, you will need a NASA EarthData account. To create an account, go to <https://urs.earthdata.nasa.gov>. Please save your username and password, as you will need it for the next step—setting up the .netrc file.
- To create the file, open **Notepad** or your text editor of choice and enter the following line:

  machine urs.earthdata.nasa.gov login <username> password <password>

- Replacing <username> with your NASA EarthData username and <password> with your NASA EarthData password.
- Save the file as .netrc to your **Home** directory (on Windows, this should be C:\Users\<your\_username>). Be sure to select **All Files** for **Save as type**:
- You should then change the permissions of the new netrc file so other users cannot access it.
## Test Data
In the 'Data' folder located at C:\Users\<your\_name>\ProjectEGM722v2\Data, you can find several shape files that have already been saved for test purposes (Table 1). Alternatively, if you prefer, you can use your own polygon shapefile of an area of your choice. However, it's **important** to note that the shape file and its associated files should be saved in the 'Data' folder. This is necessary for the Python script to locate the shape file.
If you want to change the location of the shapefile you will need to comment out lines 29-37 and 45
and uncomment line 46, adding the path to your shape file between the ''.

|Name of Shapefile|Description of Shapefile|
| :-: | :-: |
|Andorra\_Country\_Boundary.shp|Outline of the Mountainous European Country, Andorra|
|Counties.shp|Outline of the Country, Northern Ireland|
|Djibouti\_Country\_Boundary.shp|Outline of the East African Country, Djibouti|
|IOM\_Boundary.shp|Outline of the Isle of Man|
|Liechtenstein\_Country\_Boundary.shp|Outline of the Mountainous European Country, Liechtenstein|
|Purbeck\_Boundary.shp|Outline of the Purbeck Coastal Area in the County of Dorset|

*Table 1 – Shapefiles available in the data folder*


That's it! You've set up your project on GitHub, created a conda environment, installed dependencies from the `environment.yml` file and should have access to NASA EarthData. You're ready to run/edit the scripts.
The code was developed in the PyCharm IDE and runs successfully using PyCharm. However, it has also been tested in Spyder and can be run directly from the Conda Command Prompt, provided the environment has been created correctly.
## Install Pycharm and run the script

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
## Run the script from the command prompt
To run the script from the command prompt:

- Open the CMD.exe prompt from the Anaconda Application, ensuring you are in the environment you created earlier.
- Change the directory to the cloned repository![ref9]
- To run the code, type and press enter:![ref10]

[ref1]: RMImages/Image1.png
[ref2]: RMImages/Image2.png
[ref3]: RMImages/Image3.png
[ref4]: RMImages/Image4.png
[ref5]: RMImages/Image5.png
[ref6]: RMImages/Image6.png
[ref7]: RMImages/Image7.png
[ref8]: RMImages/Image8.png
[ref9]: RMImages/Image9.png
[ref10]: RMImages/Image10.png


## License

[MIT](https://choosealicense.com/licenses/mit/)
