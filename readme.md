# Runespoor Python 3D Game Engine

> A python 3D game engine written in c++ using SDL, Assimp, OpenGL(GLAD), and GLM.

Runespoor requires pkg-config along

```
pip install Runespoor
```

 - Note that Runespoor is still in development and only dev versions are available right now.  Everything is subject to change, be fixed, and improve.

## About:

Runespoor is a flexible, straight forward, multi-paradigm game engine that is built from the ground up with developer experience in mind.  Utilizing a game loop system similar to pygame, you are able to abstract elements of your game away from the game loop as much as you'd like.

For a taste of the api check out the test file:

```py
from renderer import (
    Vec3, Camera, Mesh, Object, Window, EVENT_FLAG,
    Material, Shader, ShaderType, EVENT_STATE, Quaternion
)
import math
from copy import copy

# The meshes used in this testfile are not provided with the library or source files.

dim = (1280, 720)
focal_length = 10000

camera = Camera(Vec3(0.0,0.0,0.0), Vec3(0.0,0.0,0.0), *dim, focal_length, math.radians(60))
window = Window("FBX Car Test", camera, *dim, False)

# Materials are equivalent to shader programs.
default_material = Material(
    Shader.from_file("./default_vertex.glsl", ShaderType.VERTEX),
    Shader.from_file("./default_fragment.glsl", ShaderType.FRAGMENT)
)

default_material.set_uniform("focal_length", focal_length, "i")
# "i" means the uniform is an integer type

car_meshes = Mesh.from_file("./meshes/fbx_car/svj_PACKED.fbx")

car = Object(car_meshes,
    Vec3(0.0,-100.0,500), Vec3(0,0,0), Vec3(1,1,1), material=default_material)

car2 = Object(car_meshes,
    Vec3(300,0,500), Vec3(10,3.57,23.2), material=default_material)

teapot = Object(Mesh.from_file("./meshes/teapot/teapot.obj"),
    Vec3(-100,0,200), Vec3(0,0,0), material=default_material)

pirate_ship = Object(Mesh.from_file("./meshes/pirate_ship/pirate_ship.obj"),
    Vec3(-100,-100,300), Vec3(0,10,0), material=default_material)

render_list = [
    car,
    car2,
    teapot,
    pirate_ship
]

window.lock_mouse(True)

vel_yaw = 0.0
vel = 0.0
frict = 0.1
accel = 5
cam_dist = 300.0
magic_turn_dampener = 4
mouse_sensitivity = 10
counter = 0
counter_speed = 1
while not window.event.check_flag(EVENT_FLAG.QUIT) and window.event.get_flag(EVENT_FLAG.KEY_ESCAPE) != EVENT_STATE.PRESSED:
    # Use WASD keys.
    if window.event.get_flag(EVENT_FLAG.KEY_d) == EVENT_STATE.PRESSED:
        # ROTATE RIGHT
        vel_yaw -= 0.3
    if window.event.get_flag(EVENT_FLAG.KEY_a) == EVENT_STATE.PRESSED:
        # ROTATE LEFT
        vel_yaw += 0.3
    if window.event.get_flag(EVENT_FLAG.KEY_s) == EVENT_STATE.PRESSED:
        # BACKWARDS
        vel -= accel
    if window.event.get_flag(EVENT_FLAG.KEY_w) == EVENT_STATE.PRESSED:
        # FORWARD
        vel += accel
    # apply a quaternion rotation arround the vector vec3(1,1,0)
    teapot.rotation = Quaternion.from_axis_angle(Vec3(1,1,0), math.radians(counter))
    
    # Clamp and rotate, then apply friction.
    vel_yaw = min(max(vel_yaw, -100), 100) if abs(vel_yaw) > frict else 0
    car.rotation.rotate_yaw(-vel_yaw/magic_turn_dampener * window.dt)
    vel_yaw -= math.copysign(frict, vel_yaw)
    
    # Clamp the velocity.
    vel = min(max(vel, -1000), 1000) if abs(vel) > frict else 0
    # Move the car forwards with its forwards vector with a magnitude of `vel` and apply friction
    car.position += -car.rotation.forward * vel * window.dt # window.dt is deltatime
    vel -= math.copysign(frict, vel)
    

    # Rotate the camera
    cam_rot = Quaternion.from_quat(camera.rotation)
    yaw_rot = 0 # capture the yaw rot so we can apply it to the quat later in the case where the camera is clamped

    if window.event.check_flag(EVENT_FLAG.MOUSE_MOTION):
        cam_rot.rotate_yaw(yaw_rot := -math.radians(window.event.mouse.rel_x * mouse_sensitivity * window.dt))

        cam_rot.rotate(cam_rot.right, math.radians(window.event.mouse.rel_y * mouse_sensitivity * window.dt))
    
    # zoom in and out
    if window.event.check_flag(EVENT_FLAG.MOUSE_WHEEL):
        cam_dist -= window.event.mouse.wheel.y * 10


    # apply/clamp, position, and camera rotation
    if cam_rot.up.y >= 0.7:
        # Position the camera behind the car based on its forward vector
        camera.position = car.position - (cam_rot.forward * cam_dist)

        camera.rotation = cam_rot
    else:
        camera.rotation.rotate_yaw(yaw_rot)
        # Position the camera behind the car based on its forward vector
        camera.position = car.position - (camera.rotation.forward * cam_dist)
    # Re-render the scene.
    window.update(render_list)
    # This also refreshes window.current_event.
    counter += counter_speed
```

Then when we run it, it looks something like this:

![](https://github.com/FrewtyPebbles/Runespoor-Python3D-Game-Engine/blob/main/tests/the_quats_are_quatting.gif)

# TODO:

 - Refactor MVP matrix into their respective entities.

 - Figure out better solution for multimesh assimp imports.  (Current solution groups all meshes from the scene in a python list.)

 - Add `from_raw` constructor to mesh to make procedural meshes possible.

 - Make render list managed by Window object.

 - Add Sprite object and Object2D object for 2D games/HUD.

 - Add window/fullscreen scaling.

 - Add Matrix datastructures for GLM.

# Future Plans:

 - Switch to Vulkan.
