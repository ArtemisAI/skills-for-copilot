# Verification Strategies

## Overview

Verification is critical for ensuring agent outputs are correct, safe, and meet requirements. Effective verification enables agents to self-correct errors, iterate toward better solutions, and operate autonomously with confidence.

The feedback loop at the heart of agent design requires robust verification: **gather context → take action → verify work → repeat**. Without verification, agents cannot learn from mistakes or improve their outputs.

## Verification Strategies

### 1. Rules-Based Verification

Use deterministic rules and checks to verify correctness.

#### When to Use

- Code quality (linting, type checking, formatting)
- Data validation (schema compliance, format checking)
- Security auditing (pattern matching for vulnerabilities)
- Compliance checking (policy enforcement)
- Output format validation (JSON structure, required fields)

#### Advantages

- **Deterministic**: Same input always produces same result
- **Fast**: No model inference required
- **Transparent**: Rules are explicit and auditable
- **Actionable**: Specific errors with clear fixes

#### Implementation Examples

**Code Linting and Type Checking:**

```python
from claude_agent_sdk import tool
import subprocess

@tool(
    "verify_python_code",
    "Run multiple verification checks on Python code",
    {"file_path": str}
)
async def verify_python_code(args):
    file_path = args["file_path"]
    issues = []

    # Run pylint
    result = subprocess.run(
        ["pylint", file_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        issues.append({
            "checker": "pylint",
            "issues": parse_pylint_output(result.stdout)
        })

    # Run mypy for type checking
    result = subprocess.run(
        ["mypy", file_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        issues.append({
            "checker": "mypy",
            "issues": parse_mypy_output(result.stdout)
        })

    # Run black for formatting
    result = subprocess.run(
        ["black", "--check", file_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        issues.append({
            "checker": "black",
            "message": "File needs formatting. Run: black " + file_path
        })

    if issues:
        return {
            "content": [{
                "type": "text",
                "text": f"Verification failed with {len(issues)} issue types:\n" +
                        json.dumps(issues, indent=2) +
                        "\n\nFix these issues and verify again."
            }]
        }
    else:
        return {
            "content": [{
                "type": "text",
                "text": "✓ All verification checks passed!"
            }]
        }
```

**Schema Validation:**

```python
from pydantic import BaseModel, ValidationError

class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    age: int
    role: Literal["admin", "user", "guest"]

@tool(
    "validate_user_data",
    "Validate user data against schema",
    {"data": dict}
)
async def validate_user_data(args):
    data = args["data"]

    try:
        user = UserSchema(**data)
        return {
            "content": [{
                "type": "text",
                "text": f"✓ Validation passed: {user.model_dump_json(indent=2)}"
            }]
        }
    except ValidationError as e:
        errors = []
        for error in e.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "type": error["type"],
                "message": error["msg"]
            })

        return {
            "content": [{
                "type": "text",
                "text": f"✗ Validation failed with {len(errors)} errors:\n" +
                        json.dumps(errors, indent=2) +
                        "\n\nFix these errors and validate again."
            }]
        }
```

**Security Pattern Detection:**

```python
import re

SECURITY_PATTERNS = {
    "sql_injection": {
        "pattern": r"execute\([\"'].*\+.*[\"']\)|cursor\.execute\(.*%.*\)",
        "severity": "critical",
        "message": "Potential SQL injection: Use parameterized queries"
    },
    "hardcoded_secret": {
        "pattern": r"(api_key|password|secret|token)\s*=\s*[\"'][^\"']+[\"']",
        "severity": "critical",
        "message": "Hardcoded secret: Use environment variables"
    },
    "command_injection": {
        "pattern": r"os\.system\(.*\+.*\)|subprocess\.(call|run)\(.*shell=True.*\)",
        "severity": "high",
        "message": "Potential command injection: Avoid shell=True and user input"
    }
}

@tool(
    "security_scan",
    "Scan code for security vulnerabilities",
    {"file_path": str}
)
async def security_scan(args):
    file_path = args["file_path"]

    with open(file_path, "r") as f:
        content = f.read()

    findings = []

    for vuln_type, config in SECURITY_PATTERNS.items():
        matches = re.finditer(config["pattern"], content, re.MULTILINE)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            findings.append({
                "type": vuln_type,
                "severity": config["severity"],
                "line": line_num,
                "code": match.group(0),
                "message": config["message"]
            })

    if findings:
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        findings.sort(key=lambda x: severity_order[x["severity"]])

        return {
            "content": [{
                "type": "text",
                "text": f"⚠️ Security scan found {len(findings)} issues:\n" +
                        json.dumps(findings, indent=2) +
                        "\n\nAddress these security concerns before proceeding."
            }]
        }
    else:
        return {
            "content": [{
                "type": "text",
                "text": "✓ Security scan passed: No obvious vulnerabilities detected"
            }]
        }
```

