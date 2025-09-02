#!/usr/bin/env python3

import os
from metrics_dashboard import MetricsDashboard

def main():
    dashboard = MetricsDashboard()
    dashboard.app.run(debug=True, port=8051)

if __name__ == '__main__':
    main()
