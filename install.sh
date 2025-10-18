#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

REPO_DIR=$(dirname "$0")

echo "Starting backuPy installation..."
#echo "This script will install system dependencies and set up a Python virtual environment."

# --- Helper functions ---

# Function to detect the operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/redhat-release ]; then
            echo "redhat"
        elif [ -f /etc/lsb-release ]; then
            echo "debian"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# --- Install system dependencies ---
install_system_deps() {
    OS=$(detect_os)
    echo "Detected OS: $OS"

    case "$OS" in
        "debian")
            echo "Installing system dependencies for Debian/Ubuntu..."
            sudo apt-get update
            sudo apt-get install -y expect xcowsay pigz
            ;;
        "redhat")
            echo "Installing system dependencies for RedHat/Fedora/CentOS..."
            sudo yum install -y expect xcowsay pigz
            ;;
        "macos")
            echo "Installing system dependencies for macOS via Homebrew..."
            if ! command -v brew &> /dev/null; then
                echo "Homebrew not found. Please install Homebrew to continue (https://brew.sh/)."
                exit 1
            fi
            brew install expect pigz xquartz autoconf gettext gdk-pixbuf gtk+ xcowsay 
	    	#git clone https://github.com/nickg/xcowsay.git
		#cd xcowsay
		#./configure
		#make
		#sudo make install
            ;;
        "unknown")
            echo "Warning: Could not determine OS. Please install 'expect' and 'xcowsay' manually."
            ;;
    esac
}

## --- Python setup ---
#setup_python_env() {
#    echo "Setting up Python virtual environment..."
#    if ! command -v python3 &> /dev/null; then
#        echo "Python 3 not found. Please install it to continue."
#        exit 1
#    fi
#
#    # Create and activate a virtual environment in the repository root
#    python3 -m venv "$REPO_DIR/.venv"
#    echo "Virtual environment created at $REPO_DIR/.venv"
#    source "$REPO_DIR/.venv/bin/activate"
#
#    echo "Installing Python dependencies from requirements.txt..."
#    if [ -f "$REPO_DIR/requirements.txt" ]; then
#        pip install -r "$REPO_DIR/requirements.txt"
#    else
#        echo "No requirements.txt file found. Skipping pip installation."
#    fi
#
#    echo "Python environment setup complete."
#}
#
## --- Make scripts executable ---
#make_scripts_executable() {
#    echo "Making shell scripts executable..."
#    chmod +x "$REPO_DIR/backup.sh"
#    chmod +x "$REPO_DIR/expect.exp"
#    # Make the python script executable (useful if using a shebang)
#    chmod +x "$REPO_DIR/backClass.py"
#    echo "Script permissions updated."
#}
#
## --- Finalizing installation ---
#final_steps() {
#    echo ""
#    echo "Installation complete!"
#    echo ""
#    echo "To run your backuPy program, you will need to use the virtual environment."
#    echo "You can activate it with:"
#    echo "source $REPO_DIR/.venv/bin/activate"
#    echo ""
#    echo "Then, you can run the program:"
#    echo "python $REPO_DIR/backClass.py"
#    echo ""
#    echo "The wrapper script 'backup.sh' is also executable:"
#    echo "$REPO_DIR/backup.sh"
#    echo ""
#    echo "If you want to use the commands without activating the virtual environment every time,"
#    echo "consider adding the scripts to your PATH by adding the following line to your shell profile (e.g., ~/.bashrc or ~/.zshrc):"
#    echo "export PATH=\"$REPO_DIR:\$PATH\""
#    echo ""
#    echo "NOTE: Remember to deactivate the virtual environment when you are done by running 'deactivate'."
#}
#
## --- Main installation flow ---
#install_system_deps
#setup_python_env
#make_scripts_executable
#final_steps