**Unit Test Execution:**

```python
@tool(
    "run_tests",
    "Execute test suite and verify all tests pass",
    {
        "test_path": str,
        "test_pattern": str,  # e.g., "test_*.py"
    }
)
async def run_tests(args):
    test_path = args["test_path"]
    test_pattern = args.get("test_pattern", "test_*.py")

    # Run pytest
    result = subprocess.run(
        ["pytest", test_path, "-v", "--tb=short"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        # Extract test summary
        summary = extract_pytest_summary(result.stdout)
        return {
            "content": [{
                "type": "text",
                "text": f"✓ All tests passed!\n{summary}"
            }]
        }
    else:
        # Parse failures
        failures = parse_pytest_failures(result.stdout)
        return {
            "content": [{
                "type": "text",
                "text": f"✗ Tests failed:\n" +
                        json.dumps(failures, indent=2) +
                        "\n\nFix failing tests and run again."
            }]
        }
```

#### Best Practices

1. **Provide multiple layers**: Lint, type check, test, security scan
2. **Give specific feedback**: Include file, line number, and fix suggestion
3. **Prioritize issues**: Critical > High > Medium > Low
4. **Make errors actionable**: "Fix X by doing Y"
5. **Support incremental verification**: Check one file at a time if needed

---

### 2. Visual Verification

Use screenshots and visual rendering to verify UI, layout, and design work.

#### When to Use

- UI component development
- Web page layout verification
- Data visualization checking
- PDF/document rendering
- Graph and chart generation

#### Advantages

- **Intuitive**: Humans and LLMs understand visual representations
- **Comprehensive**: Catches layout, styling, and rendering issues
- **Context-rich**: Shows relationships and hierarchy
- **Realistic**: Tests actual rendered output

#### Implementation Examples

**Screenshot-Based UI Verification:**

```python
from playwright.async_api import async_playwright

@tool(
    "verify_webpage",
    "Take screenshot of webpage and analyze layout",
    {
        "url": str,
        "viewport": dict,  # {"width": 1920, "height": 1080}
        "checks": list[str]  # ["responsive", "accessibility", "styling"]
    }
)
async def verify_webpage(args):
    url = args["url"]
    viewport = args.get("viewport", {"width": 1920, "height": 1080})
    checks = args.get("checks", ["layout"])

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport=viewport)

        await page.goto(url)

        # Take screenshot
        screenshot_path = f"screenshots/{timestamp()}.png"
        await page.screenshot(path=screenshot_path, full_page=True)

        # Get page info
        page_info = {
            "title": await page.title(),
            "url": page.url,
            "viewport": viewport
        }

        # Run accessibility checks if requested
        accessibility_issues = []
        if "accessibility" in checks:
            accessibility_issues = await page.accessibility.snapshot()

        # Get console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text))

        await browser.close()

    return {
        "content": [{
            "type": "text",
            "text": f"Screenshot saved to {screenshot_path}\n\n" +
                    f"Page info: {json.dumps(page_info, indent=2)}\n\n" +
                    f"Console errors: {len(console_errors)}\n\n" +
                    "Review the screenshot and verify:\n" +
                    "- Layout is correct\n" +
                    "- Styling matches design\n" +
                    "- All elements are visible\n" +
                    "- Responsive behavior is appropriate\n\n" +
                    f"Accessibility issues: {len(accessibility_issues)}"
        }]
    }
```

**Interactive Verification Loop:**

```python
# Agent workflow:
# 1. Generate HTML/CSS
# 2. Render and take screenshot
# 3. Analyze screenshot
# 4. If issues found, iterate
# 5. Repeat until satisfactory

async def ui_verification_loop(client: ClaudeSDKClient):
    max_iterations = 5

    for i in range(max_iterations):
        # Agent generates UI
        response = await client.send_message(
            "Generate the user profile page component"
        )

        # Render and screenshot
        screenshot = await render_and_screenshot(response.code)

        # Agent reviews screenshot
        review = await client.send_message(
            f"Review this screenshot of the UI you created: {screenshot}. " +
            "Check: layout, spacing, colors, typography, responsiveness. " +
            "If issues exist, describe them and update the code. " +
            "If perfect, respond with 'APPROVED'."
        )

        if "APPROVED" in review.upper():
            print(f"UI approved after {i+1} iterations")
            break
    else:
        print(f"Max iterations ({max_iterations}) reached")
```

