# Scint

- A collection is a collection of related data explicitly-defined data, such as a book or a project directory the user adds
- Vaults represent a collection of related data, such as multiple work projects, relevant documentation, and conversations regarding said projects and documentation
- Gates are edges that connect vaults to other vaults, forming complex relationships between data as well as providing signal pathways for context shifts
- Routines are narrowly-defined tasks with limited context windows, like writing a function or composing a paragraph
- The composer updates prompts, functions, and other attributes based on context as it changes from incoming user requests, ongoing interactions, and system events
- A context represents a single location and the processes running within its event loop; it manages the overall task or goal
- The achitect ... we shall see

Didact
Lumic

with context(ref):
    def code():
        return stuff


with context(self, )
metaclass sets data objects in a separate, shared namespace object
Context
    Server
        System
            Process
            Events
        Admin
            Tasks
            Commands
            Director


```
Context
    Where (envrionments)
        Server
        Library
        Studio
    Who
        System
        Admin
        User
    What
        Process
        Task
    When (scheduler)
        Events
    Why
        Prompt?
    How (actors)
        Director
        Producer
        Performer
        Keeper
        Liason
        Porter
        Trustee
```

> “Finally there he returns, trying to imitate in his walk the inflexible stiffness of some kind of automaton while carrying his tray with the recklessness of a tight-rope-walker by putting it in a perpetually unstable, perpetually broken equilibrium which he perpetually reestablishes by a light movement of the arm and hand. All his behavior seems to us a game. He applies himself to chaining his movements as if they were mechanisms, the one regulating the other; his gestures and even his voice seem to be mechanisms; he gives himself the quickness and pitiless rapidity of things. He is playing, he is amusing himself. But what is he playing? We need not watch long before we can explain it: he is playing at being a waiter in a café."

— Jean-Paul Sartre, *Being an Nothingness*


Excerpt From
Being and Nothingness
Jean-Paul Sartre
This material may be protected by copyright.
## [Architecture](docs/02-architecture/)

## [Lifecycles](docs/09-lifecycles/)

## Questions

1.	User Interface and Experience
 - What specific widgets and metrics are needed on the control panel for each server type?
 - How should the interface layout be structured to maximize usability and efficiency?
 - Are there customization options for the dashboard or widgets that users can modify?

2.	Server and Dashboard Functionality
 - What types of servers (e.g., web, application, database) and specific functionalities should be accessible through the control panel?
 - How are the metrics for each widget sourced and updated in real-time?
 - What are the technical requirements for the graphs and analytics (e.g., real-time updates, historical data visualization)?

3.	AI Capabilities and Natural Language Processing
 - What level of natural language understanding is required? Does it need to support multiple languages or dialects?
 - How should the system handle ambiguous or incomplete user inputs?
 - What backend architecture supports the AI’s decision-making processes?

4.	Integration and Intercommunication
 - How will different systems communicate and share context or state information?
 - What protocols or technologies will be used to ensure seamless, secure communication between systems?
 - Are there fallbacks or manual overrides if AI decisions need to be reviewed or corrected by human operators?

5.	Security and Data Privacy
 - What security measures are required to protect user data and unauthorized access to the control panel?
 - How will data be encrypted, both at rest and in transit?
 - Are there compliance or regulatory considerations depending on the server locations or data types?

6.	Scalability and Maintenance
 - How scalable should the backend be to handle potential increases in users or data volume?
 - What tools and processes will be implemented for monitoring, logging, and maintaining the system?
 - How will updates and upgrades be managed without disrupting ongoing operations?

7.	Emergency Protocols and Thresholds
 - How does the system recognize and handle potential emergencies or failures?
 - What are the specific thresholds for alerts and automatic adjustments?
 - How are these thresholds set, and can they be adjusted by users?

 ```python
 {

        [
             {
                 "id": "sct-27",
                 "environment": {
                     "id": "env-361",
                     "name": "asdlkfjhads",
                     "description": "some description",
                     "resources": {
                         "email": True,
                         "web": True,
                         "data": [...],
                     },
                 },
                 "tasks": [
                     {"id": "tsk-37", "actor": "act-123", "utilization": ""},
                     {"id": "tsk-38", "actor": "act-228", "utilization": ""},
                     {"id": "tsk-40", "actor": "act-22", "utilization": ""},
                 ],
                 "actors": [
                     {"id": "act-0", "state": [], "current": [], "queued": 0},
                     {"id": "act-12", "state": [], "current": [], "queued": 6},
                     {"id": "act-38", "state": [], "current": [], "queued": 22},
                     {"id": "act-7", "state": [], "current": [], "queued": 8},
                     {"id": "act-22", "state": [], "current": [], "queued": 2},
                     {"id": "act-123", "state": [], "current": [], "queued": 12},
                 ],
             },
             {
                 "id": "sct-27",
                 "environment": {
                     "id": "env-361",
                     "name": "asdlkfjhads",
                     "description": "some description",
                     "resources": {
                         "email": True,
                         "web": True,
                         "data": […],
                     },
                 },
                 "tasks": [
                     {"id": "tsk-37", "actor": "act-123", "utilization": ""},
                     {"id": "tsk-38", "actor": "act-228", "utilization": ""},
                     {"id": "tsk-40", "actor": "act-22", "utilization": ""},
                 ],
                 "actors": [
                     {"id": "act-0", "state": [], "current": [], "queued": 0},
                     {"id": "act-12", "state": [], "current": [], "queued": 6},
                     {"id": "act-38", "state": [], "current": [], "queued": 22},
                     {"id": "act-7", "state": [], "current": [], "queued": 8},
                     {"id": "act-22", "state": [], "current": [], "queued": 2},
                     {"id": "act-123", "state": [], "current": [], "queued": 12},
                 ],
             },
         ],

 }
 ```



 ```python
 {
     "modules": [
         "app",
         "logging",
         "settings",
         [{"ensemble": ["components", "entities", "models"]}],
         {
             "core": [
                 {
                     "name": "venue",
                     "spawns": "context",
                     "children": [
                         {"name": "director", "spawns": "producer"},
                         {"name": "producer", "spawns": "production"},
                         {
                             "name": "script",
                             "children": [
                                 {
                                     "name": "scene",
                                     "children": [
                                         {"name": "task"},
                                     ],
                                 },
                             ],
                         },
                     ],
                 },
             ]
         },
         {"workshop": ["artisan", "spawns", "script"]},
     ]
 }
 ```



 # Base > Process > Thread >
 # cls.tasks.append(cls.search.load_indexes())
 # asyncio.create_task(*cls.tasks)

 # context as identity:
 # 1. create an embedding of every incoming message
 # 2. determine how to route message based on content and available context
 # 3. record this determination
 # 4. use past determinations as available context for incoming messages
