# William Python Game Engine

Welcome to the William Python Game Engine repository!

## Introduction

William Python Game Engine is a lightweight and versatile game engine designed for creating 2D games using Python. It provides developers with a simple yet powerful framework to bring their game ideas to life.

## Getting Started

To start using William Python Game Engine, follow these steps:

1. **Clone the Repository:** Clone this repository to your local machine using `git clone https://github.com/your-username/william-python-game-engine.git`.

2. **Get Python 3.12.1:** Download this python version:

3. **Install Dependencies:** Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Developing:** You're all set! Start developing your game using the William Python Game Engine.

## Contributing

Contributions are welcome! If you'd like to contribute to the William Python Game Engine, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Certainly! Here's the edited markdown for your README:

## Documentation

### Drawing logic

To work in native resolution but scale up for better testing, blit your sprite surfaces on the `NATIVE_SURFACE`, which is then scaled and blitted to the `DISPLAY_SURFACE`. This allows you to avoid squinting when testing the game.

### Create your scenes

Create your main game scene using the `SceneManager.change_scene_to_file` method. Provide the relative path from `main.py` and the scene class name.

```python
from classes.scene_manager import SceneManager

SceneManager.change_scene_to_file("./scenes/test_scene.py")
```

## Update

In the main game loop, update the Input singleton and the current scene:

```python
# Update input
Input.update(pg.key.get_pressed())

# Update current scene
SceneManager.current_scene.update(delta)
```

## Scene structure

Here's a simple scene structure example:

```python
from classes.input import Input
from classes.scene_manager import SceneManager
import pygame as pg

class AnotherTestScene:
    def __init__(self):
        # Initialize props + children

    def update(self, delta):
        # Update scene logic
        if Input.is_action_pressed(pg.K_SPACE):
            print("Space key is pressed from AnotherTestScene")

        if Input.is_action_pressed(pg.K_RIGHT):
            SceneManager.change_scene_to_file("./scenes/test_scene.py")

    def draw(self):
        # Draw scene elements

    # Add other methods for callbacks, etc.
```

## Next update

Here's what's planned for future updates:

- [x] Importing images
- [x] Drawing layers
- [x] Camera class
- [ ] Animation class
- [x] Level editor -> save feature
- [x] a Y sort layer

I need to add name prop to each sprite in the sprite sheet, so that i can distinguish each one
