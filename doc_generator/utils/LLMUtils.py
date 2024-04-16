import os

from langchain_openai import ChatOpenAI
from ..types import LLMModelDetails, LLMModels

models = {
    LLMModels.GPT3: LLMModelDetails(
        name=LLMModels.GPT3,
        input_cost_per_1k_tokens=0.0015,
        output_cost_per_1k_tokens=0.002,
        max_length=3050,
        llm=ChatOpenAI(temperature=0.1, openai_api_key=os.getenv('OPENAI_API_KEY'), model_name=LLMModels.GPT3),
        input_tokens=0,
        output_tokens=0,
        succeeded=0,
        failed=0,
        total=0
    ),
    LLMModels.GPT4: LLMModelDetails(
        name=LLMModels.GPT4,
        input_cost_per_1k_tokens=0.03,
        output_cost_per_1k_tokens=0.06,
        max_length=8192,
        llm=ChatOpenAI(temperature=0.1, openai_api_key=os.getenv('OPENAI_API_KEY'), model_name=LLMModels.GPT4),
        input_tokens=0,
        output_tokens=0,
        succeeded=0,
        failed=0,
        total=0
    ),
    LLMModels.GPT432k: LLMModelDetails(
        name=LLMModels.GPT432k,
        input_cost_per_1k_tokens=0.06,
        output_cost_per_1k_tokens=0.12,
        max_length=32768,
        llm=ChatOpenAI(temperature=0.1, openai_api_key=os.getenv('OPENAI_API_KEY'), model_name=LLMModels.GPT4),
        input_tokens=0,
        output_tokens=0,
        succeeded=0,
        failed=0,
        total=0
    )
}

def print_model_details(models):
    output = []
    for model_details in models.values():
        result = {
            'Model': model_details.name,
            'File Count': model_details.total,
            'Succeeded': model_details.succeeded,
            'Failed': model_details.failed,
            'Tokens': model_details.inputTokens + model_details.output_tokens,
            'Cost': ((model_details.inputTokens / 1000) * model_details.input_cost_per_1k_tokens +
                     (model_details.output_tokens / 1000) * model_details.output_cost_per_1k_tokens)
        }
        output.append(result)

    totals = {
        'Model': 'Total',
        'File Count': sum(item['File Count'] for item in output),
        'Succeeded': sum(item['Succeeded'] for item in output),
        'Failed': sum(item['Failed'] for item in output),
        'Tokens': sum(item['Tokens'] for item in output),
        'Cost': sum(item['Cost'] for item in output)
    }

    all_results = output + [totals]
    for item in all_results:
        print(item)

def total_index_cost_estimate(models):
    total_cost = sum(
        (model.input_tokens / 1000) * model.input_cost_per_1k_tokens +
        (model.output_tokens / 1000) * model.output_cost_per_1k_tokens
        for model in models.values()
    )
    return total_cost