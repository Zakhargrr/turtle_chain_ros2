# Turtle Chain ROS2

Пакет ROS 2, реализующий следование черепах друг за другом в симуляторе turtlesim

## Требования

- Ubuntu 20.04 / 22.04 / 24.04
- ROS 2 Humble / Iron / Jazzy
- Python 3.8+
- xterm (для запуска teleop в отдельном окне)

## Сборка
```bash
colcon build --packages-select turtle_follower
source install/setup.bash
```

## Генерация и запуск с N черепахами

### Сгенерировать launch-файл для 10 черепах
```bash
python3 src/turtle_follower/generate_launch.py 10
```
### Запустить сгенерированную конфигурацию
```bash
ros2 launch turtle_follower turtle_chain_launch.py
```
### Запуск с пользовательской скоростью ведомых черепах
```bash
ros2 launch turtle_follower turtle_chain_launch.py follower_speed:=2.0
```

## Использование

1. После запуска откроется окно симулятора с turtle1 в центре
2. Автоматически откроется отдельное окно xterm с узлом управления `turtle_teleop_key` — переключитесь на него и используйте стрелки для движения turtle1
3. Остальные черепахи (turtle2, turtle3 и т.д.) появятся с задержкой и начнут следовать друг за другом цепочкой
4. Ведомые черепахи автоматически останавливаются, оказавшись в пределах 0.6 м от цели
5. Для остановки нажмите `Ctrl+C` в терминале запуска