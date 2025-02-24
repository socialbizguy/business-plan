import os
from crew_implementation.utils.logging import logger

class ApprovalSystem:
    def __init__(self):
        self.approval_path = "docs/approvals/slt_signoff.md"
        self.approvers = {}  # Initialize approvers here
        self.review_status = {}  # Initialize review status here
    
    def is_approved(self):
        """Check if all required approvals are granted"""
        return all(self.approvers.values())
    
    def request_approval(self, plan_version):
        """Manage the approval workflow"""
        self.current_plan = f"leadership_plan_v{plan_version}.txt"
        # Reset approvers for new plan version with all required roles
        self.approvers = {
            'CEO': False,
            'CFO': False,
            'CTO': False,
            'COO': False,
            'VP Sales': False
        }
        
        print("\n=== Approval Process ===")
        print("Please have the following members review and approve:")
        for approver in self.approvers.keys():
            self._request_approval_from(approver)
        
        logger.info(f"Approval process started for {self.current_plan}")

    def _request_approval_from(self, role):
        """Request approval from a specific role"""
        if not hasattr(self, 'current_plan') or not self.current_plan:
            print("Error: No plan version selected for approval")
            self.approvers[role] = False
            logger.error(f"Attempted to request approval without setting current_plan for role: {role}")
            return
            
        print(f"\n{role} Approval:")
        try:
            with open(f"docs/business_plans/{self.current_plan}", 'r') as file:
                plan_content = file.read()
                print("\n=== Plan Content ===")
                print(plan_content[:1000] + "..." if len(plan_content) > 1000 else plan_content)
        except FileNotFoundError:
            print("Plan content not available for review")
            self.approvers[role] = False
            return
            
        approval = input(f"Does {role} approve? (yes/no): ").lower()
        self.approvers[role] = approval == 'yes'
        logger.info(f"{role} approval status: {self.approvers[role]}")
    
    def get_approval_status(self):
        """Return current approval status based on approvers' decisions"""
        if not hasattr(self, 'approvers') or not self.approvers:
            return "Pending"
        
        if all(self.approvers.values()):
            return "Approved"
        elif any(self.approvers.values()):
            return "Partially Approved"
        else:
            return "Pending"
    
    def track_review(self, role, section):
        """Track progress of team reviews"""
        self.review_status[role] = {
            'section': section,
            'status': 'In Progress',
            'dependencies': self._get_dependencies(role)
        }
        logger.info(f"Tracking review for {role} on {section}")

    def _get_dependencies(self, role):
        """Get team dependencies for tracking"""
        dependencies = {
            'CMO': {
                'Market Research': 'Complete',
                'Content Marketing': 'Pending',
                'Digital Marketing': 'Pending',
                'Social Media': 'Pending'
            }
        }
        return dependencies.get(role, {}) 

    def view_approval_history(self):
        """View the approval history"""
        if not hasattr(self, 'current_plan'):
            print("No approval history available.")
            return
        
        print("\n=== Approval History ===")
        print(f"Plan: {self.current_plan}")
        for role, status in self.approvers.items():
            print(f"{role}: {'Approved' if status else 'Pending'}")
        
        if hasattr(self, 'review_status'):
            print("\nReview Status:")
            for role, status in self.review_status.items():
                print(f"{role} - {status['section']}: {status['status']}") 