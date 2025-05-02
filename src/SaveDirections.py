# src/SaveDirections.py

import json
import sys
import os
import numpy as np
import math
import time

# --- 添加项目根目录到 Python 路径 ---
# 这使得脚本可以找到 training 和 elements 包
# 根据你的项目结构调整 '../..' 可能需要变成 '..' 或其他
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
# ------------------------------------

# --- 导入必要的类 ---
# 假设 PacmanOfReseauNeuron 在 training 包下
# 并且 TrainingGame 也在 training 包下
# 如果不在，请调整导入路径
try:
    # 尝试从 training 包导入
    from training.pacmanAI import PacmanOfReseauNeuron
    from training.training_AIs import TrainingGame # TrainingGame 包含 evaluate_ai 等需要的内容
    from elements.dot import Dot # TrainingGame 可能间接需要
    from elements.bigDot import BigDot # TrainingGame 可能间接需要
except ImportError:
    print("Error: Could not import necessary classes.")
    print("Ensure PacmanOfReseauNeuron and TrainingGame are in the 'training' directory")
    print("and elements (Dot, BigDot) are in the 'elements' directory relative to the project root.")
    print(f"Project root added to path: {project_root}")
    sys.exit(1)
# ---------------------


def load_ai_from_json(json_filepath, ai_id):
    """
    从指定的 JSON 文件加载特定 ID 的 AI 权重。

    Args:
        json_filepath (str): 包含 AI 数据（包括权重）的 JSON 文件路径。
        ai_id (int): 要加载的 AI 的 ID。

    Returns:
        PacmanOfReseauNeuron: 加载了权重的 AI 实例。
        int: AI 在原始训练中的得分 (如果找到)。
        int: AI 在原始训练中的步数 (如果找到)。
        None: 如果找不到指定 ID 的 AI。
    """
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_filepath}")
        return None, None, None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_filepath}")
        return None, None, None

    target_ai_data = None
    for ai_result in data.get("ai_results", []):
        if ai_result.get("id") == ai_id:
            target_ai_data = ai_result
            break

    if not target_ai_data:
        print(f"Error: AI with ID {ai_id} not found in {json_filepath}")
        return None, None, None

    # 创建 AI 实例 (使用原始代码中的默认结构)
    # *** 重要提示 ***:
    # 这里的 PacmanOfReseauNeuron() 初始化会使用默认的 input_size, hidden_layers, output_size。
    # 必须确保 JSON 文件中的权重结构与这些默认值 *完全匹配*。
    # 如果你的 JSON 文件是针对不同网络结构（例如 PacmanOfReseauNeuronOneLayer 或 ThreeLayer）训练的，
    # 你需要在这里实例化正确的类，或者修改 PacmanOfReseauNeuron 使其更灵活。
    # 我们假设 JSON 文件对应的是 PacmanOfReseauNeuron 的结构 (input=14, hidden=[20,10], output=4)。
    try:
        ai_agent = PacmanOfReseauNeuron() # 或者 PacmanOfReseauNeuronOneLayer/ThreeLayer 如果 JSON 对应那个结构

        # 验证加载的层数是否匹配
        if len(target_ai_data["network_weights"]) != len(ai_agent.network_weights):
             print(f"Error: Mismatch in number of layers between loaded weights ({len(target_ai_data['network_weights'])}) and AI class ({len(ai_agent.network_weights)}).")
             print("Ensure the correct AI class (PacmanOfReseauNeuron, OneLayer, ThreeLayer) is instantiated based on the JSON file.")
             return None, None, None

        loaded_weights = []
        for i, layer_weights_list in enumerate(target_ai_data["network_weights"]):
            try:
                # 将列表转换回 NumPy 数组
                layer_weights_np = np.array(layer_weights_list, dtype=np.float64) # 使用 float64 匹配 np.random.uniform

                # 验证形状是否匹配
                expected_shape = ai_agent.network_weights[i].shape
                if layer_weights_np.shape != expected_shape:
                    print(f"Error: Shape mismatch for layer {i}.")
                    print(f"  Expected shape: {expected_shape}")
                    print(f"  Loaded shape: {layer_weights_np.shape}")
                    print("Ensure the JSON weights correspond exactly to the network structure defined in the AI class.")
                    return None, None, None

                loaded_weights.append(layer_weights_np)

            except ValueError as e:
                print(f"Error converting weights for layer {i} to NumPy array: {e}")
                return None, None, None

        # 将加载并验证过的权重赋值给 AI 实例
        ai_agent.network_weights = loaded_weights

        original_score = target_ai_data.get("score", "N/A")
        original_steps = target_ai_data.get("steps", "N/A")

        print(f"Successfully loaded AI ID {ai_id} with original score: {original_score}, steps: {original_steps}")
        return ai_agent, original_score, original_steps

    except Exception as e:
        print(f"An error occurred during AI instantiation or weight loading: {e}")
        return None, None, None


