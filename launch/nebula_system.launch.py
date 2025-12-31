import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    """
    Nebula sisteminin tüm ana düğümlerini başlatan ana launch dosyası.
    - Profil tabanlı kamera konfigürasyonu (profiles_file + profile + ...)
    """
    vision_share = FindPackageShare('nebula_vision')
    test_share = FindPackageShare('nebula_test')
    control_share = FindPackageShare('nebula_control')

    default_profiles_file = PathJoinSubstitution([vision_share, 'config', 'camera_profiles.yaml'])

    profiles_file_arg = DeclareLaunchArgument(
        'profiles_file',
        default_value=default_profiles_file,
        description='Kamera profil YAML dosyasının yolu'
    )

    profile_arg = DeclareLaunchArgument(
        'profile',
        default_value='internal',
        description="Kullanılacak kamera profili."
    )

    camera_driver_node = Node(
        package='nebula_vision',
        executable='camera_driver',
        name='camera_driver',
        output='screen',
        parameters=[{
            'profiles_file': LaunchConfiguration('profiles_file'),
            'profile': LaunchConfiguration('profile'),
        }]
    )

    vision_processor_node = Node(
        package='nebula_vision',
        executable='vision_processor_node',
        name='vision_processor',
        output='screen',
        parameters=[
            PathJoinSubstitution([vision_share, 'config', 'vision_params.yaml'])
        ]
    )

    image_subscriber_node = Node(
        package='nebula_test',
        executable='image_processed_subscriber',
        name='image_logger_test',
        output='screen'
    )

    operation_manager_node = Node(
        package='nebula_control',
        executable='operation_manager_node',
        name='operation_manager',
        output='screen'
    )


    return LaunchDescription([
        profiles_file_arg,
        profile_arg,
        camera_driver_node,
        vision_processor_node,
        image_subscriber_node,
        operation_manager_node
    ])
