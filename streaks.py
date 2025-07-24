from task_manager import calculate_streak

def get_streak_badge():
    streak = calculate_streak()
    
    if streak >= 7:
        badge = "🧙 Focus Wizard"
    elif streak >= 3:
        badge = "🥷 Time Ninja"
    elif streak >= 1:
        badge = "🔥 Getting Started"
    else:
        badge = "🌀 No Streak Yet"

    return streak, badge
