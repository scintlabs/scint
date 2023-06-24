# Scratchpad

## Search engines

The schema of a search engine can be pretty complex, but it fundamentally centers on storing, indexing, and retrieving data efficiently and accurately. Let's break down the general conceptual components:

- **Crawling:** This is the process of collecting documents or webpages from the internet. The crawler, also known as a spider or bot, visits websites and downloads their content for further processing. The schema here might include fields for the URL of the webpage, the date and time it was last visited, its relationship to other pages (links), etc.
- **Indexing:** Once the pages are crawled, they need to be indexed. This involves processing the crawled data and creating a large data structure (the index) that allows for fast full-text searches. An indexing schema might include fields for every unique word (called a token) found in the documents, a list of documents each word appears in, the frequency of each word in each document, etc.
- **Ranking:** Ranking determines the order in which results are presented to the user based on a specific query. The ranking algorithm often relies on many factors, including the relevance of a webpage to the query, the popularity of the webpage, the user's personalization settings, etc. The schema here might include fields for each document's relevance score, its popularity score, etc.
- **Query Processing:** This part of the schema deals with handling user queries. It needs to parse and understand the query, interact with the index to find relevant documents, and then use the ranking algorithm to order them. The schema might include fields for the original user query, the parsed query, the final list of results, etc.
- **User Interface:** This part of the schema deals with presenting search results to the user, as well as handling user interactions like clicks and query modifications. The schema might include fields for each result's title, snippet, URL, etc., as well as fields for tracking user interactions.
- **Logging and Analytics:** Search engines often collect data on user interactions for the purposes of improving their services, ensuring security, or serving personalized content. The schema here might include fields for each user's ID, their query history, the results they clicked on, their session duration, etc.

Keep in mind that each of these components might actually be made up of several smaller databases, services, or microservices, each with their own schemas. Also, different search engines might use very different schemas depending on their specific needs and the technologies they're built on. For example, a search engine that specializes in academic papers might have a schema that includes fields for authors, citations, and publication dates, while a search engine for e-commerce might have fields for product categories, prices, and customer reviews.



## Memory

```
import json
def summarize():
    with open('core/nodes.json') as file:
        init = file["memory"]["summarize"]["system_prompt"]
        print(init)

summarize()
```

user message(string) -> chat interface(string) -> format(json) -> minify(json) -> tokenize -> context window check -> openai -> response
                        chat interface                   ==>                      memory interface                    api


Memory connects to the chat interface.
Memory collects every message that's processed. 

- For every new message
    - If the message contains prunable content
        - Extract content ->
    - Check buffer capacity
        - If the buffer is at capacity
            - Process summarizing function ->
        - Else
            - Buffer memory ->


# Scratch Pad

## Messages

# system = message

# message = role, message, name

## Prompt/Process config

# api_key

# ChatCompletions(model, max_tokens, temperature, top_p, n, stream, logprobs, echo, stop, presence_penalty, frequency_penalty, best_of, user)

# Completions(model, prompt, suffix, max_tokens, temperature, top_p, n, stream, logprobs, echo, stop, presence_penalty, frequency_penalty, best_of, user)

# classify

# system = "You are a classification algorithm for an artificial intelligence system. For every message, classify the message according to these categories:"## Objective?

```python
recursive_expansion = Process(
  system: 'string',
  assistant: 'string',
  config: [
    model: 'gpt-4',

  ]

)
```

Started with:

```
Create a Python command line app to leverage LLMs through OpenAI's API, which makes interlinking LLM outputs to other LLM outputs easy, providing a sandbox to test and research prompt engineering.
```

Ran recursive depth on it five times and ran all five outputs through recursive clarity and then narrative cohesion one time to produce this:

```
start_process = Process("You are the processing interface for an artificial intelligence system that's tasked with clarifying and contexualizing a user's request. For every message, write a single sentence which categorizes the request and provides an overview for the system's internal processes to follow while they complete the task.")

Design a Python command line application that effectively integrates OpenAI's API to interconnect LLM outputs, creating an optimal sandbox environment for testing and researching prompt engineering techniques. Consider key components and best practices when developing this app to ensure seamless integration with the OpenAI API, enabling users to experiment with LLM outputs and their connections while providing an enhanced user experience.

To create a cohesive and intuitive environment for users exploring LLM output interconnections and experimenting with various prompt engineering methods, focus on optimizing the app's architecture, user interface, and OpenAI API integration. Adhere to best practices in software development and user experience design by employing strategies and methodologies that guarantee a smooth, user-friendly platform tailored for efficient resource utilization.

Key aspects to consider include:

1. App Structure: Design a modular architecture that separates concerns like data processing, API communication, and user interaction. This will facilitate easy maintenance, updates, and scalability.
2. User Interface: Create a clear and concise command line interface that guides users through available options while minimizing input errors. Implement helpful error messages and usage instructions to enhance usability.
3. API Integration: Efficiently integrate the OpenAI API using well-structured code that handles authentication, request management, rate limiting, error handling, and response parsing.
4. Resource Management: Optimize resource usage by implementing caching mechanisms or parallel processing where appropriate to minimize redundant requests or computations.
5. Error Handling: Ensure robust error handling throughout the app to gracefully handle unexpected situations such as network issues or invalid inputs from users.
6. Documentation: Provide comprehensive documentation detailing installation instructions, usage guidelines, examples of use cases, troubleshooting tips, and any known limitations or caveats.
7. Testing & Validation: Develop unit tests covering critical functionality as well as integration tests simulating real-world scenarios to ensure reliability across different environments.

By focusing on these aspects during development of the Python command line app for interconnecting LLM outputs via OpenAI's API, you can create a seamless and intuitive environment that enables users to effectively explore LLM output connections and experiment with diverse prompt engineering approaches while maintaining high standards in software development and user experience design.
```

