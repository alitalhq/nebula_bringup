import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    """
    Nebula sisteminin tüm ana düğümlerini başlatan ana launch dosyası.
    - Profil tabanlı kamera konfigürasyonu (profiles_file + profile)
    - İsteğe bağlı simülasyon (use_simulation)
    """
    hss_vision_pkg = get_package_share_directory('hss_vision')
    #nebula_simulation_pkg = get_package_share_directory('nebula_simulation')

    # --- Launch Argümanları (profil tabanlı) ---
    profiles_file_arg = DeclareLaunchArgument(
        'profiles_file',
        default_value=os.path.join(hss_vision_pkg, 'config', 'camera_profiles.yaml'),
        description="Kamera profilleri YAML dosyasının yolu."
    )

    profile_arg = DeclareLaunchArgument(
        'profile',
        default_value='internal',
        description="Kullanılacak kamera profili (örn. internal, front, down)."
    )
    """
    use_simulation_arg = DeclareLaunchArgument(
        'use_simulation',
        default_value='true',
        description="True ise gimbal_simulator_node'u başlatır, False ise gerçek donanım beklenir."
    )
    """

    # --- Dahil Edilen Launch Dosyaları ---
    # hss_vision/launch/camera_driver.launch.py, 'profiles_file' ve 'profile' argümanlarını bekliyor
    camera_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(hss_vision_pkg, 'launch', 'camera_driver.launch.py')
        ),
        launch_arguments={
            'profiles_file': LaunchConfiguration('profiles_file'),
            'profile': LaunchConfiguration('profile')
        }.items()
    )

    """
    simulator_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nebula_simulation_pkg, 'launch', 'gimbal_simulator.launch.py')
        ),
        condition=IfCondition(LaunchConfiguration('use_simulation'))
    )
    """

    return LaunchDescription([
        profiles_file_arg,
        profile_arg,
        #use_simulation_arg,
        camera_driver_launch,
        #simulator_launch,
    ])