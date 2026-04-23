#!/usr/bin/env python3
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

    follower_2_node = Node(
        package='turtle_follower',
        executable='turtle_follower_node',
        name='follower_2_node',
        output='screen',
        parameters=[{
            'my_name': 'turtle2',
            'target_name': 'turtle1',
            'speed': 1.5,
            'spawn_x': 1.0,
            'spawn_y': 1.0,
            'spawn_theta': 0.0
        }]
    )
    ld.add_action(follower_2_node)

    follower_3_node = Node(
        package='turtle_follower',
        executable='turtle_follower_node',
        name='follower_3_node',
        output='screen',
        parameters=[{
            'my_name': 'turtle3',
            'target_name': 'turtle2',
            'speed': 1.5,
            'spawn_x': 9.0,
            'spawn_y': 9.0,
            'spawn_theta': 0.0
        }]
    )

    delayed_follower_3 = TimerAction(
        period=1.5,
        actions=[follower_3_node]
    )
    ld.add_action(delayed_follower_3)

    follower_4_node = Node(
        package='turtle_follower',
        executable='turtle_follower_node',
        name='follower_4_node',
        output='screen',
        parameters=[{
            'my_name': 'turtle4',
            'target_name': 'turtle3',
            'speed': 1.5,
            'spawn_x': 1.0,
            'spawn_y': 1.0,
            'spawn_theta': 0.0
        }]
    )

    delayed_follower_4 = TimerAction(
        period=3.0,
        actions=[follower_4_node]
    )
    ld.add_action(delayed_follower_4)

    follower_5_node = Node(
        package='turtle_follower',
        executable='turtle_follower_node',
        name='follower_5_node',
        output='screen',
        parameters=[{
            'my_name': 'turtle5',
            'target_name': 'turtle4',
            'speed': 1.5,
            'spawn_x': 9.0,
            'spawn_y': 9.0,
            'spawn_theta': 0.0
        }]
    )

    delayed_follower_5 = TimerAction(
        period=4.5,
        actions=[follower_5_node]
    )
    ld.add_action(delayed_follower_5)

    return ld
