# Contributing to ForceWeaver MCP Client

Thank you for your interest in contributing to the ForceWeaver MCP Client! This document provides guidelines for contributing to this project.

## 🤝 **Ways to Contribute**

- **Bug Reports** - Help us identify and fix issues
- **Feature Requests** - Suggest new features or improvements
- **Documentation** - Improve documentation and examples
- **Code Contributions** - Submit bug fixes and new features
- **Testing** - Help test new features and report issues

## 🐛 **Reporting Bugs**

Before creating a bug report, please:

1. **Check existing issues** to avoid duplicates
2. **Use the latest version** of the client
3. **Test with minimal configuration** to isolate the issue

### Bug Report Template

```markdown
**Describe the Bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Configure MCP client with...
2. Run command...
3. See error...

**Expected Behavior**
What you expected to happen.

**Environment**
- OS: [e.g., macOS 14.0]
- Python Version: [e.g., 3.11.0]
- ForceWeaver Client Version: [e.g., 1.1.0]
- MCP Client: [e.g., VS Code, Claude Desktop]

**Additional Context**
Any other context about the problem.
```

## 💡 **Feature Requests**

We welcome feature requests! Please:

1. **Check existing issues** for similar requests
2. **Describe the use case** clearly
3. **Explain the expected behavior**
4. **Consider implementation complexity**

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Describe the specific use case this feature would address.

**Proposed Solution**
If you have ideas for implementation, describe them here.

**Alternatives Considered**
Any alternative solutions you've considered.

**Additional Context**
Any other context about the feature request.
```

## 🔧 **Development Setup**

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/forceweaver-mcp-client.git
   cd forceweaver-mcp-client
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

4. **Install development dependencies**
   ```bash
   pip install pytest pytest-asyncio black flake8 mypy
   ```

5. **Run tests**
   ```bash
   pytest tests/
   ```

## 📝 **Code Style**

We follow Python best practices:

### Formatting
- **Black** for code formatting
- **Line length**: 88 characters (Black default)
- **Import sorting**: Use isort

### Linting
- **Flake8** for linting
- **Type hints** are encouraged
- **Docstrings** for all public functions

### Running Code Quality Tools

```bash
# Format code
black src/

# Check linting
flake8 src/

# Type checking
mypy src/

# Run all checks
make lint  # If Makefile is available
```

## 🧪 **Testing**

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Writing Tests

- **Unit tests** for individual functions
- **Integration tests** for API interactions
- **Mock external dependencies** when appropriate
- **Test both success and error cases**

### Test Structure

```python
import pytest
from src import ForceWeaverMCPClient
from src.exceptions import AuthenticationError

class TestForceWeaverMCPClient:
    @pytest.fixture
    def client(self):
        return ForceWeaverMCPClient()
    
    async def test_authentication_error(self, client):
        with pytest.raises(AuthenticationError):
            await client.call_mcp_api("health/check", forceweaver_api_key="invalid")
```

## 🔀 **Pull Request Process**

### Before Submitting

1. **Create feature branch** from main
2. **Write/update tests** for your changes
3. **Update documentation** if needed
4. **Run all tests** and ensure they pass
5. **Follow code style** guidelines
6. **Write clear commit messages**

### Pull Request Template

```markdown
**Description**
Brief description of the changes.

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**Testing**
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

**Checklist**
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or breaking changes documented)
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in different environments
4. **Approval** required before merge

## 🏷️ **Release Process**

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

### Release Steps

1. **Update version** in `setup.py` and `__init__.py`
2. **Update CHANGELOG.md** with new version
3. **Create release tag** and GitHub release
4. **Publish to PyPI** (maintainers only)

## 🤔 **Questions?**

If you have questions about contributing:

- **Check existing issues** and discussions
- **Read the documentation** thoroughly
- **Ask in discussions** for general questions
- **Create an issue** for specific problems

## 📄 **Code of Conduct**

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) for more information.

## 🎉 **Recognition**

Contributors will be:

- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes**
- **Recognized in project documentation**

Thank you for contributing to ForceWeaver MCP Client! 🚀