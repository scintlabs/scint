import time
from typing import Dict, List, Any

from services.openai import openai_assistants, openai_threads, openai_files
from services.logger import log
from core.config import GPT4


class File:
    def __init__(self, filepath) -> None:
        return openai_files.create(file=open(filepath, "rb"), purpose="assistants")


class Message:
    def __init__(self) -> None:
        self.id: str

    def create_message(thread_id, content):
        message = openai_threads.messages.create(
            role="user", thread_id=thread_id, content=content
        )
        message_id = message.id
        return message_id


class Thread:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id")
        self.messages: List[Dict[str, Any]] = kwargs.get("messages")
        self.metadata: Dict[str, str] = {}

    def create(self, messages):
        return openai_threads.create(messages=messages)

    def run(self, assistant_id):
        self.assistant_id = assistant_id
        return openai_threads.runs.create(self.id, self.assistant_id)


class Assistant:
    def __init__(self):
        log.info(f"Assistant: initializing self.")

        self.assistant = openai_assistants.retrieve("asst_clbdRWE3P83OAcalUwHXaS7g")
        self.thread = openai_threads.retrieve("thread_hzoajppRCt0sOtL5C7eU61IR")

    def process_request(self, request):
        log.info(request)
        content = request.get("content")
        self.create_message(self.thread.id, content)
        run = openai_threads.runs.create(
            thread_id=self.thread.id, assistant_id=self.assistant.id
        )
        count = 0

        while run.status != "completed" and count < 20:
            time.sleep(1)
            run = openai_threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
            count += 1
            log.info(run)

        messages = openai_threads.messages.list(thread_id=self.thread.id, order="desc")

        message_data = messages.data[0]
        message = openai_threads.messages.retrieve(
            thread_id=self.thread.id, message_id=message_data.id
        )
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []

        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f" [{index}]"
            )

            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = openai_files.retrieve(file_citation.file_id)
                citations.append(
                    f"[{index}] {file_citation.quote} from {cited_file.filename}"
                )

            elif file_path := getattr(annotation, "file_path", None):
                cited_file = openai_files.retrieve(file_path.file_id)
                citations.append(
                    f"[{index}] Click <here> to download {cited_file.filename}"
                )

        message_content.value += "\n" + "\n".join(citations)

        return {"content": message_content.value}

    def create_message(self, thread_id, content):
        message = openai_threads.messages.create(
            role="user", thread_id=thread_id, content=content
        )
        message_id = message.id
        return message_id
