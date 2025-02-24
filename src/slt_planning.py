from crew_implementation.business_plan.plan_manager import PlanManager
from crew_implementation.utils.logging import logger

def main():
    print("Leadership Destination - Business Planning System")
    print("Senior Leadership Team Access Only\n")
    
    plan_manager = PlanManager()
    
    if not plan_manager.has_approved_plan():
        print("No approved business plan found. Let's create one!")
        plan_manager.start_collaborative_planning()
    else:
        print("Current approved plan exists. Viewing mode only.")
        plan_manager.view_plan()

if __name__ == "__main__":
    main() 