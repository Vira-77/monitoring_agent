# Server metrics dashboard - Group 7

## Overview

This project is a web application designed to monitor and manage server metrics, including CPU usage, memory usage, disk usage, and logs. It provides real-time data visualization and historical tracking through a user-friendly interface.

## Features

- **Real-Time Server Metrics**: Displays CPU, memory, disk usage, and log data in real-time.
- **Historical Data**: Stores and visualizes historical data of server metrics.
- **Responsive Design**: Works seamlessly across desktops and mobile devices.
- **Easy-to-Use Interface**: Provides intuitive controls for viewing server health.
- **Customizable Alerts**: Setup alerts for critical server conditions (not yet implemented, if applicable).
  
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)

## Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

- Python 3.7+
- Docker (optional for containerized setups)

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repo-url> monitoring_agent
   cd monitoring_agent/web-ui
   ```

2. **Install backend dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**

   To run the backend, you can use:

   ```bash
   python src/app.py
   ```

   Or for Docker users:

   ```bash
   docker build -t monitoring-web-ui .
   docker run -p 8050:8050 monitoring-web-ui
   ```

## Usage

1. Start the application (as detailed in the Installation section).
2. Open your web browser and go to `http://localhost:8050` or the URL specified for the application.
3. The dashboard will display server metrics and historical data. You can view CPU, memory, disk usage, and logs.

## Testing

To run the tests:

1. Install test dependencies:

   ```bash
   pip install -r requirements.dev.txt
   ```

2. Run the tests:

   ```bash
   make coverage-test
   ```
