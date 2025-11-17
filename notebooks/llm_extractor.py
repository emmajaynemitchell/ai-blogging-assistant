"""llm_extractor.py

Extract mentions of accommodation and locations from text using a Hugging Face
transformers model wrapped by LangChain. The model used defaults to
`google/gemma-3-4b-it` but can be changed with `--model`.

Usage examples:
  python llm_extractor.py --text "We stayed at Hotel Aurora, Rome, Italy." 
  python llm_extractor.py --file path/to/article.txt

The script prints a JSON array of objects with fields: name, place, country.
"""
import argparse
import json
import re
import sys
from typing import Any

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline


DEFAULT_MODEL = "google/gemma-3-4b-it"


def build_pipeline(model_name: str = DEFAULT_MODEL, device: int = -1, max_new_tokens: int = 256, temperature: float = 0.2) -> Any:
    """Load tokenizer and model and return a LangChain `HuggingFacePipeline` LLM.

    device: -1 for CPU, or torch device id (0,1,...) for GPU if available.
    """
    print(f"Loading model {model_name} (this may take a while)...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    text_gen = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        device=device,
    )

    hf_llm = HuggingFacePipeline(pipeline=text_gen)
    return hf_llm


PROMPT_TEMPLATE = (
    "Extract mentions of accommodation (hotels, hostels, B&Bs, apartments, villas, campsites, etc.)\n"
    "from the following text. For each accommodation found, produce a JSON object with fields:\n"
    "- \"name\": name of the accommodation (string)\n"
    "- \"place\": city, town, or locality (string or empty)\n"
    "- \"country\": country (string or empty)\n\n"
    "Return a JSON array of objects. Respond ONLY with valid JSON (no extra commentary).\n\n"
    "Text:\n"
    "{text}"
)


def extract_accommodations(llm: Any, text: str, prompt_template: str = PROMPT_TEMPLATE) -> str:
    template = PromptTemplate(input_variables=["text"], template=prompt_template)
    chain = LLMChain(llm=llm, prompt=template)
    output = chain.run({"text": text})
    return output


def extract_json_from_text(text: str):
    """Attempt to extract JSON (array or object) from model output and parse it.

    Tries several heuristics to locate the JSON payload.
    """
    # Try to find a JSON array first
    m = re.search(r"(\[\s*\{.*?\}\s*\])", text, re.S)
    if m:
        candidate = m.group(1)
        return json.loads(candidate)

    # Fall back to the first JSON object
    m = re.search(r"(\{.*\})", text, re.S)
    if m:
        candidate = m.group(1)
        parsed = json.loads(candidate)
        # If single object, wrap in list for consistent output
        return parsed if isinstance(parsed, list) else [parsed]

    # As a last resort, attempt to locate the first '[' and last ']' and parse
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        return json.loads(candidate)

    raise ValueError("No JSON found in model output")


def load_text_from_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Extract accommodations and locations from text using an LLM.")
    parser.add_argument("--file", "-f", help="Path to a text file to process.")
    parser.add_argument("--text", "-t", help="Text to process directly.")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="Hugging Face model name")
    parser.add_argument("--max-tokens", type=int, default=256, help="Max new tokens for generation")
    parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature")
    parser.add_argument("--device", type=int, default=-1, help="Device: -1 for CPU, 0 for first GPU, etc.")
    args = parser.parse_args()

    if not args.file and not args.text:
        print("Provide either --file or --text.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    text = load_text_from_file(args.file) if args.file else args.text

    llm = build_pipeline(model_name=args.model, device=args.device, max_new_tokens=args.max_tokens, temperature=args.temperature)

    raw = extract_accommodations(llm, text)
    try:
        data = extract_json_from_text(raw)
    except Exception:
        print("Failed to parse JSON from model output. Raw output below:", file=sys.stderr)
        print(raw, file=sys.stderr)
        raise

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
