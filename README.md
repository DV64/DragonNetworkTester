# 🐉 DragonNetworkTester

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-red)

**DragonNetworkTester** is an advanced network testing suite designed for educational purposes and authorized testing environments. It provides comprehensive network analysis capabilities with real-time monitoring and detailed reporting.

## ⚠️ Important Disclaimer

This tool is for **EDUCATIONAL PURPOSES ONLY**. It should never be used for:
- Unauthorized testing of networks or systems
- Malicious attacks on any infrastructure
- Any illegal activities

Misuse of this tool may result in serious legal consequences.

## 🌟 Features

- Advanced UDP packet generation and transmission
- Real-time system resource monitoring
- Comprehensive statistics and reporting
- Multi-threaded architecture with optimized performance
- Adaptive rate limiting based on system load
- Detailed logging and error handling
- Cross-platform compatibility
- Beautiful CLI interface with progress visualization

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- 64-bit operating system
- Minimum 4GB RAM recommended
- Network adapter supporting UDP

### Python Dependencies
```bash
pip install rich colorama psutil requests typing-extensions
```

## 🚀 Installation

### Linux/Unix
```bash
# Clone the repository
git clone https://github.com/username/DragonNetworkTester

# Navigate to directory
cd DragonNetworkTester

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x dragon_tester.py
```

### Windows
```bash
# Clone repository
git clone https://github.com/username/DragonNetworkTester

# Navigate to directory
cd DragonNetworkTester

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Basic Usage
```bash
python dragon_tester.py --ip TARGET_IP --port PORT --duration SECONDS
```

### Advanced Usage
```bash
python dragon_tester.py --ip TARGET_IP \
                       --port PORT \
                       --duration SECONDS \
                       --threads 20 \
                       --packet-size 1024 \
                       --verbose
```

### Command Line Arguments
- `--ip`: Target IP address (required)
- `--port`: Target port (default: 80)
- `--duration`: Test duration in seconds (required)
- `--threads`: Number of threads (default: 10)
- `--packet-size`: Packet size in bytes (default: 1024)
- `--verbose`: Enable verbose output

## 📊 Output Example

```
╔══════════════════════════════════════════════╗
║           DragonNetworkTester v1.0           ║
╚══════════════════════════════════════════════╝

Target: 192.168.1.1:80
Threads: 10
Duration: 60s

[====================] 100% Complete

Statistics:
• Packets Sent: 1,234,567
• Bytes Sent: 1.23 GB
• Success Rate: 99.98%
• Avg Response: 0.23ms
```

## 🛡️ Best Practices

1. Always obtain proper authorization before testing
2. Start with lower thread counts and increase gradually
3. Monitor system resources during testing
4. Use verbose mode for detailed debugging
5. Keep logs for analysis

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🔄 Updates

Check the [CHANGELOG](CHANGELOG.md) for recent updates and changes.
