import importlib.util


class SceneManager:
    current_scene = None

    @staticmethod
    def change_scene_to_file(module_path, module_name):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        custom_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(custom_module)
        scene_class_name = module_name.split('.')[-1]
        scene_class = getattr(custom_module, scene_class_name)
        SceneManager.current_scene = scene_class()
