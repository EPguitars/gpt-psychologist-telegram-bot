# pylint: disable=line-too-long
"""
This is a module with chatGPT logic for ai-psychologist bot

Coded by Eugene Poluyakhtov
Idea by Ilya Lisov and Eugene Poluyakhtov
"""
import os

import openai
import tiktoken
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPEN_AI_TOKEN")


def get_result(data: list, prompt):
    """This is a function for making a request to GPT API"""
    data.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=data,
    )

    answer = response.choices[0].message.content

    data.append({"role": "assistant", "content": answer})

    return data, answer


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
