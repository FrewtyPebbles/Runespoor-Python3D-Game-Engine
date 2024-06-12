from renderer import Vec3, Camera, Mesh, Object, Window, event,\
    Material, Shader, ShaderType
import math

dim = (1280, 720)
focal_length = 1000

camera = Camera(Vec3(0.0,0.0,0.0), *dim, focal_length, math.radians(60))
window = Window("FBX Car Test", camera, *dim)

# Materials are equivalent to shader programs.
default_material = Material(
    Shader.from_file("./default_vertex.glsl", ShaderType.VERTEX),
    Shader.from_file("./default_fragment.glsl", ShaderType.FRAGMENT)
)

default_material.set_uniform("focal_length", focal_length, "i")
# "i" means the uniform is an integer type

car_meshes = Mesh.from_file("meshes/fbx_car/svj_PACKED.fbx")

car = Object(car_meshes,
    Vec3(0.0,0,-500), Vec3(0,0,0), material=default_material)

car2 = Object(car_meshes,
    Vec3(300,0,-500), Vec3(10,3.57,23.2), material=default_material)

teapot = Object(Mesh.from_file("meshes/teapot/teapot.obj"),
    Vec3(-100,0,-200), Vec3(10,3.57,23.2), material=default_material)

render_list = [
    car,
    car2,
    teapot
]

vel_yaw = 0.0
vel_pitch = 0.0
frict = 0.1
while window.current_event != event.QUIT:
    if window.current_event == event.KEY_RIGHT:
        vel_yaw -= 0.3
    if window.current_event == event.KEY_LEFT:
        vel_yaw += 0.3

    vel_yaw = min(max(vel_yaw, -100), 100)

    car.rotation.y += vel_yaw * window.dt

    vel_yaw -= math.copysign(frict, vel_yaw)

    if window.current_event == event.KEY_DOWN:
        vel_pitch -= 0.3
    if window.current_event == event.KEY_UP:
        vel_pitch += 0.3

    vel_pitch = min(max(vel_pitch, -100), 100)

    car.rotation.x += vel_pitch * window.dt

    vel_pitch -= math.copysign(frict, vel_pitch)

    window.update(render_list)