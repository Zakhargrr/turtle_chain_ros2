#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
from turtle_follower.turtle_logic import TurtleFollowerLogic
from rclpy.qos import qos_profile_sensor_data
from rclpy.executors import ExternalShutdownException

class TurtleFollowerNode(Node):
    def __init__(self):
        super().__init__('turtle_follower')
        
        self.declare_parameter('my_name', 'turtle2')
        self.declare_parameter('target_name', 'turtle1')
        self.declare_parameter('speed', 1.0)
        self.declare_parameter('spawn_x', 5.0)
        self.declare_parameter('spawn_y', 5.0)
        self.declare_parameter('spawn_theta', 0.0)

        self._my_name = self.get_parameter('my_name').get_parameter_value().string_value
        self._target_name = self.get_parameter('target_name').get_parameter_value().string_value
        self._speed = self.get_parameter('speed').get_parameter_value().double_value
        self._spawn_x = self.get_parameter('spawn_x').get_parameter_value().double_value
        self._spawn_y = self.get_parameter('spawn_y').get_parameter_value().double_value
        self._spawn_theta = self.get_parameter('spawn_theta').get_parameter_value().double_value
        
        self._my_pose = None
        self._target_pose = None
        self._logic = TurtleFollowerLogic(max_speed=self._speed, stop_distance=0.6)
        
        self._try_spawn()
        
        self._my_sub = self.create_subscription(
            Pose,
            f'/{self._my_name}/pose',
            self._my_pose_cb,
            qos_profile_sensor_data
        )
        
        self._target_sub = self.create_subscription(
            Pose,
            f'/{self._target_name}/pose',
            self._target_pose_cb,
            qos_profile_sensor_data
        )
        
        self._cmd_pub = self.create_publisher(
            Twist,
            f'/{self._my_name}/cmd_vel',
            10
        )
        
        self._timer = self.create_timer(0.033, self._control_loop)

    def _try_spawn(self):
        client = self.create_client(Spawn, '/spawn')
        
        while not client.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                return
            self.get_logger().info('Service /spawn not available, waiting...')
        
        req = Spawn.Request()
        req.x = self._spawn_x
        req.y = self._spawn_y
        req.theta = self._spawn_theta
        req.name = self._my_name
        
        future = client.call_async(req)
        future.add_done_callback(self._spawn_callback)

    def _spawn_callback(self, future):
        try:
            res = future.result()
            if res is not None:
                self.get_logger().info(f"Turtle '{self._my_name}' spawned successfully.")
            else:
                self.get_logger().warn(f"Turtle '{self._my_name}' may already exist or failed to spawn. Continuing.")
        except Exception as e:
            self.get_logger().warn(f"Spawn service call failed: {e}")

    def _my_pose_cb(self, msg):
        self._my_pose = msg
        
    def _target_pose_cb(self, msg):
        self._target_pose = msg

    def _control_loop(self):
        if self._my_pose is not None and self._target_pose is not None:
            lin, ang = self._logic.compute_cmd(
                self._my_pose.x, self._my_pose.y, self._my_pose.theta,
                self._target_pose.x, self._target_pose.y
            )
            
            cmd = Twist()
            cmd.linear.x = lin
            cmd.angular.z = ang
            self._cmd_pub.publish(cmd)
        else:
            self.get_logger().debug('Waiting for poses...', throttle_duration_sec=2.0)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleFollowerNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()