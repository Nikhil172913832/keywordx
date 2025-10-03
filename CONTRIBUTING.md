# Contributing to KeywordX

Thank you for considering contributing to **KeywordX**! We welcome contributions from everyone, especially during **Hacktoberfest**. This document outlines the guidelines for contributing to this project.

---

## How to Contribute

### 1. Fork the Repository
1. Click the **Fork** button at the top-right corner of this repository.
2. Clone your forked repository to your local machine:
    ```shell
    git clone https://github.com/keikurono7/keywordx.git
    cd keywordx
    ```

### 2. Set Up the Development Environment
1. Create a virtual environment:
    ```bash
    python -m venv .env
    source .env/bin/activate  
    # On Windows: .env\Scripts\activate
    ```
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install the project in editable mode:
    ```bash
    pip install -e .
    ```

4. Ensure the required spaCy model is installed:
    ```bash
    python -m spacy download en_core_web_md
    ```

### 3. Pick an Issue
1. Check the [Issues](https://github.com/keikurono7/keywordx/issues) tab for open issues.

2. Look for issues labeled <mark>good first issue</mark> or <mark>hacktoberfest</mark>.

3. Comment on the issue to let maintainers know you’re working on it.

### 4. Make Your Changes
1. Create a new branch for your changes:
    ```bash
    git checkout -b feature/your-feature-name
    ```
2. Make your changes in the codebase.

3. Test your changes locally:
    ```bash
    pytest
    ```
### 5. Commit and Push
1. Commit your changes with a meaningful message:
    ```bash
    git add .
    git commit -m "Add meaningful commit message"
    ```
2. Push your branch to your forked repository:
    ```bash
    git push origin feature/your-feature-name
    ```

### 6. Create a Pull Request
1. Go to your forked repository on GitHub.
2. Click the <b>Compare & pull request</b> button.
3. Provide a clear description of your changes and link to the issue you’re addressing.
4. Submit the pull request.
## Contribution Guidelines
Code Style
- Follow PEP 8 for Python code.
- Use meaningful variable and function names.
- Add comments where necessary to explain complex logic.

Testing
- Ensure all existing tests pass before submitting your changes.
- Add new tests for any new functionality you introduce.
- Run tests using:
    ```bash
    pytest
    ```

Documentation
- Update the [README.md](https://github.com/keikurono7/keywordx/blob/main/README.md) or relevant documentation files if your changes affect usage.
- Add docstrings to any new functions or classes.

## Hacktoberfest Guidelines
1. Ensure your pull request adheres to the [Hacktoberfest rules](https://hacktoberfest.com/participation/).
2. Only meaningful contributions will be accepted. Avoid spammy or low-quality pull requests.
3. Contributions that fix bugs, add features, improve documentation, or enhance tests are welcome.

## Need Help?
If you have any questions or need help, feel free to:

- Open a [new issue](https://github.com/keikurono7/keywordx/issues/new).
- Reach out to the maintainers:
    - Madhusudan: dmpathani@gmail.com
---
Thank you for contributing to KeywordX!

