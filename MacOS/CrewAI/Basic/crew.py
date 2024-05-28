from crewai import Crew
from agents import reviewer, test_designer
from tasks import review,design

user_requirements = """
A claims adjudication system must support secure user authentication with role-based access, and multi-factor authentication.\n
It should allow electronic claim submissions with standardized forms and document validation. The system must enable automated\n
and manual claims processing, integration with payment systems for various payment methods, and robust reporting and analytics \n
capabilities. Communication features should include automated notifications and multi-channel support. Compliance with regulations, \n
data encryption, audit logging, and user-friendly interfaces are essential. Seamless integration with other enterprise systems and \n
scalability to handle high claim volumes are also critical requirements.
"""

crew = Crew(
    agents=[reviewer, test_designer],
    tasks=[review, design],
    verbose=2
)

result = crew.kickoff(inputs={"user_requirements": user_requirements})