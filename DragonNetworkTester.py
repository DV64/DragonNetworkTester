#!/usr/bin/python3

"""
DragonNetworkTester - Advanced Network Testing Suite
Author: DV64
Version: 1.0
"""

import os
import socket
import time
import random
import sys
import threading
import logging
import argparse
import queue
import statistics
import platform
import psutil
import requests
import colorama
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.layout import Layout
from rich.live import Live

# Initialize colorama for cross-platform color support
colorama.init(autoreset=True)

@dataclass
class SystemResources:
    """System Resource Monitor"""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    network_speed: float = 0.0
    active_connections: int = 0

@dataclass
class NetworkStats:
    """Network Statistics Tracker"""
    packets_sent: int = 0
    bytes_sent: int = 0
    failed_attempts: int = 0
    successful_attempts: int = 0
    start_time: float = 0.0
    response_times: List[float] = None
    packet_sizes: List[int] = None

    def __post_init__(self):
        self.response_times = []
        self.packet_sizes = []
        self.start_time = time.time()

    @property
    def success_rate(self) -> float:
        total = self.packets_sent + self.failed_attempts
        return (self.packets_sent / total * 100) if total > 0 else 0.0

    @property
    def average_response(self) -> float:
        """Calculate average response time"""
        return statistics.mean(self.response_times) if self.response_times else 0.0

class DragonUI:
    """Enhanced User Interface Manager"""
    
    BANNER = """
    ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║
    ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║
    ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
    """
    
    def __init__(self, console: Console):
        self.console = console
        self.layout = Layout()
        self._setup_layout()
        
    def _setup_layout(self):
        """Setup enhanced UI layout"""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        self.layout["main"].split_row(
            Layout(name="stats"),
            Layout(name="monitor")
        )