**Data Visualization Verification:**

```python
@tool(
    "verify_chart",
    "Generate and verify data visualization",
    {
        "data": dict,
        "chart_type": str,
        "requirements": list[str]
    }
)
async def verify_chart(args):
    data = args["data"]
    chart_type = args["chart_type"]
    requirements = args["requirements"]

    # Generate chart
    chart_path = generate_chart(data, chart_type)

    # Basic checks
    checks = {
        "file_exists": os.path.exists(chart_path),
        "file_size": os.path.getsize(chart_path) if os.path.exists(chart_path) else 0,
        "meets_requirements": []
    }

    # Verify requirements
    for req in requirements:
        if req == "has_title":
            checks["meets_requirements"].append({
                "requirement": "has_title",
                "status": check_chart_has_title(chart_path)
            })
        elif req == "has_legend":
            checks["meets_requirements"].append({
                "requirement": "has_legend",
                "status": check_chart_has_legend(chart_path)
            })
        # ... more checks

    return {
        "content": [{
            "type": "text",
            "text": f"Chart generated: {chart_path}\n\n" +
                    f"Verification results:\n{json.dumps(checks, indent=2)}\n\n" +
                    "Review the chart visually and verify:\n" +
                    "- Data is accurately represented\n" +
                    "- Labels are clear and readable\n" +
                    "- Colors are appropriate\n" +
                    "- Scale and proportions are correct"
        }]
    }
```

#### Best Practices

1. **Multiple viewports**: Test desktop, tablet, mobile
2. **Capture full page**: Use full_page=True for scrolling content
3. **Check console errors**: Catch JavaScript errors
4. **Accessibility checks**: Verify ARIA labels, contrast ratios
5. **Iterative refinement**: Give agent multiple chances to improve
6. **Specific feedback**: Point out exact issues (spacing, colors, alignment)

---

### 3. LLM-as-Judge Verification

Use a secondary LLM to evaluate agent outputs against fuzzy or subjective criteria.

#### When to Use

- Content quality (writing, tone, clarity)
- Customer support responses (empathy, accuracy, helpfulness)
- Creative outputs (originality, coherence)
- Summarization quality (completeness, conciseness)
- Translation accuracy (meaning preservation, natural fluency)

#### Advantages

- **Handles ambiguity**: Can judge subjective criteria
- **Context-aware**: Understands nuance and intent
- **Flexible**: Can adapt to various quality dimensions
- **Natural language**: Provides human-like feedback

#### Disadvantages

- **Latency**: Requires additional model inference
- **Cost**: Extra API calls
- **Consistency**: May vary across evaluations
- **Potential bias**: Inherits model biases

#### Implementation Examples

**Content Quality Evaluation:**

```python
@tool(
    "evaluate_content_quality",
    "Evaluate written content for quality across multiple dimensions",
    {
        "content": str,
        "content_type": str,  # "blog_post", "email", "documentation"
        "criteria": list[str]  # ["clarity", "accuracy", "tone", "completeness"]
    }
)
async def evaluate_content_quality(args):
    content = args["content"]
    content_type = args["content_type"]
    criteria = args.get("criteria", ["clarity", "accuracy", "completeness"])

    # Create evaluation prompt
    evaluation_prompt = f"""
Evaluate the following {content_type} across these criteria: {', '.join(criteria)}

Content:
```
{content}
```

For each criterion, provide:
1. Score (1-10)
2. Strengths
3. Areas for improvement
4. Specific suggestions

Format response as JSON.
"""

    # Use a separate Claude instance as judge
    from anthropic import Anthropic
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-sonnet-4.5-20250929",
        max_tokens=2048,
        messages=[{"role": "user", "content": evaluation_prompt}]
    )

    evaluation = json.loads(response.content[0].text)

    # Check if passes threshold
    passing_score = 7
    all_passed = all(eval["score"] >= passing_score for eval in evaluation.values())

    if all_passed:
        return {
            "content": [{
                "type": "text",
                "text": f"✓ Content quality evaluation passed!\n\n{json.dumps(evaluation, indent=2)}"
            }]
        }
    else:
        return {
            "content": [{
                "type": "text",
                "text": f"⚠️ Content needs improvement:\n\n{json.dumps(evaluation, indent=2)}\n\n" +
                        "Address the areas for improvement and re-evaluate."
            }]
        }
```

**Customer Support Response Evaluation:**

