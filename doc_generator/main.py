"""CLI interface for doc_generator project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
from doc_generator.query import query
from doc_generator.index import index
from doc_generator.types import AutodocRepoConfig, AutodocUserConfig, LLMModels
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m doc_generator` and `$ doc_generator `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    # Example config objects, these need to be defined or imported properly
    print("Initializing Auto Documentation...")
    name = prompt("Project Name?[Example: autodoc]\n")
    project_root = prompt("Project Root?[Example: ./autodoc]\n",
                          default=f"./{name}")
    project_url = prompt("Project URL?[Example: https://github.com/context-labs/autodoc]\n")
    output_dir = prompt("Output Directory?[Example: ./output/autodoc]\n",
                        default=f"./output/{name}")

    mode_completer = WordCompleter(["Readme", "Query"])
    mode = prompt("Documentation Mode?[Readme/Query]\n", default="Readme",
                  completer=mode_completer)

    model_completer = WordCompleter([LLMModels.LLAMA2_7B_CHAT_GPTQ.value,
                                     LLMModels.LLAMA2_13B_CHAT_GPTQ.value,
                                     LLMModels.CODELLAMA_7B_GPTQ.value,
                                     LLMModels.CODELLAMA_13B_GPTQ.value])
    model = prompt("Which model?\n",
                   default=LLMModels.LLAMA2_7B_CHAT_GPTQ.value,
                   completer=model_completer)
    print("Initialization Complete.\n")

    repo_config = {
        "name": name,
        "root": project_root,
        "repository_url": project_url,
        "output": output_dir,
        "llms": [model],
        "ignore": [
            ".*",
            "*package-lock.json",
            "*package.json",
            "node_modules",
            "*dist*",
            "*build*",
            "*test*",
            "*.svg",
            "*.md",
            "*.mdx",
            "*.toml"
        ],
        "file_prompt": "Write a detailed technical explanation of what this code does. \n      Focus on the high-level purpose of the code and how it may be used in the larger project.\n      Include code examples where appropriate. Keep you response between 100 and 300 words. \n      DO NOT RETURN MORE THAN 300 WORDS.\n      Output should be in markdown format.\n      Do not just list the methods and classes in this file.",
        "folder_prompt": "Write a technical explanation of what the code in this file does\n      and how it might fit into the larger project or work with other parts of the project.\n      Give examples of how this code might be used. Include code examples where appropriate.\n      Be concise. Include any information that may be relevant to a developer who is curious about this code.\n      Keep you response under 400 words. Output should be in markdown format.\n      Do not just list the files and folders in this folder.",
        "chat_prompt": "",
        "content_type": "docs",
        "target_audience": "smart developer",
        "link_hosted": True,
        "priority": 'performance',
        "max_concurrent_calls": 50,
        "add_questions": False
    }
    user_config = {
        "llms": [model]
    }

    repo_conf = AutodocRepoConfig(
        name=repo_config["name"],
        repository_url=repo_config["repository_url"],
        root=repo_config["root"],
        output=repo_config["output"],
        llms=repo_config["llms"],
        priority=repo_config["priority"],
        max_concurrent_calls=repo_config["max_concurrent_calls"],
        add_questions=repo_config["add_questions"],
        ignore=repo_config["ignore"],
        file_prompt=repo_config["file_prompt"],
        folder_prompt=repo_config["folder_prompt"],
        chat_prompt=repo_config["chat_prompt"],
        content_type=repo_config["content_type"],
        target_audience=repo_config["target_audience"],
        link_hosted=repo_config["link_hosted"],
    )

    usr_conf = AutodocUserConfig(llms=user_config['llms'])

    index.index(repo_conf)
    print("Done Indexing !!")

    if mode.lower() == "query":
        query.query(repo_conf, usr_conf)
    else:
        query.generate_readme(repo_conf, usr_conf)

