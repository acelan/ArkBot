#!/bin/bash

echo "=== ArkBot Health Check ==="
echo "Time: $(date)"
echo ""

# Process check
if pgrep -f arkbot_cli.py > /dev/null; then
    echo "✓ Bot process is running"
    PID=$(pgrep -f arkbot_cli.py)
    echo "  PID: $PID"
else
    echo "✗ Bot process is NOT running"
    exit 1
fi

# Memory check
RSS=$(ps -o rss= -p $PID)
RSS_MB=$((RSS / 1024))
echo ""
echo "Memory Usage: ${RSS_MB} MB"
if [ $RSS_MB -lt 500 ]; then
    echo "✓ Memory usage is normal"
else
    echo "⚠ Memory usage is high"
fi

# Recent errors check
echo ""
echo "Recent Errors (last 10):"
if [ -f logs/arkbot.log ]; then
    tail -100 logs/arkbot.log | grep -i error | tail -10
else
    echo "  No log file found"
fi

# Recent activity
echo ""
echo "Recent Activity (last 5 messages):"
if [ -f logs/arkbot.log ]; then
    tail -100 logs/arkbot.log | grep "Received message" | tail -5
else
    echo "  No log file found"
fi

echo ""
echo "=== Health Check Complete ==="
