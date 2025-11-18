"""tests for the affiliate link tool."""

import sys
from pathlib import Path
import tempfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from affiliate.accommodation_extractor import AccommodationExtractor
from affiliate.link import LinkProcessor
from affiliate.config import Config


def test_property_extraction():
    """Test that the property extractor finds properties in blog content."""
    extractor = AccommodationExtractor()
    
    test_content = """
    I stayed at the Central Hotel in Donegal, Ireland.
    Harvey's Point Hotel was also recommended.
    We visited Slieve League B&B during the trip.
    """
    
    properties = extractor.extract_accommodations(test_content)
    assert len(properties) >= 1
    assert any(p['name'] == 'Central Hotel' for p in properties)
    assert any(p['name'] == "Harvey's Point Hotel" for p in properties)
    assert any(p['name'] == 'Slieve League B&B' for p in properties)
    print("1. Property extraction test passed")


def test_link_generation():
    """Test that affiliate links are generated correctly."""
    processor = LinkProcessor("12345")
    
    url = processor.generate_affiliate_url("Central Hotel")
    assert "https://booking.com/searchresults.html" in url
    assert "Central%20Hotel" in url
    assert "aid=12345" in url
    print("2. Link generation test passed")


def test_markdown_processing():
    """Test that markdown is processed correctly with hyperlinks."""
    processor = LinkProcessor("12345")
    
    blog_content = """# My Trip
    I stayed at the Central Hotel in Donegal.
    Later I visited the Central Hotel again.
    """
    
    properties = [{"name": "Central Hotel", "location": "Donegal, Ireland"}]
    
    result = processor.process_markdown(blog_content, properties)
    
    # Check that first mention is hyperlinked
    assert "[Central Hotel]" in result
    assert "booking.com" in result
    
    # Count occurrences - should have one hyperlink
    link_count = result.count("[Central Hotel]")
    assert link_count == 1, f"Expected 1 hyperlink, found {link_count}"
    
    print("3. Markdown processing test passed")


def test_configuration_loading():
    """Test that configuration loads correctly."""
    config = Config()
    
    affiliate_id = config.get("affiliate.id")
    assert affiliate_id is not None
    print(f"4. Configuration loading test passed (affiliate_id: {affiliate_id})")


def test_end_to_end():
    """Test the full end-to-end workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create a test blog file
        test_blog = tmpdir / "test_blog.md"
        test_blog.write_text("""# My Blog
I visited the Central Hotel in Donegal.
""")
        
        # Process it
        from affiliate.cli import main
        
        # Temporarily replace sys.argv
        old_argv = sys.argv
        try:
            sys.argv = ["cli.py", str(test_blog), "--affiliate-id", "54321"]
            main()
            
            # Check output file was created
            output_file = tmpdir / "test_blog_linked.md"
            assert output_file.exists(), f"Output file not created: {output_file}"
            
            content = output_file.read_text()
            assert "aid=54321" in content
            assert "[Central Hotel]" in content
            print("5. End-to-end test passed")
            
        finally:
            sys.argv = old_argv


if __name__ == "__main__":
    test_property_extraction()
    test_link_generation()
    test_markdown_processing()
    test_configuration_loading()
    test_end_to_end()
    print("\n All tests passed!")
