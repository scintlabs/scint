# class Processes:
#     def __init__(self, processes: List[Process] = None):
#         if processes is None:
#             processes = []

#         self._processes = processes

#     def __iter__(self):
#         return iter(self._processes)

#     def load(self, *processes):
#         for process in processes:
#             if process.name not in [p.name for p in self._processes]:
#                 self._processes.append(process)

#     def unload(self, process_name):
#         self._processes = [process for process in self._processes if process.name != process_name]

#     def get(self, process_name):
#         return next(
#             (process for process in self._processes if process.name == process_name),
#             None,
#         )


# class Processes:
#     def __init__(self, processes: List[Process] = None):
#         if processes is None:
#             processes = []

#         self._processes = processes

#     def __iter__(self):
#         return iter(self._processes)

#     def load(self, *processes):
#         for process in processes:
#             if process.name not in [p.name for p in self._processes]:
#                 self._processes.append(process)

#     def unload(self, process_name):
#         self._processes = [
#             process for process in self._processes if process.name != process_name
#         ]

#     def get(self, process_name):
#         return next(
#             (process for process in self._processes if process.name == process_name),
#             None,
#         )


# class Select(Process):
#     description = "You are a web search selection process. For every message, select the website that best matches the search query."

#     def initialize_workers(self):
#         self.workers.add(SelectSearchResult())


# class Load(Process):
#     description = "You are a website loading process. For every message, load the appropriate data for the search query."

#     def initialize_workers(self):
#         pass


# class Parse(Process):
#     description = "You are a data parsing process. For every message you receive, generate a contextually rich summary."

#     def initialize_workers(self):
#         self.workers.add(SummarizeData())
