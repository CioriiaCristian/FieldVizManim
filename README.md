# FieldVizManim

This is a repository of 3D visualizations of a spherical configuration of field lines. 

To run the code, install manim. For this please follow the instructions at this link [Manim installation](https://docs.manim.community/en/stable/installation.html)

Make sure to add the FFmpeg bin directory to the System Path.

To run the code, open the cli inside local repository 
```shell
    $ manim -ql --disable_caching -p --write_to_movie field_arrows.py FieldArrows
```

The -p flag stands for preview
The --write_to_movie will save a copy of the video locally
The -ql stands for low quality. Change to -qm for medium quality

If you would like to interact with the scene it is recomended to run the following command
```shell
    $ manim -ql --disable_caching -p --write_to_movie --renderer=opengl field_arrows.py FieldArrows
```
This will use the somewhat stable OpenGL backend. This needs to be used in conjunction with the self.interactive_embed() inside the construct environment. 