def run_simulation_and_record_actions(ai_agent, max_steps=100000):
    """
    使用给定的 AI 运行一次游戏模拟，并记录每一步的动作。

    Args:
        ai_agent (PacmanOfReseauNeuron): 已加载权重的 AI 实例。
        max_steps (int): 模拟的最大步数限制。

    Returns:
        list: 记录下的动作序列 (e.g., ['U', 'R', 'R', 'D', ...])。
        int: 模拟结束时的最终得分。
        int: 模拟的总步数。
    """
    if ai_agent is None:
        print("Error: Cannot run simulation with None AI agent.")
        return [], 0, 0

    game = TrainingGame(ai_agent=ai_agent, max_steps=max_steps) # 使用无头模式
    game.resetGameState()

    game.last_position = (game.player.x, game.player.y)
    game.frames_stuck = 0

    recorded_actions = []
    step = 0

    print(f"Starting simulation for AI...") # Add AI ID if available

    while game.isRunning and step < game.max_steps:
        state = game.get_game_state()
        action = ai_agent.getDecision(state) # AI 做决策

        recorded_actions.append(action) # 记录决策

        game.player.setDirection(action) # 应用决策
        game.update() # 更新游戏状态
        game.dontMove360() # 检查卡住状态

        step += 1
        if step % 1000 == 0: # 每 1000 步打印一次进度
             print(f"  Step: {step}, Current Score: {game.score}")

        # 可选：如果需要调试，可以取消注释以下行
        # print(f"Step {step}: State sample = {state[:3]}..., Action = {action}, Score = {game.score}")

    final_score = game.score
    total_steps = step
    print(f"Simulation finished. Final Score: {final_score}, Total Steps: {total_steps}")

    return recorded_actions, final_score, total_steps

def save_recorded_actions(ai_id, original_score, original_steps, actions, final_score, total_steps, output_filepath):
    """
    将记录的动作、得分和步数保存到 JSON 文件。

    Args:
        ai_id (int): 被模拟的 AI 的 ID。
        original_score (int/str): AI 在原始训练中的得分。
        original_steps (int/str): AI 在原始训练中的步数。
        actions (list): 记录的动作序列。
        final_score (int): 模拟得到的最终得分。
        total_steps (int): 模拟的总步数。
        output_filepath (str): 保存结果的 JSON 文件路径。
    """
    data_to_save = {
        "ai_id": ai_id,
        "original_score_from_training": original_score,
        "original_steps_from_training": original_steps,
        "simulation_final_score": final_score,
        "simulation_total_steps": total_steps,
        "recorded_actions": actions
    }

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)
        print(f"Successfully saved recorded actions for AI {ai_id} to {output_filepath}")
    except IOError as e:
        print(f"Error saving actions to {output_filepath}: {e}")
    except TypeError as e:
        print(f"Error serializing data to JSON: {e}")


if __name__ == "__main__":
    # --- 配置 ---
    # 输入 JSON 文件路径 (包含训练好的 AI 权重)
    # **确保这个路径相对于 SaveDirections.py 是正确的**
    # 假设 couche_2middle_json.json 与 SaveDirections.py 在同一目录或上一级目录等
    input_json_file = os.path.join(script_dir, "couche_2_middle.json") # 假设在同一目录下
    # input_json_file = os.path.join(project_root, "data", "couche_2middle_json.json") # 或者在项目根目录的 data 子目录下

    # 要加载和模拟的 AI 的 ID (来自 JSON 文件中的 "id" 字段)
    target_ai_id_to_run = 1 # 修改为你想要运行的 AI 的 ID

    # 输出 JSON 文件路径 (用于保存记录的动作)
    output_json_file = os.path.join(script_dir, f"recorded_actions_ai_{target_ai_id_to_run}.json")

    # 模拟的最大步数 (与训练时匹配或根据需要调整)
    simulation_max_steps = 100000
    # ------------

    print("--- Starting AI Action Recording ---")
    print(f"Input Weights JSON: {input_json_file}")
    print(f"Target AI ID: {target_ai_id_to_run}")
    print(f"Output Actions JSON: {output_json_file}")

    # 1. 加载指定 AI 的权重
    loaded_ai, orig_score, orig_steps = load_ai_from_json(input_json_file, target_ai_id_to_run)

    if loaded_ai:
        # 2. 运行模拟并记录动作
        actions, score, steps = run_simulation_and_record_actions(loaded_ai, simulation_max_steps)

        # 3. 保存记录的结果
        if actions: # 确保模拟实际运行并产生了动作
             save_recorded_actions(
                 ai_id=target_ai_id_to_run,
                 original_score=orig_score,
                 original_steps=orig_steps,
                 actions=actions,
                 final_score=score,
                 total_steps=steps,
                 output_filepath=output_json_file
             )
        else:
            print("Simulation did not produce any actions to save.")
    else:
        print(f"Could not load AI with ID {target_ai_id_to_run}. Aborting.")

    print("--- Action Recording Script Finished ---")