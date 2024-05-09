api_fine_tuning = {
    "create_fine_tuning_job": {
        "url": "https://api.openai.com/v1/fine_tuning/jobs",
        "description": "Creates a fine-tuning job which begins the process of creating a new model from a given dataset.",
        "request_body": {
            "model": {
                "type": "string",
                "required": True,
                "description": "The name of the model to fine-tune. You can select one of the supported models.",
            },
            "training_file": {
                "type": "string",
                "required": True,
                "description": "The ID of an uploaded file that contains training data.",
            },
            "hyperparameters": {
                "type": "object",
                "optional": True,
                "description": "The hyperparameters used for the fine-tuning job.",
            },
            "suffix": {
                "type": "string or null",
                "optional": True,
                "default": None,
                "description": "A string of up to 18 characters that will be added to your fine-tuned model name.",
            },
            "validation_file": {
                "type": "string or null",
                "optional": True,
                "description": "The ID of an uploaded file that contains validation data.",
            },
            "integrations": {
                "type": "array or null",
                "optional": True,
                "description": "A list of integrations to enable for your fine-tuning job.",
            },
            "seed": {
                "type": "integer or null",
                "optional": True,
                "description": "The seed controls the reproducibility of the job.",
            },
        },
        "returns": "A fine-tuning.job object.",
    },
    "list_fine_tuning_jobs": {
        "url": "https://api.openai.com/v1/fine_tuning/jobs",
        "description": "List your organization's fine-tuning jobs",
        "query_parameters": {
            "after": {
                "type": "string",
                "optional": True,
                "description": "Identifier for the last job from the previous pagination request.",
            },
            "limit": {
                "type": "integer",
                "optional": True,
                "default": 20,
                "description": "Number of fine-tuning jobs to retrieve.",
            },
        },
        "returns": "A list of paginated fine-tuning job objects.",
    },
    "list_fine_tuning_events": {
        "url": "https://api.openai.com/v1/fine_tuning/jobs/{fine_tuning_job_id}/events",
        "description": "Get status updates for a fine-tuning job.",
        "path_parameters": {
            "fine_tuning_job_id": {
                "type": "string",
                "required": True,
                "description": "The ID of the fine-tuning job to get events for.",
            }
        },
        "query_parameters": {
            "after": {
                "type": "string",
                "optional": True,
                "description": "Identifier for the last event from the previous pagination request.",
            },
            "limit": {
                "type": "integer",
                "optional": True,
                "default": 20,
                "description": "Number of events to retrieve.",
            },
        },
        "returns": "A list of fine-tuning event objects.",
    },
    "list_fine_tuning_checkpoints": {
        "url": "https://api.openai.com/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints",
        "description": "List checkpoints for a fine-tuning job.",
        "path_parameters": {
            "fine_tuning_job_id": {
                "type": "string",
                "required": True,
                "description": "The ID of the fine-tuning job to get checkpoints for.",
            }
        },
        "query_parameters": {
            "after": {
                "type": "string",
                "optional": True,
                "description": "Identifier for the last checkpoint ID from the previous pagination request.",
            },
            "limit": {
                "type": "integer",
                "optional": True,
                "default": 10,
                "description": "Number of checkpoints to retrieve.",
            },
        },
        "returns": "A list of fine-tuning checkpoint objects for a fine-tuning job.",
    },
    "retrieve_fine_tuning_job": {
        "url": "https://api.openai.com/v1/fine_tuning/jobs/{fine_tuning_job_id}",
        "description": "Get info about a fine-tuning job.",
        "path_parameters": {
            "fine_tuning_job_id": {
                "type": "string",
                "required": True,
                "description": "The ID of the fine-tuning job.",
            }
        },
        "returns": "The fine-tuning object with the given ID.",
    },
    "cancel_fine_tuning": {
        "url": "https://api.openai.com/v1/fine_tuning/jobs/{fine_tuning_job_id}/cancel",
        "description": "Immediately cancel a fine-tune job.",
        "path_parameters": {
            "fine_tuning_job_id": {
                "type": "string",
                "required": True,
                "description": "The ID of the fine-tuning job to cancel.",
            }
        },
        "returns": "The cancelled fine-tuning object.",
    },
}

api_data = {
    "audio_speech": {
        "url": "https://api.openai.com/v1/audio/speech",
        "description": "Generates audio from the input text.",
        "request_body": {
            "model": {
                "type": "string",
                "required": True,
                "description": "One of the available TTS models: tts-1 or tts-1-hd",
            },
            "input": {
                "type": "string",
                "required": True,
                "description": "The text to generate audio for. The maximum length is 4096 characters.",
            },
            "voice": {
                "type": "string",
                "required": True,
                "description": "The voice to use when generating the audio. Supported voices are alloy, echo, fable, onyx, nova, and shimmer.",
            },
            "response_format": {
                "type": "string",
                "optional": True,
                "default": "mp3",
                "description": "The format to audio in. Supported formats are mp3, opus, aac, flac, wav, and pcm.",
            },
            "speed": {
                "type": "number",
                "optional": True,
                "default": 1,
                "description": "The speed of the generated audio. Select a value from 0.25 to 4.0. 1.0 is the default.",
            },
        },
        "returns": "The audio file content.",
    },
    "audio_transcriptions": {
        "url": "https://api.openai.com/v1/audio/transcriptions",
        "description": "Transcribes audio into the input language.",
        "request_body": {
            "file": {
                "type": "file",
                "required": True,
                "description": "The audio file object (not file name) to transcribe, in one of these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm.",
            },
            "model": {
                "type": "string",
                "required": True,
                "description": "ID of the model to use. Only whisper-1 (which is powered by our open source Whisper V2 model) is currently available.",
            },
            "language": {
                "type": "string",
                "optional": True,
                "description": "The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency.",
            },
            "prompt": {
                "type": "string",
                "optional": True,
                "description": "An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language.",
            },
            "response_format": {
                "type": "string",
                "optional": True,
                "default": "json",
                "description": "The format of the transcript output, in one of these options: json, text, srt, verbose_json, or vtt.",
            },
            "temperature": {
                "type": "number",
                "optional": True,
                "default": 0,
                "description": "The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.",
            },
            "timestamp_granularities": {
                "type": "array",
                "optional": True,
                "default": ["segment"],
                "description": "The timestamp granularities to populate for this transcription. response_format must be set verbose_json to use timestamp granularities. Either or both of these options are supported: word, or segment.",
            },
        },
        "returns": "The transcription object or a verbose transcription object.",
    },
    "audio_translations": {
        "description": "Translates audio into English.",
        "request_body": {
            "file": {
                "type": "file",
                "required": True,
                "description": "The audio file object (not file name) translate, in one of these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm.",
            },
            "model": {
                "type": "string",
                "required": True,
                "description": "ID of the model to use. Only whisper-1 (which is powered by our open source Whisper V2 model) is currently available.",
            },
            "prompt": {
                "type": "string",
                "required": True,
                "description": "An optional text to guide the model's style or continue a previous audio segment. The prompt should be in English.",
            },
            "response_format": {
                "type": "string",
                "optional": True,
                "default": "json",
                "description": "The format of the transcript output, in one of these options: json, text, srt, verbose_json, or vtt.",
            },
            "temperature": {
                "type": "number",
                "optional": True,
                "default": 0,
                "description": "The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.",
            },
        },
        "returns": "The translated text.",
    },
}
