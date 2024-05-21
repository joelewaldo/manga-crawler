## 📖 Manga Crawler Project

This is a manga scraper that scrapes various pages for manga content.

# 👨‍💻 Installation

To install the dependencies for this project run the following two commands
after ensuring pip is installed for the version of python you are using.
Admin privileges might be required to execute the commands. Also make sure
that the terminal is at the root folder of this project.

```bash
python -m pip install -r packages/requirements.txt
```

# 🛠 Running

To execute the crawler run the launch.py command.

```bash
python launch.py
```

You can restart the crawler from the seed url
(all current progress will be deleted) using the command

```bash
python launch.py --restart
```

You can specify a different config file to use by using the command with the option

```bash
python launch.py --config_file path/to/config
```