I then ran the same prompt through a recursive planning function to get a few tasks:

```
Subtask: Parse and validate command line arguments to configure the app's behavior and input parameters.
Subtask: Create a function to process and format the LLM outputs for easy interlinking with other LLM outputs.
Subtask: Implement error handling and user prompts to ensure a smooth user experience during testing and research.
Subtask: Design a user-friendly interface for inputting prompts and displaying LLM-generated responses.
Subtask: Integrate a method for users to easily modify and adjust prompt engineering techniques within the app.
Subtask: Implement a logging system to track user interactions, LLM outputs, and prompt engineering adjustments for analysis and improvement.
Subtask: Create a comprehensive user guide and documentation to help users understand the app's features, usage, and prompt engineering techniques.
Subtask: Test the app with various prompts and scenarios to ensure its functionality, usability, and effectiveness in leveraging LLM outputs.
```

I then ran them through a recursive sorting function three times:

```
Category: Command Line Arguments
- Parsing and validation
- App behavior configuration
- Input parameter management

Category: LLM Output Processing
- Output processing and formatting
- Interlinking with other LLM outputs

Category: Error Handling & User Prompts
- Smooth user experience assurance
- Support during testing and research phases

Category: Interface Design
- Development of a user-friendly interface
- Prompt inputting, response displaying

Category: Prompt Engineering Techniques Modification
 - Seamless integration for users within the app

Category: Logging System Implementation
 - Monitoring interactions, outputs, adjustments

Category: User Guide/Documentation Creation
 - Comprehensive guidance on features, usage, techniques

 Category: App Testing
  - Evaluation of functionality, usability, effectiveness
```

And then through recursive depth three more times and the sorting function one more time:

```
Category: Command Line Arguments
  - Parsing and validation
    - Implementing argument parser libraries
    - Ensuring correct input format and data types
  - App behavior configuration
    - Customizing app settings through command line options
    - Setting default values for unspecified arguments
  - Input parameter management
    - Handling optional and required parameters
  - Providing help messages for users

Category: LLM Output Processing
  - Output processing and formatting
   - Converting raw output into human-readable format
   - Customizing output display based on user preferences
   - Interlinking with other LLM outputs
   - Combining multiple outputs for a comprehensive analysis
   - Ensuring consistency in data representation across outputs

Category: Error Handling & User Prompts
   - Smooth user experience assurance
   – Implementing informative error messages
   – Graceful handling of unexpected situations
   – Support during testing and research phases
       – Debugging tools integration
       – Assisting users in identifying issues

Category: Interface Design
   – Development of a user-friendly interface
        – Utilizing best practices in UI/UX design
        – Ensuring accessibility for all users
   – Prompt inputting, response displaying
        – Efficient input methods implementation
        – Clear visualization of responses

Category: Prompt Engineering Techniques Modification
   — Seamless integration for users within the app
         — Adapting prompt engineering techniques to specific use cases
         — Enhancing user experience through tailored prompts

 Category: Logging System Implementation
     — Monitoring interactions, outputs, adjustments
          — Tracking user activity and system performance
          — Analyzing logs to identify areas for improvement

 Category: User Guide/Documentation Creation
      — Comprehensive guidance on features, usage, techniques
           — Detailed instructions for each feature
           — Providing examples and use cases
           — Frequently asked questions (FAQ) section

  Category: App Testing
       — Evaluation of functionality, usability, effectiveness
            — Conducting unit, integration, and system testing
            — Gathering user feedback for improvements
```

And finally, the newest edition to the recursive team: a recursive criticizer:

