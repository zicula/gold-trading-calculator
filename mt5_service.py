"""
Windows Service Installer for MT5 Trading Server
Converts the Python server into a Windows Service for VPS
"""

import sys
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import subprocess
import time
import logging

class MT5TradingService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MT5TradingServer"
    _svc_display_name_ = "MT5 Trading Server"
    _svc_description_ = "Production MT5 Trading Server for Gold Calculator"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        
        # Setup logging
        self.log_file = os.path.join(os.getcwd(), 'mt5_service.log')
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        logging.info("Service stop requested")
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        """Run the service"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        logging.info("MT5 Trading Service starting...")
        self.main()
        
    def main(self):
        """Main service loop"""
        try:
            # Get service directory
            service_dir = os.path.dirname(os.path.abspath(__file__))
            server_script = os.path.join(service_dir, 'production_server.py')
            
            # Change to service directory
            os.chdir(service_dir)
            
            # Start the Python server
            logging.info(f"Starting server: {server_script}")
            
            # Use virtual environment if available
            venv_python = os.path.join(service_dir, 'venv', 'Scripts', 'python.exe')
            python_exe = venv_python if os.path.exists(venv_python) else 'python'
            
            # Start server process
            self.server_process = subprocess.Popen([
                python_exe, 
                server_script
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            logging.info(f"Server started with PID: {self.server_process.pid}")
            
            # Wait for stop signal or process to end
            while True:
                # Check if service should stop
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
                if rc == win32event.WAIT_OBJECT_0:
                    logging.info("Service stop signal received")
                    break
                
                # Check if server process is still running
                if self.server_process.poll() is not None:
                    logging.error("Server process ended unexpectedly")
                    # Try to restart
                    time.sleep(5)
                    self.server_process = subprocess.Popen([
                        python_exe, 
                        server_script
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    logging.info(f"Server restarted with PID: {self.server_process.pid}")
            
            # Cleanup
            if self.server_process and self.server_process.poll() is None:
                logging.info("Terminating server process")
                self.server_process.terminate()
                self.server_process.wait(timeout=10)
                
        except Exception as e:
            logging.error(f"Service error: {e}")
            servicemanager.LogErrorMsg(f"Service error: {e}")

def install_service():
    """Install the Windows service"""
    try:
        win32serviceutil.InstallService(
            MT5TradingService,
            MT5TradingService._svc_name_,
            MT5TradingService._svc_display_name_,
            startType=win32service.SERVICE_AUTO_START,
            description=MT5TradingService._svc_description_
        )
        print("✅ Service installed successfully")
        print(f"Service Name: {MT5TradingService._svc_name_}")
        print(f"Display Name: {MT5TradingService._svc_display_name_}")
        print("\nTo start the service, run:")
        print(f"net start {MT5TradingService._svc_name_}")
        
    except Exception as e:
        print(f"❌ Failed to install service: {e}")

def uninstall_service():
    """Uninstall the Windows service"""
    try:
        win32serviceutil.RemoveService(MT5TradingService._svc_name_)
        print("✅ Service uninstalled successfully")
        
    except Exception as e:
        print(f"❌ Failed to uninstall service: {e}")

def start_service():
    """Start the service"""
    try:
        win32serviceutil.StartService(MT5TradingService._svc_name_)
        print("✅ Service started successfully")
        
    except Exception as e:
        print(f"❌ Failed to start service: {e}")

def stop_service():
    """Stop the service"""
    try:
        win32serviceutil.StopService(MT5TradingService._svc_name_)
        print("✅ Service stopped successfully")
        
    except Exception as e:
        print(f"❌ Failed to stop service: {e}")

def main():
    """Main function for service management"""
    if len(sys.argv) == 1:
        # No arguments - show help
        print("MT5 Trading Service Manager")
        print("============================")
        print("Usage:")
        print("  python mt5_service.py install   - Install service")
        print("  python mt5_service.py uninstall - Uninstall service")
        print("  python mt5_service.py start     - Start service")
        print("  python mt5_service.py stop      - Stop service")
        print("  python mt5_service.py restart   - Restart service")
        print("  python mt5_service.py debug     - Run in debug mode")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'install':
        install_service()
    elif command == 'uninstall':
        uninstall_service()
    elif command == 'start':
        start_service()
    elif command == 'stop':
        stop_service()
    elif command == 'restart':
        stop_service()
        time.sleep(2)
        start_service()
    elif command == 'debug':
        # Run service in debug mode
        print("Running in debug mode...")
        service = MT5TradingService(sys.argv)
        service.main()
    else:
        # Handle service control manager
        win32serviceutil.HandleCommandLine(MT5TradingService)

if __name__ == '__main__':
    main()
