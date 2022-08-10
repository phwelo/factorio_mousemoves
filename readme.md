# Factorio MouseMoves
This is the first project I've ever built on/for my Windows PC.  I was playing factorio & felt pretty strongly that mouse based movement would be a serious improvement.  I think I was right.

## Installation:
```
> git clone {repo path}
> py -m pip install Autohotkey.py screeninfo keyboard mouse anycache
```

## Run:
```
> py -m ahkpy {path to factorio.py}
```

### How it works:
* Edges of the screen (and corners) will move your player or the camera in the appropriate direction. This only applies when the game described by TITLE_SEARCH is active.
* You can toggle on mouse right click by pressing Shift + Left Mouse click.  Tap Right Mouse button to cancel.
* Hold shift to ignore the edges of the screen temporarily.

## Variables:
There eare a few variables that act as pseudo settings at the moment
* `EDGE_PIXELS`: Integer representing the number of pixels from the edge of the screen at which to activate the movement.  Default = 20
* `TITLE_SEARCH`: String including a portion of the title which to search for.  This could likely be used to adapt the tool to other games. Default = "Factorio"
* `RELATIVE_TO`: Seems that if you have multiple monitors you might have to change this. Options: Screen, Relative, Window, Client. Default: "Screen"
