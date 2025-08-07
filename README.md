# Momentum - Memo Application

A clean memo application built with Flask to help you easily record and manage daily thoughts and tasks.

## Features

- 📝 Create, edit, and delete memos
- 🎨 Modern responsive interface design
- 📱 Mobile-friendly layout
- 💾 Local JSON file storage
- ⏰ Record creation and update times
- 🔔 Operation success notifications

## Quick Start

### Requirements

- Python 3.13+
- uv package manager

### Installation and Running

1. **Clone the project**
   ```bash
   git clone <repository-url>
   cd momentum
   ```

2. **Create virtual environment**
   ```bash
   uv venv
   ```

3. **Activate virtual environment**
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   uv sync
   ```

5. **Run the application**
   ```bash
   uv run app.py
   ```

6. **Access the application**
   Open your browser and visit `http://localhost:5000`

## Project Structure

```
momentum/
├── app.py              # Flask application main file
├── main.py             # Entry point file
├── memos.json          # Data storage file
├── pyproject.toml      # Project configuration
├── requirements.txt    # Dependencies list
├── uv.lock            # uv lock file
├── static/
│   └── style.css      # Style file
└── templates/
    ├── index.html     # Home page template
    └── edit.html      # Edit page template
```

## Development Guide

### Using uv for package management

```bash
# Add new dependency
uv add package-name

# Remove dependency
uv remove package-name

# Sync dependencies
uv sync

# Run script
uv run script.py
```

### Code Standards

- Follow PEP 8 Python code standards
- Each Python file should not exceed 200 lines
- No more than 8 files per folder level
- Avoid code duplication and circular dependencies
- Keep code clean and readable

## Feature Description

### Memo Management
- **Create Memo**: Enter title and content to create a new memo
- **Edit Memo**: Click edit button to modify existing memo
- **Delete Memo**: Click delete button to remove memo (requires confirmation)

### Data Storage
- Use local JSON file for data storage
- Automatically record creation and update times
- Persistent data saving

### User Interface
- Responsive design supporting desktop and mobile devices
- Modern card-based layout
- Gradient background and shadow effects
- Friendly user interaction feedback

## Interface Preview

The application includes the following main interfaces:
- Home page: Display memo list and form for adding new memos
- Edit page: Modify title and content of existing memos

## Custom Configuration

### Change Secret Key
Modify `app.secret_key` in `app.py`:
```python
app.secret_key = 'your-custom-secret-key'
```

### Change Data File Path
Modify `DATA_FILE` in `app.py`:
```python
DATA_FILE = 'custom/path/to/memos.json'
```

## Contributing Guide

1. Fork this project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- [Your Name] - [Your Email]

## Contact

For questions or suggestions, please contact through:
- Submit an Issue
- Send email to [Your Email]

---

⭐ If this project is helpful to you, please consider giving it a star!