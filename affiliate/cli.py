"""Command-line interface for the affiliate link tool."""

import argparse
import sys
from pathlib import Path

from .config import Config
from .accommodation_extractor import AccommodationExtractor
from .link import LinkProcessor


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Blogging Assistant - Affiliate Link Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.cli examples/donegal_blog.md
  python -m src.cli examples/donegal_blog.md --config config/default_config.yaml
  python -m src.cli examples/donegal_blog.md --affiliate-id 54321
        """
    )
    
    parser.add_argument(
        "blog_post",
        help="Path to the markdown blog post file"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration YAML file",
        default=None
    )
    
    parser.add_argument(
        "--affiliate-id",
        help="Booking.com affiliate ID (overrides config)",
        default=None
    )
    
    parser.add_argument(
        "--output-dir",
        help="Output directory for processed file (default: same as input)",
        default=None
    )
    
    parser.add_argument(
        "--llm-model",
        help="LLM model to use (default: mock)",
        default=None
    )
    
    args = parser.parse_args()
    
    # Validate input file
    blog_path = Path(args.blog_post)
    if not blog_path.exists():
        print(f"Error: Blog post file not found: {args.blog_post}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Load configuration
        config = Config(args.config)
        
        # Override with command-line arguments
        if args.affiliate_id:
            config.config["affiliate"]["id"] = args.affiliate_id
        if args.llm_model:
            config.config["llm"]["model"] = args.llm_model
        
        # Read blog post
        with open(blog_path, 'r', encoding='utf-8') as f:
            blog_content = f.read()
        
        print(f"Reading in: {blog_path}")
        
        # Extract properties using LLM
        extractor = AccommodationExtractor()
        properties = extractor.extract_accommodations(blog_content)
        
        if not properties:
            print("No accommodation properties found in the blog post.")
            sys.exit(0)
        
        print(f"Found {len(properties)} properties mentioned in the blog post.")

        for prop in properties:
            print(f"  - {prop['name']} ({prop['location']})")
        
        # Process markdown and add links
        processor = LinkProcessor(config.get("affiliate.id", "12345"))
        print("Got affiliate id")
        processed_content = processor.process_markdown(blog_content, properties)
        print("Processed markdown content with affiliate links. ")
        
        # Determine output file path
        output_dir = Path(args.output_dir) if args.output_dir else blog_path.parent
        suffix = config.get("output.suffix", "_linked")
        output_filename = f"{blog_path.stem}{suffix}.md"
        output_path = output_dir / output_filename
        
        # Write processed content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        print(f"Successfully processed blog post")
        print(f"Output saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
