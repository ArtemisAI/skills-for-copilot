# PDF Processing

## Overview

Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. Use when working with PDF files programmatically - reading content, generating documents, filling forms, or analyzing structure.

## When to Use

- Extracting text or tables from PDF documents
- Creating new PDF files from scratch
- Merging, splitting, or rotating PDF pages
- Filling out PDF forms programmatically
- Converting documents to/from PDF format
- Analyzing PDF structure and metadata
- Batch processing PDF documents

## Workflows

### Workflow Decision Tree

**For Simple Text Extraction:**
→ Use `pdfplumber` for clean text and table extraction

**For PDF Creation:**
→ Use `reportlab` for generating new PDFs with full control
→ Use `weasyprint` for HTML-to-PDF conversion

**For Form Filling:**
→ Read `document-skills/pdf/forms.md` for comprehensive form handling guide
→ Use `pypdf` for filling interactive forms

**For Merging/Splitting/Rotating:**
→ Use `pypdf` for basic operations
→ Use scripts in `document-skills/pdf/scripts/` if available

**For Advanced Features:**
→ Check `document-skills/pdf/reference.md` for JavaScript libraries and advanced patterns

### Workflow 1: Extract Text from PDF

```python
import pdfplumber

# Extract all text
with pdfplumber.open("document.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text()
    
print(full_text)

# Extract tables
with pdfplumber.open("data.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            # table is a list of lists
            for row in table:
                print(row)
```

**Tips:**
- `pdfplumber` provides cleaner extraction than `pypdf`
- Use `extract_tables()` for structured data
- Handle None values when text extraction fails

### Workflow 2: Create PDF from Scratch

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create simple PDF
c = canvas.Canvas("output.pdf", pagesize=letter)
c.drawString(100, 750, "Hello World")
c.drawString(100, 730, "This is a PDF created with reportlab")
c.save()

# Or convert HTML to PDF
from weasyprint import HTML

HTML("input.html").write_pdf("output.pdf")

# With CSS styling
HTML("input.html").write_pdf(
    "output.pdf",
    stylesheets=["styles.css"]
)
```

**Tips:**
- `reportlab` for programmatic control
- `weasyprint` for HTML/CSS-based layouts
- Consider templates for consistent formatting

### Workflow 3: Merge Multiple PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()

# Add pages from multiple PDFs
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

# Write merged PDF
with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Workflow 4: Split PDF into Separate Pages

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")

for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### Workflow 5: Rotate PDF Pages

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

# Rotate first page 90 degrees clockwise
page = reader.pages[0]
page.rotate(90)
writer.add_page(page)

# Add remaining pages without rotation
for page in reader.pages[1:]:
    writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

**Rotation angles:**
- `90` - Clockwise 90°
- `180` - 180°
- `270` - Counter-clockwise 90° (or clockwise 270°)

### Workflow 6: Fill PDF Forms

**Important:** For comprehensive form filling, read `document-skills/pdf/forms.md`

```python
from pypdf import PdfReader, PdfWriter

# Read PDF with form fields
reader = PdfReader("form.pdf")
writer = PdfWriter()

# Add pages to writer
writer.append_pages_from_reader(reader)

# Fill form fields
writer.update_page_form_field_values(
    writer.pages[0],
    {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "555-1234"
    }
)

# Write filled form
with open("filled_form.pdf", "wb") as output:
    writer.write(output)
```

### Workflow 7: Extract Metadata

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
meta = reader.metadata

print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
print(f"Producer: {meta.producer}")
print(f"Created: {meta.creation_date}")
print(f"Modified: {meta.modification_date}")
```

## Examples

### Example 1: Batch Convert HTML Reports to PDF

```python
from weasyprint import HTML
import os

html_dir = "reports/"
pdf_dir = "pdfs/"

for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        html_path = os.path.join(html_dir, filename)
        pdf_path = os.path.join(pdf_dir, filename.replace(".html", ".pdf"))
        
        HTML(html_path).write_pdf(pdf_path)
        print(f"Converted: {filename}")
```

### Example 2: Extract Tables and Save as CSV

```python
import pdfplumber
import csv

with pdfplumber.open("data.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        
        for j, table in enumerate(tables):
            filename = f"page_{i+1}_table_{j+1}.csv"
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(table)
```