```
Critique:

1. Command Line Arguments:
     - Parsing and validation: Relying solely on argument parser libraries may limit customization options, and some libraries might not support all required features.
     - App behavior configuration: Setting default values for unspecified arguments can lead to unexpected behavior if the user is unaware of these defaults.
     - Input parameter management: Handling optional parameters could result in confusion when users forget to include them or mistakenly assume they are required.

2. LLM Output Processing:
     - Output processing and formatting: Converting raw output into a human-readable format may sacrifice precision or introduce errors during conversion.
     - Customizing output display based on user preferences might be time-consuming and challenging to implement effectively.

3. Error Handling & User Prompts:
     – Smooth user experience assurance: Informative error messages may still be confusing for non-technical users, leading to frustration.

4. Interface Design:
     – Development of a user-friendly interface: Ensuring accessibility for all users can be difficult due to varying needs and abilities among the target audience.

5. Prompt Engineering Techniques Modification:
     — Seamless integration within the app might require significant development effort, especially if existing prompt engineering techniques need substantial modification.

6. Logging System Implementation:
     — Monitoring interactions, outputs, adjustments: Collecting extensive logs could negatively impact system performance or raise privacy concerns among users.

7. User Guide/Documentation Creation:
     — Comprehensive guidance on features, usage, techniques: Creating detailed documentation can be time-consuming and may become outdated as new features are added or existing ones change over time.

8. App Testing
     — Evaluation of functionality, usability, effectiveness : Conducting thorough testing requires considerable resources (time/money), which could delay product release; however insufficient testing increases risk of undiscovered issues that affect end-users' experience
```

And then a recursive solution finder:

```
Creative Solutions:

1. Command Line Arguments:
     - Develop a custom argument parser that supports all required features and allows for greater customization.
     - Clearly document default values and provide an option to display them when running the app.
     - Implement a dynamic help system that shows users which parameters are optional and provides examples of correct usage.

2. LLM Output Processing:
     - Utilize a flexible output formatting system that can be easily customized to accommodate user preferences without sacrificing precision or introducing errors.
     - Offer multiple output display options, allowing users to choose the format that best suits their needs.

3. Error Handling & User Prompts:
     – Design error messages with clear language and actionable steps, making them more accessible for non-technical users.
     – Provide in-app guidance or tooltips to help users navigate through potential issues.

4. Interface Design:
     – Collaborate with accessibility experts and conduct user testing with diverse groups to ensure the interface meets the needs of all users.

5. Prompt Engineering Techniques Modification:
     — Break down the integration process into smaller tasks, allowing for incremental improvements while minimizing disruption to existing functionality.

6. Logging System Implementation:
     — Implement an efficient logging system that minimizes performance impact and allows users to opt-out if they have privacy concerns.
     — Anonymize collected data where possible to further protect user privacy.

7. User Guide/Documentation Creation:
     — Keep documentation modular and easy to update as new features are added or existing ones change.
     — Consider creating video tutorials or interactive guides alongside written documentation for different learning styles.

8. App Testing
    — Prioritize critical functionality during testing, focusing on areas most likely to impact end-users' experience.
    — Employ automated testing tools where possible, reducing manual effort while increasing test coverage.
    — Encourage beta testing among target audience members, gathering valuable feedback before full release.
```

I went back and forth three or four times, and I think there's something to this process. The last iteration landed me here:

```
1. Command Line Arguments:
    - Flaws: Lightweight libraries may not cover all edge cases or complex scenarios, potentially limiting functionality. Machine learning algorithms for autocomplete suggestions could be resource-intensive and slow down the user experience.

2. LLM Output Processing:
    - Flaws: User-friendly configuration systems can become overly complex, leading to confusion and difficulty in customization. Regularly updating design guidelines might cause inconsistencies in output formats over time.

3. Error Handling & User Prompts:
    – Flaws: Optimizing machine learning techniques may require significant computational resources and still not guarantee perfect results. A well-organized help system could become outdated quickly if not maintained regularly.

4. Interface Design:
    – Flaws: Consistent design principles might stifle creativity or lead to a monotonous user experience. Ensuring compatibility across devices and platforms through rigorous testing can be time-consuming and costly.

5. Prompt Engineering Techniques Modification:
   — Flaws: Balancing agile methodologies with long-term planning can result in conflicts between short-term goals and overarching objectives, potentially causing delays or inefficiencies.

6. Logging System Implementation:
   — Flaws: Intelligent logging systems that dynamically adjust data collection based on context may miss important information due to misinterpretation of contextual cues; robust data anonymization techniques might inadvertently remove valuable insights during analysis.

7.User Guide/Documentation Creation
  —Flaws : Well-structured documentation frameworks can still become unwieldy as sections are added or removed; automation tools for creating multiple documentation formats may introduce errors or inconsistencies if not carefully managed.

8.App Testing
  —Flaw : Risk-based testing approaches might overlook less critical features that impact user satisfaction; relying on automated testing tools without sufficient manual oversight could lead to undiscovered issues slipping through the cracks; community-driven beta testing programs or crowdsourced platforms risk exposing sensitive information about your application before it's officially released
```

That said, I'm missing a LOT since I was deleting the previous message on every iteration. If I narrowed the scope to only one of these categories and sent it back and forth, between these two prompts while retaining context, things could get interesting.

You are a recursive function for an artificial intelligence system. For every critique or apparent flaw, you produce a creative solution.

You are narrative cohesion function for an artificial intelligence system. For every message, maintain complexity and content but rewrite for narrative cohesion.
