<**      Project Start Date - 13/11/2022         **>

==============================================
                    Steps
==============================================
______________________________________________
        Import and Install Dependancies
______________________________________________
1) YOLOv5 github repo is cloned
2) Requirements are added to the YOLOv5 folder
3) Install the correct PyTorch torchvision version
______________________________________________
        Train and Validate the Model
______________________________________________
1) Custom .yaml file made that contains the classes and path to the custom dataset
2) To avoid conflicts between libraries when training, KMP_DUPLICATE_LIB_OK is set to true
3) Hyperparameters for image and batch size is set to 416 and 16 respectfully
4) Weights pulled from YOLOv5l for more parameters (40million instead of the 7million from YOLOv5s)
5) Set the cache to GPU as it is the fastest option
6) Weights are saved to exp(i) that increment each time model is trained
7) detect.py is run on a set of different validation images
8) Pre-trained YOLOv5 model is then used to get the object detector to work
______________________________________________
        Running the model
______________________________________________
1) Used tkinter to create a screen that can hold the camera, buttons, and text
2) OpenCV used to turn on the camera
3) Generates a random letter for the user to try and sign
4) Lets the user open up a reference image that has pictues of the ideal signs
5) Tells the user how well they are doing for each letter. Colour coordinated
6) Has an option for the user to start a timer that randomly selects a new letter for them to sign every 5 seconds, or 
   to select a specific letter that they want to practice


==============================================
The use of Roboflow
==============================================

Roboflow was used to get the labels for images in the custom dataset (collected by myself).
While roboflow also has the ability to add the neccisary folders to the program directly, it was found that this brings up a few issues with pathing.
Therefore, a new folder outside of ../yolov5 was manually made called 'data'. This folder has all of the images used as well as their labels. The
roboflow-created folders now just contain images for the test and validation of the model.


==============================================
Issues
==============================================

> //SOLVED\\ > There is no way to turn on the camera in Google Colab with OpenCV. This was solved by switching IDEs to Visual Studio Code - 14/11/2022

> //SOLVED\\ > The biggest issue when making this model was having the camera not turn on when cv2.VideoCapture(0) was ran.
This was fixed by uninstalling and reinstalling the cv2 library through the terminal (or Command Prompt) only.  - 20/11/2022

> //SOLVED\\ > The pre-generated roboflow data.yaml file had an incorrect layout as well as pathing, to fix this, a new file called 'sign_language_dataset.yaml' 
was manually created and called upon where needed. - 29/11/2022

> //SOLVED\\ > The program will only detect gestures if the user is in a particular spot and under the perfect lighting conditions. This can be solved by
making more defined and varied labels per image in the training set. I will most likely have to redo the dataset for this.  - 06/12/2022

> //SOLVED\\ > To display the messages, buttons were used instead of labels.These are more hardware intensive. 
At the moment I cannot fit them to a label using tkinter - 18/12/2022

> //LOW PRIORITY\\ > (only when testing) When the program crashes, it displays error message saying that there is a dead kernal. 
The only way to fix this is by reopening VSC - 16/12/2022

> //SOLVED\\ > //HIGH PRIORITY\\ > Crashes due to memory limit when trying to train the model using the ADAM optimizer - 22/01/2023

> //HIGH PRIORITY\\ > The program uses a LOT of memory - 27/01/2023


==============================================
Log
==============================================

> The letter x never works with the current model - 01/12/2022
> Gets confused between vowls due to them having very similar gestures - 01/12/2022
> Gets confused with the letters 'l', 'n', and (rarely), 'v' - 01/12/2022
> The letter s is very hard to detect due to it having more depth than any other letter - 06/12/2022
> The model needs a very specific light level to work accuratly. The model did not work at all when testing at the campus labs - 06/12/2022
> Added simple GUI functionality with a start and stop button - 06/12/2022
> Class names are now displayed under the image and not on the image itself as the model - 18/12/2022
> Created a whole new dataset. It is much smaller but a lot more consistent and produces better results - 21/01/2023
> New dataset struggles with the letter 'a' and seems to prefer the letter 'g' over a lot of letters- 21/01/2023
> User is now able to display a reference image of the ideal way to sign the letters - 21/01/2023
> Added a button that provides a description of how to sign most letters as well as some tips - 21/01/2023
> Never recognises 'R'. Other than that, it works perfectly - 22/01/2023
> New dataset with brightness augmentation works perfectly with every letter. Will now focus on UI/UX and additional functions - 27/01/2023
> Capped the maximum frame rate at 30fps to reduce memory load - 29/01/2023
> New text file that contains the cheat sheet to make it easier to add/remove items from it - 29/01/2023
> Program is now on an "app" sized screen with better defined headers and footers - 03/02/2023
