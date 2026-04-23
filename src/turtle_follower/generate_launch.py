#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

def generate_launch_file(count):
    if count < 2:
        print("Error: Minimum number of turtles is 2.")
        return

    launch_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction
import launch

def generate_launch_description():
    ld = LaunchDescription()
    
    follower_speed_param = launch.actions.DeclareLaunchArgument(
        'follower_speed',
        default_value='1.5',
        description='Speed for follower turtles'
    )
    ld.add_action(follower_speed_param)
    
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen'
    )
    ld.add_action(turtlesim_node)
    
    teleop_node = Node(
        package='turtlesim',
        executable='turtle_teleop_key',
        name='teleop',
        output='screen',
        prefix=['xterm -e']
    )
    ld.add_action(teleop_node)
'''

    followers_code = []
    for i in range(2, count + 1):
        my_name = f"turtle{i}"
        target_name = f"turtle{i-1}"
        spawn_x, spawn_y = (1.0, 1.0) if i % 2 == 0 else (9.0, 9.0)
        delay_seconds = (i - 2) * 1.5
        
        node_def = f'''
    follower_{i}_node = Node(
        package='turtle_follower',
        executable='turtle_follower_node',
        name='follower_{i}_node',
        output='screen',
        parameters=[{{
            'my_name': '{my_name}',
            'target_name': '{target_name}',
            'speed': 1.5,
            'spawn_x': {spawn_x},
            'spawn_y': {spawn_y},
            'spawn_theta': 0.0
        }}]
    )
'''
        followers_code.append(node_def)
        
        if delay_seconds > 0:
            followers_code.append(f'''
    delayed_follower_{i} = TimerAction(
        period={delay_seconds},
        actions=[follower_{i}_node]
    )
    ld.add_action(delayed_follower_{i})
''')
        else:
            followers_code.append(f"    ld.add_action(follower_{i}_node)\n")
            
    launch_content += "".join(followers_code)
    launch_content += "\n    return ld\n"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    launch_dir = os.path.join(script_dir, 'launch')
    os.makedirs(launch_dir, exist_ok=True)
    file_path = os.path.join(launch_dir, 'turtle_chain_launch.py')

    with open(file_path, 'w') as f:
        f.write(launch_content)

    print(f"Done! Launch file is saved in: {file_path}")
    print("Run: ros2 launch turtle_follower turtle_chain_launch.py")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 generate_launch.py <number_of_turtles>")
    else:
        try:
            n = int(sys.argv[1])
            generate_launch_file(n)
        except ValueError:
            print("Error: Parameter must be an integer.")