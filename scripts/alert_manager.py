#!/usr/bin/env python3

import os
import json
import yaml
import logging
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List

class AlertManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(
            self.base_dir,
            "workflows/yaml_workflows/monitoring_config.yml"
        )
        self.alerts_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "alerts"
        )
        os.makedirs(self.alerts_dir, exist_ok=True)
        self.setup_logging()
        self.load_config()

    def setup_logging(self):
        """Configure logging"""
        log_file = os.path.join(self.alerts_dir, 'alerts.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        """Load alert configuration"""
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)['alerts']

    def process_alert(self, alert: Dict[str, Any]):
        """Process and route alert"""
        self.logger.info(f"Processing alert: {alert['metric']}")
        
        # Save alert
        self._save_alert(alert)
        
        # Route alert based on severity
        if alert['severity'] == 'critical':
            self._send_critical_alert(alert)
        elif alert['severity'] == 'warning':
            self._send_warning_alert(alert)
        else:
            self._send_info_alert(alert)

    def _save_alert(self, alert: Dict[str, Any]):
        """Save alert to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        alert_file = os.path.join(
            self.alerts_dir,
            f"alert_{alert['severity']}_{timestamp}.json"
        )
        
        with open(alert_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'alert': alert
            }, f, indent=2)

    def _send_critical_alert(self, alert: Dict[str, Any]):
        """Send critical alert"""
        # Send to all configured channels
        for channel in self.config['channels']:
            if channel['enabled']:
                self._send_alert(alert, channel)

    def _send_warning_alert(self, alert: Dict[str, Any]):
        """Send warning alert"""
        # Send to configured warning channels
        for channel in self.config['channels']:
            if channel['enabled'] and 'warning' in channel['levels']:
                self._send_alert(alert, channel)

    def _send_info_alert(self, alert: Dict[str, Any]):
        """Send info alert"""
        # Send to configured info channels
        for channel in self.config['channels']:
            if channel['enabled'] and 'info' in channel['levels']:
                self._send_alert(alert, channel)

    def _send_alert(self, alert: Dict[str, Any], channel: Dict[str, Any]):
        """Send alert through specified channel"""
        try:
            if channel['type'] == 'email':
                self._send_email_alert(alert, channel)
            elif channel['type'] == 'slack':
                self._send_slack_alert(alert, channel)
            elif channel['type'] == 'webhook':
                self._send_webhook_alert(alert, channel)
        except Exception as e:
            self.logger.error(f"Error sending alert via {channel['type']}: {str(e)}")

    def _send_email_alert(self, alert: Dict[str, Any], channel: Dict[str, Any]):
        """Send email alert"""
        msg = MIMEMultipart()
        msg['From'] = channel['from']
        msg['To'] = ', '.join(channel['recipients'])
        msg['Subject'] = f"[{alert['severity'].upper()}] {alert['metric']} Alert"
        
        body = f"""
        Alert Details:
        - Metric: {alert['metric']}
        - Value: {alert['value']}
        - Threshold: {alert['threshold']}
        - Time: {datetime.now().isoformat()}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(channel['smtp_server']) as server:
            if channel.get('use_tls'):
                server.starttls()
            if channel.get('username') and channel.get('password'):
                server.login(channel['username'], channel['password'])
            server.send_message(msg)

    def _send_slack_alert(self, alert: Dict[str, Any], channel: Dict[str, Any]):
        """Send Slack alert"""
        payload = {
            'text': f"*[{alert['severity'].upper()}] {alert['metric']} Alert*\n"
                   f"Value: {alert['value']}\n"
                   f"Threshold: {alert['threshold']}\n"
                   f"Time: {datetime.now().isoformat()}"
        }
        
        requests.post(
            channel['webhook_url'],
            json=payload,
            headers={'Content-Type': 'application/json'}
        )

    def _send_webhook_alert(self, alert: Dict[str, Any], channel: Dict[str, Any]):
        """Send webhook alert"""
        payload = {
            'severity': alert['severity'],
            'metric': alert['metric'],
            'value': alert['value'],
            'threshold': alert['threshold'],
            'timestamp': datetime.now().isoformat()
        }
        
        requests.post(
            channel['url'],
            json=payload,
            headers=channel.get('headers', {})
        )

    def check_alert_status(self, alert_id: str) -> Dict[str, Any]:
        """Check status of specific alert"""
        alert_file = os.path.join(self.alerts_dir, f"{alert_id}.json")
        if os.path.exists(alert_file):
            with open(alert_file, 'r') as f:
                return json.load(f)
        return None

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active alerts"""
        active_alerts = []
        for file in os.listdir(self.alerts_dir):
            if file.endswith('.json'):
                with open(os.path.join(self.alerts_dir, file), 'r') as f:
                    alert = json.load(f)
                    if not alert.get('resolved'):
                        active_alerts.append(alert)
        return active_alerts

    def resolve_alert(self, alert_id: str):
        """Mark alert as resolved"""
        alert_file = os.path.join(self.alerts_dir, f"{alert_id}.json")
        if os.path.exists(alert_file):
            with open(alert_file, 'r') as f:
                alert = json.load(f)
            
            alert['resolved'] = True
            alert['resolved_at'] = datetime.now().isoformat()
            
            with open(alert_file, 'w') as f:
                json.dump(alert, f, indent=2)

def main():
    alert_manager = AlertManager()
    
    # Example alert
    alert = {
        'severity': 'warning',
        'metric': 'cpu_usage',
        'value': 85.5,
        'threshold': 80.0
    }
    
    alert_manager.process_alert(alert)

if __name__ == "__main__":
    main()
