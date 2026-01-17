#!/bin/bash

echo "=== ArkBot Performance Report ==="
echo "Report Time: $(date)"
echo "Report Period: Last 24 hours"
echo ""

if [ ! -f logs/arkbot.log ]; then
    echo "Error: logs/arkbot.log not found"
    exit 1
fi

# Request count
TOTAL_REQUESTS=$(grep "Received message" logs/arkbot.log | wc -l)
echo "Total Requests: $TOTAL_REQUESTS"

# Error count
TOTAL_ERRORS=$(grep -E "ERROR|Exception" logs/arkbot.log | wc -l)
echo "Total Errors: $TOTAL_ERRORS"

# Error rate
if [ $TOTAL_REQUESTS -gt 0 ]; then
    ERROR_RATE=$(awk "BEGIN {printf \"%.2f\", ($TOTAL_ERRORS/$TOTAL_REQUESTS)*100}")
    echo "Error Rate: ${ERROR_RATE}%"
else
    echo "Error Rate: N/A (no requests)"
fi

# Function calls
FUNCTION_CALLS=$(grep "Calling function:" logs/arkbot.log | wc -l)
echo "Function Calls: $FUNCTION_CALLS"

# Most called functions
echo ""
echo "Top 5 Functions Called:"
if [ $FUNCTION_CALLS -gt 0 ]; then
    grep "Calling function:" logs/arkbot.log | awk -F': ' '{print $2}' | sort | uniq -c | sort -rn | head -5
else
    echo "  No function calls found"
fi

# API errors
echo ""
echo "API Error Breakdown:"
echo "  429 (Quota Exceeded): $(grep "429" logs/arkbot.log | wc -l)"
echo "  500 (Server Error): $(grep "500" logs/arkbot.log | wc -l)"
echo "  Other: $(grep -E "APIError|ToolExecutionError" logs/arkbot.log | wc -l)"

echo ""
echo "=== Report Complete ==="
