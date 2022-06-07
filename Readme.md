The aim here is to determine the lights angulus/intensity by using the obtained mask and the picture obtained from the neural network.

We currently have three steps in this process:
    1) Get the lightest point on the sphere
    2) Get the circles parameters (center position, radius)
        For this we use the circle regression (found on https://scipy-cookbook.readthedocs.io/)
    3) Deduct the light properties
        The size of the shadowed area
        The light vector direction
        The relative intensity of the light

Given in this part are:
    1) tai.py  
        The code itself (need to uncomment and write the name files to work)

    2) test_0.py => test_10.py
        The list of test scripts that works directly

    3) im_0.jpg => im_10.jpg
        The pictures used in the test scripts
        Please be aware that those should never be published

    4) im_0_mk.jpg => im_10_mk.jpg
        The binary masks associated with each picture (used in the test scripts)

Some files will be created by the test so as to help understand what happens