class DragonNetworkTester:
    """Advanced Network Testing Suite with Enhanced Capabilities"""
    
    def __init__(self,
                 target_ip: str,
                 target_port: int,
                 duration: int,
                 thread_count: int = 10,
                 packet_size: int = 1024,
                 buffer_size: int = 65507,
                 verbose: bool = False):
        
        self.validate_input(target_ip, target_port, duration)
        
        self.target = (target_ip, target_port)
        self.duration = duration
        self.thread_count = min(thread_count, 500)  # Safety limit
        self.packet_size = min(packet_size, 65507)  # Max UDP packet size
        self.buffer_size = buffer_size
        self.verbose = verbose
        
        self.stats = NetworkStats()
        self.system_resources = SystemResources()
        self.packet_queue = queue.Queue(maxsize=100000)
        self.console = Console()
        self.stop_event = threading.Event()
        
        # Enhanced socket configurations
        self.socket_configs = {
            'timeout': 2.0,
            'keepalive': True,
            'blocking': 0
        }
        
        self._setup_logging()
        self._setup_sockets()
        self._check_target_availability()

    @staticmethod
    def validate_input(ip: str, port: int, duration: int) -> None:
        """Validate input parameters"""
        if not ip or not isinstance(ip, str):
            raise ValueError("Invalid IP address")
        if not 0 <= port <= 65535:
            raise ValueError("Port must be between 0 and 65535")
        if duration <= 0:
            raise ValueError("Duration must be positive")

    def _setup_logging(self) -> None:
        """Configure comprehensive logging system"""
        log_format = '%(asctime)s [%(threadName)s] %(levelname)s: %(message)s'
        logging.basicConfig(
            level=logging.DEBUG if self.verbose else logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('dragon_network_test.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def _setup_sockets(self) -> None:
        """Initialize and configure optimized network sockets"""
        self.sockets = []
        for _ in range(self.thread_count):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.socket_configs['timeout'])
            
            # Enhanced socket options
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.buffer_size)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            if hasattr(socket, 'SO_REUSEPORT'):  # Linux specific
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                
            self.sockets.append(sock)

    def _check_target_availability(self) -> None:
        """Verify target accessibility"""
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(2)
            test_socket.connect(self.target)
            test_socket.close()
        except Exception as e:
            logging.warning(f"Target may be unreachable: {str(e)}")

    def _monitor_system_resources(self) -> None:
        """Monitor system resource usage"""
        while not self.stop_event.is_set():
            self.system_resources.cpu_percent = psutil.cpu_percent()
            self.system_resources.memory_percent = psutil.virtual_memory().percent
            self.system_resources.active_connections = len(psutil.net_connections())
            time.sleep(1)

    def _generate_packet(self) -> bytes:
        """Generate sophisticated test packet with headers"""
        header = bytearray([
            random.randint(0, 255) for _ in range(24)
        ])
        payload = random._urandom(self.packet_size - 24)
        return bytes(header) + payload

    def _send_packets(self, socket_id: int) -> None:
        """Enhanced packet sending with advanced error handling and rate limiting"""
        sock = self.sockets[socket_id]
        
        while not self.stop_event.is_set():
            try:
                packet = self._generate_packet()
                start_time = time.time()
                
                sock.sendto(packet, self.target)
                
                response_time = time.time() - start_time
                with threading.Lock():
                    self.stats.packets_sent += 1
                    self.stats.bytes_sent += len(packet)
                    self.stats.response_times.append(response_time)
                    self.stats.packet_sizes.append(len(packet))
                
                # Adaptive rate limiting based on system load
                if self.system_resources.cpu_percent > 90:
                    time.sleep(0.01)
                elif self.stats.packets_sent % 1000 == 0:
                    time.sleep(0.001)
                    
            except Exception as e:
                with threading.Lock():
                    self.stats.failed_attempts += 1
                if self.verbose:
                    logging.error(f"Thread {socket_id} error: {str(e)}")
                time.sleep(0.1)

    def start(self) -> None:
        """Execute network test with comprehensive monitoring"""
        self.console.clear()
        self._display_banner()
        
        # Start system monitoring
        monitor_thread = threading.Thread(target=self._monitor_system_resources)
        monitor_thread.start()
        
        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            futures = [
                executor.submit(self._send_packets, i)
                for i in range(self.thread_count)
            ]
            
            # Start progress display
            progress_thread = threading.Thread(target=self._display_progress)
            progress_thread.start()
            
            # Wait for duration
            time.sleep(self.duration)
            self.stop_event.set()
            
            # Cleanup
            for future in futures:
                future.result()
            progress_thread.join()
            monitor_thread.join()
            
        self._display_final_report()
        self._cleanup()

    def _display_final_report(self) -> None:
        """Generate comprehensive final report"""
        self.console.print("\n[bold green]Test Complete - Final Report[/bold green]")
        
        total_time = time.time() - self.stats.start_time
        packets_per_second = self.stats.packets_sent / total_time
        mb_sent = self.stats.bytes_sent / 1024 / 1024
        
        report_table = Table(show_header=True, header_style="bold magenta")
        report_table.add_column("Metric", style="cyan")
        report_table.add_column("Value", style="green")
        
        metrics = [
            ("Total Time", f"{total_time:.2f} seconds"),
            ("Total Packets", f"{self.stats.packets_sent:,}"),
            ("Total Data", f"{mb_sent:.2f} MB"),
            ("Packet Rate", f"{packets_per_second:.2f} packets/sec"),
            ("Failed Attempts", f"{self.stats.failed_attempts}"),
            ("Success Rate", f"{(1 - self.stats.failed_attempts/self.stats.packets_sent)*100:.2f}%"),
            ("Avg Response", f"{self.stats.average_response*1000:.2f} ms")
        ]
        
        for metric, value in metrics:
            report_table.add_row(metric, value)
            
        self.console.print(Panel(report_table, title="Final Report", border_style="green"))

    def _cleanup(self) -> None:
        """Perform cleanup operations"""
        for sock in self.sockets:
            try:
                sock.close()
            except:
                pass
        logging.info("Network test completed and resources cleaned up")

    def parse_arguments() -> argparse.Namespace:
        """Enhanced command line argument parser"""
        parser = argparse.ArgumentParser(
            description="DragonNetworkTester - Advanced Network Testing Suite",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        parser.add_argument("--ip", required=True, help="Target IP address")
        parser.add_argument("--port", type=int, default=80, help="Target port")
        parser.add_argument("--duration", type=int, required=True, help="Test duration in seconds")
        parser.add_argument("--threads", type=int, default=10, help="Number of threads")
        parser.add_argument("--packet-size", type=int, default=1024, help="Packet size in bytes")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
        return parser.parse_args()
    
    def _display_banner(self) -> None:
        """Display the program banner with styling"""
        self.console.print(DragonUI.BANNER, style="bold blue")
        self.console.print("\n[bold cyan]DragonNetworkTester[/bold cyan] - Advanced Network Testing Suite")
        self.console.print("Version 1.0 - Enhanced Edition\n")

class EnhancedNetworkTester(DragonNetworkTester):
    """Enhanced Network Testing Suite with Advanced UI"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = DragonUI(self.console)
        self.test_start_time = None
    
    def _display_progress(self) -> None:
        """Display real-time progress with enhanced visuals"""
        with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Running network test...", total=self.duration)
            while not progress.finished and not self.stop_event.is_set():
                progress.update(task, completed=time.time() - self.stats.start_time)
                time.sleep(0.1)
    
    def _generate_enhanced_packet(self) -> bytes:
        """Generate packet with advanced headers and patterns"""
        timestamp = int(time.time()).to_bytes(8, 'big')
        sequence = self.stats.packets_sent.to_bytes(8, 'big')
        flags = random.randint(0, 255).to_bytes(8, 'big')
        payload = random._urandom(self.packet_size - 24)
        return timestamp + sequence + flags + payload
    
    def _display_live_stats(self):
        """Display real-time statistics with enhanced visuals"""
        with Live(self.ui.layout, refresh_per_second=4) as live:
            while not self.stop_event.is_set():
                self._update_stats_display()
                time.sleep(0.25)
    
    def _update_stats_display(self):
        """Update UI with current statistics"""
        stats_table = Table(show_header=True, header_style="bold magenta", border_style="blue")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        # Add real-time statistics
        current_time = time.time() - self.stats.start_time
        packets_per_second = self.stats.packets_sent / max(current_time, 1)
        
        stats = [
            ("Time Elapsed", f"{current_time:.1f}s"),
            ("Packets Sent", f"{self.stats.packets_sent:,}"),
            ("Packet Rate", f"{packets_per_second:.1f}/s"),
            ("Success Rate", f"{self.stats.success_rate:.1f}%"),
            ("CPU Usage", f"{self.system_resources.cpu_percent:.1f}%"),
            ("Memory Usage", f"{self.system_resources.memory_percent:.1f}%")
        ]
        
        for metric, value in stats:
            stats_table.add_row(metric, value)
        
        self.ui.layout["stats"].update(
            Panel(stats_table, title="Live Statistics", border_style="blue")
        )

def parse_arguments() -> argparse.Namespace:
    """Enhanced command line argument parser"""
    parser = argparse.ArgumentParser(
        description="DragonNetworkTester - Advanced Network Testing Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--ip", required=True, help="Target IP address")
    parser.add_argument("--port", type=int, default=80, help="Target port")
    parser.add_argument("--duration", type=int, required=True, help="Test duration in seconds")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("--packet-size", type=int, default=1024, help="Packet size in bytes")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def main():
    """Enhanced main entry point"""
    console = Console()
    
    try:
        console.print(DragonUI.BANNER, style="bold blue")
        console.print("\n[bold cyan]DragonNetworkTester[/bold cyan] - Advanced Network Testing Suite")
        console.print("Version 1.0 - Enhanced Edition\n")
        
        args = parse_arguments()
        
        with console.status("[bold green]Initializing test suite..."):
            tester = EnhancedNetworkTester(
                target_ip=args.ip,
                target_port=args.port,
                duration=args.duration,
                thread_count=args.threads,
                packet_size=args.packet_size,
                verbose=args.verbose
            )
        
        tester.start()
        
    except KeyboardInterrupt:
        console.print("\n[bold red]Test interrupted by user[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Fatal error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
