from .approval_system import ApprovalSystem
from crew_implementation.utils.logging import logger
import os

class PlanManager:
    def __init__(self):
        # Initialize current_version to 0 if not set
        self.current_version = getattr(self, 'current_version', 0)
        self.slt_roles = ['CEO', 'CFO', 'COO', 'CTO', 'CMO', 'VP Sales']
        self.plan_data = self._load_plan_data()  # Initialize plan data
        self.approval_system = ApprovalSystem()
    
    def has_approved_plan(self):
        return self.approval_system.is_approved()
    
    def start_collaborative_planning(self):
        logger.info("Starting collaborative business plan creation")
        self._initialize_plan_structure()
        self._assign_sections_to_roles()
        self._collect_inputs()
        self._submit_for_approval()
    
    def view_plan(self):
        """View the current business plan with proper initialization checking"""
        if not self.plan_data or not isinstance(self.plan_data, dict):
            print("No valid plan data available. Please create or load a plan first.")
            logger.warning("Attempted to view plan with invalid or missing data")
            return
        
        try:
            print("\n=== Business Plan ===")
            for role, data in self.plan_data.items():
                if not isinstance(data, dict):
                    logger.warning(f"Invalid data format for role: {role}")
                    continue
                    
                print(f"\n## {role} Section")
                for section, content in data.items():
                    if section != 'teams':
                        if not content:
                            logger.debug(f"Empty content in {role} - {section}")
                        print(f"### {section}\n{content}")
                
                if 'teams' in data and isinstance(data['teams'], dict):
                    print("\n### Marketing Teams")
                    for team, team_data in data['teams'].items():
                        if not isinstance(team_data, dict):
                            logger.warning(f"Invalid team data format for {team}")
                            continue
                        print(f"#### {team}")
                        for section, content in team_data.items():
                            if not content:
                                logger.debug(f"Empty content in {team} - {section}")
                            print(f"{section}: {content}")
                        print()
        
        except Exception as e:
            print("Error displaying the business plan. Please check the plan data.")
            logger.error(f"Error in view_plan: {str(e)}")
            logger.debug(f"Plan data structure: {self.plan_data}")
    
    def _initialize_plan_structure(self):
        # Create initial plan template
        pass
    
    def _assign_sections_to_roles(self):
        """Assign plan sections to SLT roles"""
        self.sections = {
            'CEO': ['Executive Summary', 'Vision Statement'],
            'CFO': ['Financial Framework', 'Budget Allocation'],
            'CMO': {
                'main': ['Market Analysis', 'Marketing Strategy'],
                'teams': {
                    'Market Research': [
                        'Competitor Analysis',
                        'Trend Analysis',
                        'Customer Segmentation'
                    ],
                    'Digital Marketing': [
                        'SEO Strategy',
                        'PPC Campaigns',
                        'Email Marketing Plan'
                    ],
                    'Social Media': [
                        'Content Calendar',
                        'Engagement Strategy',
                        'Influencer Partnerships'
                    ],
                    'Content Marketing': [
                        'Blog Strategy',
                        'Video Content Plan',
                        'Lead Magnet Development'
                    ]
                }
            },
            'CTO': ['Technology Roadmap'],
            'COO': ['Operations Plan', 'Risk Assessment'],
            'VP Sales': ['Revenue Model', 'Target Segments']
        }
        logger.info("Plan sections assigned to SLT roles")
    
    def _collect_inputs(self):
        """Collect inputs from SLT members"""
        self.plan_data = {}
        
        for role, sections in self.sections.items():
            print(f"\n{role} Input:")
            if isinstance(sections, dict):  # Handle CMO's team structure
                self.plan_data[role] = {}
                # Collect main sections
                for section in sections['main']:
                    self.plan_data[role][section] = input(f"{section}: ")
                # Collect team sections
                self.plan_data[role]['teams'] = {}
                for team, team_sections in sections['teams'].items():
                    self.plan_data[role]['teams'][team] = {}
                    for section in team_sections:
                        self.plan_data[role]['teams'][team][section] = input(f"{team} - {section}: ")
            else:
                self.plan_data[role] = {}
                for section in sections:
                    self.plan_data[role][section] = input(f"{section}: ")
            
            logger.info(f"Collected input from {role}")
    
    def _submit_for_approval(self):
        """Handle approval workflow with CMO oversight"""
        print("\n=== Marketing Team Oversight ===")
        print("CMO Review Checklist:")
        print("1. Verify all team inputs are complete")
        print("2. Ensure alignment with overall marketing strategy")
        print("3. Check dependencies between teams")
        print("4. Review budget allocations")
        print("5. Approve final marketing plan")
        
        # Track CMO's review status
        self.approval_system.track_review('CMO', 'Marketing Plan')
        logger.info("CMO review process initiated")
    
    def _get_latest_version(self):
        # Implement version tracking
        return None
    
    def _get_team_lead(self, team):
        """Get team lead for each marketing sub-team"""
        team_leads = {
            'Market Research': 'Research Manager',
            'Digital Marketing': 'Digital Marketing Manager',
            'Social Media': 'Social Media Manager',
            'Content Marketing': 'Content Manager'
        }
        return team_leads.get(team, 'Team Lead')
    
    def save_plan(self, version):
        """Save the plan to a file"""
        plan_path = f"docs/business_plans/leadership_plan_v{version}.txt"
        os.makedirs(os.path.dirname(plan_path), exist_ok=True)
        
        with open(plan_path, 'w') as f:
            f.write("# Leadership Destination Business Plan\n\n")
            for role, data in self.plan_data.items():
                f.write(f"## {role} Section\n")
                if isinstance(data, dict):
                    for section, content in data.items():
                        if section != 'teams':
                            f.write(f"### {section}\n{content}\n\n")
                    if 'teams' in data:
                        f.write("### Marketing Teams\n")
                        for team, team_data in data['teams'].items():
                            f.write(f"#### {team}\n")
                            for section, content in team_data.items():
                                f.write(f"{section}: {content}\n")
                            f.write("\n")
        
        logger.info(f"Plan saved to {plan_path}")
        return plan_path

    def generate_plan(self):
        """Generate the final business plan"""
        version = self._get_next_version()
        plan_path = self.save_plan(version)
        
        print(f"\nBusiness plan generated successfully!")
        print(f"Location: {plan_path}")
        logger.info(f"Generated plan version {version}")
        
        return plan_path

    def _get_next_version(self):
        """Get the next version number"""
        version = 1
        while os.path.exists(f"docs/business_plans/leadership_plan_v{version}.txt"):
            version += 1
        return version

    def _load_plan_data(self):
        """Load existing plan data if available"""
        if self.current_version > 0:
            plan_path = f"docs/business_plans/leadership_plan_v{self.current_version}.txt"
            if os.path.exists(plan_path):
                return self._parse_plan_file(plan_path)
        return None
    
    def _parse_plan_file(self, file_path):
        """Parse the plan file into structured data"""
        plan_data = {}
        current_role = None
        current_team = None
        current_section = None
        
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('## '):  # Role section
                    current_role = line[3:].strip()
                    plan_data[current_role] = {}
                    current_team = None
                    current_section = None
                elif line.startswith('### '):  # Section or team
                    current_section = line[4:].strip()
                    if current_team:
                        if current_section not in plan_data[current_role]['teams'][current_team]:
                            plan_data[current_role]['teams'][current_team][current_section] = ''
                    else:
                        if current_section not in plan_data[current_role]:
                            plan_data[current_role][current_section] = ''
                    current_team = None
                elif line.startswith('#### '):  # Team subsection
                    current_team = line[5:].strip()
                    if 'teams' not in plan_data[current_role]:
                        plan_data[current_role]['teams'] = {}
                    if current_team not in plan_data[current_role]['teams']:
                        plan_data[current_role]['teams'][current_team] = {}
                    current_section = None
                elif line:  # Content
                    if current_team and current_section:
                        if plan_data[current_role]['teams'][current_team][current_section]:
                            plan_data[current_role]['teams'][current_team][current_section] += '\n' + line
                        else:
                            plan_data[current_role]['teams'][current_team][current_section] = line
                    elif current_section:
                        if plan_data[current_role][current_section]:
                            plan_data[current_role][current_section] += '\n' + line
                        else:
                            plan_data[current_role][current_section] = line
        return plan_data 