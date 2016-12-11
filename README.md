# Generating Valid Course Plans using CSPs
CS 182 Final Project / Jeffrey Chang, Tomoya Hasegawa

Each semester, every student at Harvard spends a significant amount of time selecting courses to take. Students must balance meeting their concentration requirements with the desire to take classes that appeal to them, all while selecting courses that do not conflict with each other. In our project, we hope to use artificial intelligence techniques to generate valid 4-year course plans for CS concentrators that satisfy both the concentration requirements and Harvard’s general education requirements, hopefully removing some of the stress that students have to face in selecting courses each semester. We will model this complex system of requirements and prerequisites using a Constraint Satisfaction Problem (CSP), and a variety of CSP solving techniques in order to produce valid schedules. 

- ScheduleGenerator.py: main code implementing the CSP solving algorithm
- Constraint.py: classes and functions modelling binary constraints
- solver.py: code to interface with user and process user preferences
- helpers.py: general helper functions used throughout the code
- *.csv: course data taken from CS50 Courses API
