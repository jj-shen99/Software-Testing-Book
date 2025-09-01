#!/usr/bin/env python3

import os
import time
import json
import yaml
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Dict, Any

class DataQualityMonitor(FileSystemEventHandler):
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "sample_analysis_results/test_data")
        self.config_file = os.path.join(self.base_dir, "scripts/test_data_validator_rules.yml")
        self.log_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "monitoring"
        )
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.setup_logging()
        self.load_config()
        self.metrics = {
            'files_processed': 0,
            'errors_found': 0,
            'warnings_issued': 0,
            'last_check': None
        }

    def setup_logging(self):
        """Configure logging"""
        log_file = os.path.join(self.log_dir, 'data_quality.log')
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
        """Load validation rules"""
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return
        if event.src_path.endswith('.json'):
            self.logger.info(f"New data file detected: {event.src_path}")
            self.validate_file(event.src_path)

    def on_modified(self, event):
        """Handle file modification"""
        if event.is_directory:
            return
        if event.src_path.endswith('.json'):
            self.logger.info(f"Data file modified: {event.src_path}")
            self.validate_file(event.src_path)

    def validate_file(self, file_path: str):
        """Validate a data file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            validation_result = self.validate_data(data)
            self.update_metrics(validation_result)
            self.check_alerts(validation_result, file_path)
            
            self.logger.info(f"Validation complete for {file_path}")
            self.save_validation_result(validation_result, file_path)
            
        except Exception as e:
            self.logger.error(f"Error validating {file_path}: {str(e)}")
            self.metrics['errors_found'] += 1

    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against rules"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(data.get('test_cases', [])),
            'valid_records': 0,
            'invalid_records': 0,
            'errors': [],
            'warnings': [],
            'metrics': {}
        }

        rules = self.config['quality']
        
        # Check completeness
        missing_fields = self._check_completeness(data, rules['completeness'])
        if missing_fields:
            result['errors'].extend(missing_fields)

        # Check consistency
        consistency_issues = self._check_consistency(data, rules['consistency'])
        if consistency_issues:
            result['warnings'].extend(consistency_issues)

        # Check validity
        validity_issues = self._check_validity(data, rules['validity'])
        if validity_issues:
            result['errors'].extend(validity_issues)

        # Calculate metrics
        result['metrics'] = self._calculate_metrics(data)
        
        return result

    def _check_completeness(self, data: Dict[str, Any], rules: Dict[str, Any]) -> list:
        """Check data completeness"""
        errors = []
        required_fields = rules['required_fields']
        
        for record in data.get('test_cases', []):
            missing = [field for field in required_fields if field not in record]
            if missing:
                errors.append(f"Missing required fields: {', '.join(missing)}")
                
        return errors

    def _check_consistency(self, data: Dict[str, Any], rules: Dict[str, Any]) -> list:
        """Check data consistency"""
        warnings = []
        check_rules = rules['check_rules']
        
        for record in data.get('test_cases', []):
            for rule in check_rules:
                if not self._evaluate_rule(record, rule):
                    warnings.append(f"Consistency rule failed: {rule}")
                    
        return warnings

    def _check_validity(self, data: Dict[str, Any], rules: Dict[str, Any]) -> list:
        """Check data validity"""
        errors = []
        format_rules = rules['format_rules']
        
        for record in data.get('test_cases', []):
            for rule in format_rules:
                if not self._evaluate_format(record, rule):
                    errors.append(f"Format rule failed: {rule}")
                    
        return errors

    def _evaluate_rule(self, record: Dict[str, Any], rule: str) -> bool:
        """Evaluate a consistency rule"""
        try:
            return eval(rule, {"__builtins__": {}}, record)
        except:
            return False

    def _evaluate_format(self, record: Dict[str, Any], rule: str) -> bool:
        """Evaluate a format rule"""
        if rule == 'sides_are_integers':
            return all(isinstance(x, int) for x in record.get('sides', []))
        elif rule == 'area_is_float':
            return isinstance(record.get('area'), float)
        elif rule == 'type_is_string':
            return isinstance(record.get('type'), str)
        return True

    def _calculate_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate data quality metrics"""
        metrics = {
            'completeness_score': 0,
            'consistency_score': 0,
            'validity_score': 0
        }
        
        total_records = len(data.get('test_cases', []))
        if total_records > 0:
            metrics['completeness_score'] = (
                1 - len(self._check_completeness(data, self.config['quality']['completeness']))
                / total_records
            )
            metrics['consistency_score'] = (
                1 - len(self._check_consistency(data, self.config['quality']['consistency']))
                / total_records
            )
            metrics['validity_score'] = (
                1 - len(self._check_validity(data, self.config['quality']['validity']))
                / total_records
            )
            
        return metrics

    def update_metrics(self, result: Dict[str, Any]):
        """Update monitoring metrics"""
        self.metrics['files_processed'] += 1
        self.metrics['errors_found'] += len(result['errors'])
        self.metrics['warnings_issued'] += len(result['warnings'])
        self.metrics['last_check'] = datetime.now().isoformat()

    def check_alerts(self, result: Dict[str, Any], file_path: str):
        """Check for alert conditions"""
        for error in result['errors']:
            if error in self.config['response']['error_levels']['critical']:
                self.logger.error(f"CRITICAL: {error} in {file_path}")
            elif error in self.config['response']['error_levels']['warning']:
                self.logger.warning(f"WARNING: {error} in {file_path}")
            else:
                self.logger.info(f"INFO: {error} in {file_path}")

    def save_validation_result(self, result: Dict[str, Any], file_path: str):
        """Save validation result"""
        base_name = os.path.basename(file_path)
        result_file = os.path.join(
            self.log_dir,
            f"validation_{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)

    def start_monitoring(self):
        """Start file system monitoring"""
        observer = Observer()
        observer.schedule(self, self.data_dir, recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.logger.info("Monitoring stopped")
        observer.join()

def main():
    monitor = DataQualityMonitor()
    monitor.logger.info("Starting data quality monitoring...")
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
