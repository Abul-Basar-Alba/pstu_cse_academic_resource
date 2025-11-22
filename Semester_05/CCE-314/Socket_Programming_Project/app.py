"""
Flask Web Application for Election Voting System
Provides web interface for socket-based multicast voting
"""

from flask import Flask, render_template, request, jsonify
from electorate import Electorate
import sys

app = Flask(__name__)

# Global electorate instance
electorate = None

@app.route('/')
def index():
    """Render main voting interface"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current voting status"""
    if electorate is None:
        return jsonify({"error": "Electorate not initialized"}), 500
    
    status = electorate.get_status()
    return jsonify(status)

@app.route('/api/vote', methods=['POST'])
def cast_vote():
    """Cast a vote for candidate A or B"""
    if electorate is None:
        return jsonify({"error": "Electorate not initialized"}), 500
    
    data = request.get_json()
    vote = data.get('vote', '').upper()
    
    result = electorate.cast_vote(vote)
    return jsonify(result)

@app.route('/api/results')
def get_results():
    """Get election results"""
    if electorate is None:
        return jsonify({"error": "Electorate not initialized"}), 500
    
    results = electorate.get_results()
    return jsonify(results)

@app.route('/api/info')
def get_info():
    """Get electorate information"""
    if electorate is None:
        return jsonify({"error": "Electorate not initialized"}), 500
    
    return jsonify({
        "electorate_id": electorate.electorate_id,
        "multicast_group": electorate.MULTICAST_GROUP,
        "multicast_port": electorate.MULTICAST_PORT
    })

def main():
    """Main entry point"""
    global electorate
    
    # Get electorate ID from command line argument
    if len(sys.argv) > 1:
        try:
            electorate_id = int(sys.argv[1])
            if electorate_id < 1 or electorate_id > 5:
                print("Electorate ID must be between 1 and 5")
                sys.exit(1)
        except ValueError:
            print("Invalid electorate ID. Must be a number between 1 and 5")
            sys.exit(1)
    else:
        electorate_id = 1  # Default
        print("No electorate ID provided, using default: 1")
    
    # Get port from command line argument (optional)
    port = 5000 + electorate_id  # Different port for each electorate
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print(f"Invalid port number, using default: {port}")
    
    # Initialize electorate
    print(f"\n{'='*60}")
    print(f"Starting Election Voting System")
    print(f"Electorate ID: {electorate_id}")
    print(f"Web Interface: http://localhost:{port}")
    print(f"{'='*60}\n")
    
    electorate = Electorate(electorate_id)
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main()