```python
@tool(
    "evaluate_support_response",
    "Evaluate customer support response quality",
    {
        "customer_message": str,
        "agent_response": str
    }
)
async def evaluate_support_response(args):
    customer_message = args["customer_message"]
    agent_response = args["agent_response"]

    evaluation_prompt = f"""
Evaluate this customer support response:

Customer message:
{customer_message}

Agent response:
{agent_response}

Evaluate across these dimensions:
1. **Empathy** (1-10): Does the response show understanding of customer's situation?
2. **Accuracy** (1-10): Is the information provided correct and relevant?
3. **Completeness** (1-10): Does it fully address all customer concerns?
4. **Tone** (1-10): Is the tone professional, friendly, and appropriate?
5. **Actionability** (1-10): Are next steps clear?

For each dimension:
- Score (1-10)
- Explanation
- Improvement suggestions

Return as JSON with structure:
{{
  "dimension_name": {{
    "score": int,
    "explanation": str,
    "improvements": [str]
  }}
}}
"""

    # Call LLM judge
    evaluation = await call_llm_judge(evaluation_prompt)

    # Calculate overall score
    avg_score = sum(d["score"] for d in evaluation.values()) / len(evaluation)

    if avg_score >= 8.0:
        return {
            "content": [{
                "type": "text",
                "text": f"✓ Response quality excellent (avg: {avg_score:.1f}/10)\n\n" +
                        json.dumps(evaluation, indent=2)
            }]
        }
    elif avg_score >= 6.0:
        return {
            "content": [{
                "type": "text",
                "text": f"⚠️ Response acceptable but could improve (avg: {avg_score:.1f}/10)\n\n" +
                        json.dumps(evaluation, indent=2) +
                        "\n\nConsider implementing suggested improvements."
            }]
        }
    else:
        return {
            "content": [{
                "type": "text",
                "text": f"✗ Response needs significant improvement (avg: {avg_score:.1f}/10)\n\n" +
                        json.dumps(evaluation, indent=2) +
                        "\n\nRewrite the response addressing all concerns."
            }]
        }
```

**Translation Quality Verification:**

```python
@tool(
    "verify_translation",
    "Verify translation quality using back-translation",
    {
        "source_text": str,
        "translated_text": str,
        "source_lang": str,
        "target_lang": str
    }
)
async def verify_translation(args):
    source = args["source_text"]
    translated = args["translated_text"]
    source_lang = args["source_lang"]
    target_lang = args["target_lang"]

    # Back-translate
    back_translation = await translate_text(translated, target_lang, source_lang)

    # Evaluate using LLM judge
    evaluation_prompt = f"""
Compare the original text with the back-translation to assess translation quality:

Original ({source_lang}):
{source}

Back-translation from {target_lang}:
{back_translation}

Translation ({target_lang}):
{translated}

Evaluate:
1. **Meaning preservation** (1-10): Is the core meaning intact?
2. **Fluency** (1-10): Is the translation natural in {target_lang}?
3. **Accuracy** (1-10): Are all details correctly translated?
4. **Cultural appropriateness** (1-10): Is it culturally appropriate?

Provide scores and identify any mistranslations or issues.

Return as JSON.
"""

    evaluation = await call_llm_judge(evaluation_prompt)
    avg_score = sum(d["score"] for d in evaluation.values()) / len(evaluation)

    if avg_score >= 8.0:
        return {
            "content": [{
                "type": "text",
                "text": f"✓ Translation quality excellent (avg: {avg_score:.1f}/10)"
            }]
        }
    else:
        return {
            "content": [{
                "type": "text",
                "text": f"⚠️ Translation needs review (avg: {avg_score:.1f}/10)\n\n" +
                        json.dumps(evaluation, indent=2)
            }]
        }
```

#### Best Practices

1. **Clear evaluation criteria**: Define specific dimensions to evaluate
2. **Structured output**: Request JSON for consistent parsing
3. **Numerical scores**: Enable thresholding and comparison
4. **Specific feedback**: Ask for actionable improvement suggestions
5. **Threshold tuning**: Adjust passing scores based on use case
6. **Cost consideration**: Cache evaluations when possible
7. **Consistency checks**: Run same evaluation multiple times for important decisions

---

## Combining Verification Strategies

### Multi-Layered Verification

Use multiple strategies together for comprehensive verification:

