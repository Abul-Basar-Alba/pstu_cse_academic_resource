#!/bin/bash

# Demo script with visual output
# Shows step-by-step what's happening

clear

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║        🗳️  ELECTION VOTING SYSTEM DEMO 🗳️                 ║"
echo "║                                                            ║"
echo "║              Socket Programming Project                    ║"
echo "║              CCE-314 Networking Sessional                 ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "This demo will:"
echo "  1. Check Python installation"
echo "  2. Install Flask if needed"
echo "  3. Start all 5 electorates"
echo "  4. Show you the browser URLs"
echo ""
read -p "Press ENTER to continue..."

# Check Python
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Checking Python installation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python3 found: $PYTHON_VERSION"
else
    echo "✗ Python3 not found!"
    echo "  Please install Python 3.7 or higher"
    exit 1
fi

# Check Flask
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Checking Flask installation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if python3 -c "import flask" &> /dev/null; then
    FLASK_VERSION=$(python3 -c "import flask; print(flask.__version__)")
    echo "✓ Flask found: version $FLASK_VERSION"
else
    echo "⚠ Flask not found. Installing..."
    pip install flask
    echo "✓ Flask installed successfully"
fi

# Kill existing processes
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Cleaning up existing processes..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for port in 5001 5002 5003 5004 5005; do
    if lsof -ti:$port &> /dev/null; then
        echo "✓ Stopped process on port $port"
        kill -9 $(lsof -ti:$port) 2>/dev/null
    fi
done
pkill -f "python.*app.py" 2>/dev/null
echo "✓ Cleanup complete"

sleep 1

# Start electorates
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Starting all 5 electorates..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Function to start electorate
start_electorate() {
    local id=$1
    local port=$((5000 + id))
    
    python3 app.py $id > /dev/null 2>&1 &
    sleep 1
    
    if lsof -ti:$port &> /dev/null; then
        echo "✓ Electorate $id started successfully on port $port"
    else
        echo "✗ Failed to start Electorate $id"
    fi
}

# Start all electorates
for i in 1 2 3 4 5; do
    start_electorate $i
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: System Ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Open these URLs in your browser (5 separate tabs):"
echo ""
echo "   Tab 1:  http://localhost:5001  (Electorate 1)"
echo "   Tab 2:  http://localhost:5002  (Electorate 2)"
echo "   Tab 3:  http://localhost:5003  (Electorate 3)"
echo "   Tab 4:  http://localhost:5004  (Electorate 4)"
echo "   Tab 5:  http://localhost:5005  (Electorate 5)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "How to use:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Click vote button (A or B) in each tab"
echo "2. Watch votes appear in real-time across all tabs"
echo "3. After all 5 votes, winner will be announced"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Technical Details:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔌 Socket Programming:"
echo "   • Protocol: UDP (User Datagram Protocol)"
echo "   • Type: Multicast Communication"
echo "   • Group: 224.0.0.1"
echo "   • Port: 5007"
echo ""
echo "🐍 Python Technologies:"
echo "   • socket - Network communication"
echo "   • threading - Concurrent operations"
echo "   • Flask - Web framework"
echo "   • json - Message format"
echo ""
echo "🌐 Web Interface:"
echo "   • HTML/CSS/JavaScript"
echo "   • AJAX real-time updates"
echo "   • REST API endpoints"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "To stop all electorates:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run: ./scripts/stop_all.sh"
echo "Or press: Ctrl+C"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  DEMO READY - ENJOY! 🎉                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Keep script running
wait