### Example 3: Create PDF Report with Multiple Sections

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Title
title = Paragraph("Monthly Report", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

# Content sections
sections = [
    ("Executive Summary", "Lorem ipsum..."),
    ("Key Metrics", "Sales increased by..."),
    ("Conclusion", "In summary...")
]

for heading, content in sections:
    story.append(Paragraph(heading, styles['Heading1']))
    story.append(Paragraph(content, styles['BodyText']))
    story.append(Spacer(1, 12))

doc.build(story)
```

## Resources

### Workspace References

**Core Documentation:**
- `document-skills/pdf/SKILL.md` - Complete PDF skill documentation
- `document-skills/pdf/reference.md` - Advanced features and JavaScript libraries
- `document-skills/pdf/forms.md` - Comprehensive PDF form handling guide

**Scripts:**
- `document-skills/pdf/scripts/` - Utility scripts for common operations (if available)

### Python Libraries

**Primary Libraries:**
- `pypdf` - Basic PDF operations (merge, split, rotate, forms)
- `pdfplumber` - Text and table extraction
- `reportlab` - PDF generation from scratch
- `weasyprint` - HTML/CSS to PDF conversion

**Installation:**
```bash
pip install pypdf pdfplumber reportlab weasyprint
```

### Common Issues

**Text extraction returns garbled text:**
- Some PDFs use custom fonts or encoding
- Try `pdfplumber` instead of `pypdf`
- Consider OCR for scanned documents

**Form fields not filling:**
- Verify field names first (see forms.md)
- Some PDFs have flattened forms (not fillable)
- Check PDF version compatibility

**Large PDFs cause memory issues:**
- Process page by page rather than loading entire document
- Use streaming when possible
- Consider splitting into smaller files

## Guidelines

### Best Practices

1. **Choose Right Tool:**
   - Text extraction → `pdfplumber`
   - Form filling → `pypdf`
   - PDF creation → `reportlab` or `weasyprint`
   - Basic operations → `pypdf`

2. **Error Handling:**
   ```python
   try:
       reader = PdfReader("file.pdf")
   except Exception as e:
       print(f"Failed to read PDF: {e}")
   ```

3. **Resource Management:**
   ```python
   # Use context managers
   with pdfplumber.open("file.pdf") as pdf:
       # Process PDF
       pass  # Automatically closed
   ```

4. **Validation:**
   - Verify page counts after operations
   - Check output file exists and is valid
   - Test with various PDF versions

### Performance Tips

1. **Process page by page for large PDFs**
2. **Use appropriate library for task** (don't use reportlab for extraction)
3. **Cache expensive operations** when processing multiple times
4. **Consider parallel processing** for batch operations

### Security Considerations

1. **Validate PDF sources** - PDFs can contain malicious content
2. **Sanitize extracted text** before using in outputs
3. **Be careful with password-protected PDFs**
4. **Don't expose sensitive data** in error messages

## Common Patterns

### Pattern 1: PDF Processing Pipeline

```python
def process_pdf_pipeline(input_path, output_path):
    """Complete PDF processing pipeline"""
    # 1. Read
    reader = PdfReader(input_path)
    
    # 2. Process
    writer = PdfWriter()
    for page in reader.pages:
        # Perform operations
        writer.add_page(page)
    
    # 3. Write
    with open(output_path, "wb") as output:
        writer.write(output)
```

### Pattern 2: Safe Form Filling

```python
def fill_form_safely(template_path, output_path, field_values):
    """Fill PDF form with error handling"""
    try:
        reader = PdfReader(template_path)
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        
        # Verify fields exist
        if writer.pages:
            writer.update_page_form_field_values(
                writer.pages[0], 
                field_values
            )
        
        with open(output_path, "wb") as output:
            writer.write(output)
            
        return True
    except Exception as e:
        print(f"Error filling form: {e}")
        return False
```

### Pattern 3: Batch Processing

```python
import os
from pathlib import Path

def batch_process_pdfs(input_dir, output_dir, process_func):
    """Process all PDFs in a directory"""
    Path(output_dir).mkdir(exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                process_func(input_path, output_path)
                print(f"✓ Processed: {filename}")
            except Exception as e:
                print(f"✗ Failed {filename}: {e}")
```

## Troubleshooting

### Problem: pypdf can't read PDF
**Solution:** Try with `pdfplumber` or check PDF corruption

### Problem: Text extraction is incomplete
**Solution:** PDF may be image-based - needs OCR (pytesseract)

### Problem: Created PDF has wrong formatting
**Solution:** Use `weasyprint` with CSS for precise control

### Problem: Form fill doesn't work
**Solution:** Read complete guide in `document-skills/pdf/forms.md`

## Next Steps

After mastering basic PDF operations:

1. **Explore Advanced Features** - Check `reference.md` for JavaScript libraries
2. **Master Form Handling** - Read `forms.md` for comprehensive guide
3. **Optimize Performance** - Implement batch processing patterns
4. **Add Error Recovery** - Handle edge cases gracefully
5. **Consider Automation** - Build workflows for common tasks

## Additional Context

This instruction set focuses on common PDF operations. For complete details:
- Full skill: `document-skills/pdf/SKILL.md`
- Advanced features: `document-skills/pdf/reference.md`
- Form handling: `document-skills/pdf/forms.md`

Use @workspace to query these resources for specific operations or edge cases.