```python
@tool(
    "comprehensive_code_review",
    "Perform comprehensive code review with multiple verification layers",
    {"file_path": str}
)
async def comprehensive_code_review(args):
    file_path = args["file_path"]
    issues = {"critical": [], "warnings": [], "suggestions": []}

    # Layer 1: Rules-based checks
    lint_result = await verify_python_code({"file_path": file_path})
    if "failed" in lint_result["content"][0]["text"]:
        issues["critical"].append("Linting issues found")

    security_result = await security_scan({"file_path": file_path})
    if "issues" in security_result["content"][0]["text"]:
        issues["critical"].append("Security vulnerabilities detected")

    test_result = await run_tests({"test_path": f"tests/test_{file_path}"})
    if "failed" in test_result["content"][0]["text"]:
        issues["critical"].append("Tests failing")

    # Layer 2: LLM-as-judge for code quality
    with open(file_path, "r") as f:
        code = f.read()

    quality_eval = await evaluate_code_quality({
        "code": code,
        "criteria": ["readability", "maintainability", "efficiency"]
    })

    if quality_eval["avg_score"] < 7.0:
        issues["warnings"].append("Code quality below threshold")

    # Layer 3: Architectural review (LLM)
    arch_review = await review_architecture({
        "code": code,
        "context": "Part of authentication module"
    })

    if arch_review["concerns"]:
        issues["suggestions"].extend(arch_review["concerns"])

    # Compile results
    has_critical = len(issues["critical"]) > 0

    result_text = "Code Review Results:\n\n"
    if has_critical:
        result_text += f"✗ CRITICAL ISSUES ({len(issues['critical'])}):\n"
        for issue in issues["critical"]:
            result_text += f"  - {issue}\n"
        result_text += "\nCode MUST NOT be merged until critical issues are resolved.\n\n"

    if issues["warnings"]:
        result_text += f"⚠️ Warnings ({len(issues['warnings'])}):\n"
        for warning in issues["warnings"]:
            result_text += f"  - {warning}\n"
        result_text += "\n"

    if issues["suggestions"]:
        result_text += f"💡 Suggestions ({len(issues['suggestions'])}):\n"
        for suggestion in issues["suggestions"]:
            result_text += f"  - {suggestion}\n"

    if not any(issues.values()):
        result_text = "✓ Code review passed! No issues found."

    return {"content": [{"type": "text", "text": result_text}]}
```

### Progressive Verification

Start with fast checks, progressively add more expensive ones:

```python
async def progressive_verification(content, content_type):
    """
    Progressive verification: fail fast with cheap checks,
    only run expensive checks if cheap ones pass
    """

    # Stage 1: Format validation (instant, free)
    if not validate_format(content):
        return {"status": "failed", "stage": "format", "message": "Invalid format"}

    # Stage 2: Schema validation (fast, free)
    if not validate_schema(content):
        return {"status": "failed", "stage": "schema", "message": "Schema violation"}

    # Stage 3: Rules-based checks (fast, free)
    rules_result = apply_rules(content)
    if not rules_result.passed:
        return {"status": "failed", "stage": "rules", "message": rules_result.message}

    # Stage 4: Unit tests (medium speed, free)
    if content_type == "code":
        test_result = run_unit_tests(content)
        if not test_result.passed:
            return {"status": "failed", "stage": "tests", "message": test_result.message}

    # Stage 5: LLM judge (slow, costs tokens)
    evaluation = await llm_judge_evaluation(content, content_type)
    if evaluation.score < 8.0:
        return {"status": "needs_improvement", "stage": "quality", "evaluation": evaluation}

    return {"status": "passed", "message": "All verification stages passed"}
```

### Verification with Iteration

Build verification into agent feedback loops:

```python
async def iterative_content_generation(client: ClaudeSDKClient, task: str, max_iterations: int = 3):
    """
    Generate content with iterative verification and improvement
    """

    for iteration in range(max_iterations):
        # Generate content
        response = await client.send_message(task)
        content = extract_content(response)

        # Verify
        verification = await comprehensive_verification(content)

        if verification["status"] == "passed":
            print(f"✓ Content approved after {iteration + 1} iterations")
            return content

        # Provide feedback for improvement
        feedback_message = (
            f"The content has issues:\n{verification['message']}\n\n"
            f"Please revise the content to address these concerns."
        )

        task = feedback_message  # Next iteration uses feedback as prompt

    print(f"⚠️ Max iterations ({max_iterations}) reached without passing verification")
    return content  # Return best attempt
```

## Best Practices

1. **Fail Fast**: Run cheap, fast checks first
2. **Specific Feedback**: Provide actionable, detailed error messages
3. **Layered Approach**: Combine multiple verification strategies
4. **Iterative Refinement**: Give agents opportunities to fix issues
5. **Appropriate Thresholds**: Set realistic passing criteria
6. **Log Everything**: Track verification results for analysis
7. **Cost-Aware**: Balance thoroughness with API costs
8. **Timeout Protection**: Prevent infinite verification loops
9. **Human Escalation**: Flag edge cases for human review
10. **Continuous Monitoring**: Track verification success rates over time
