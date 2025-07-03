@echo off
REM Launcher batch file for Markdown to PDF Converter

cd /src "%~dp0"
python run_markdown_converter.py
