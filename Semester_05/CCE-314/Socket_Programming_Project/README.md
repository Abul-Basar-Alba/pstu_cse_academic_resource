# Election Voting System - Socket Programming Project
## CCE-314 Networking Sessional

### 📋 Project Overview
This is a distributed election voting application that demonstrates **socket programming with multicast communication**. The system allows 5 independent electorates to cast votes for two candidates (A or B) using UDP multicast sockets. Each electorate can vote once and independently determine the election winner.

---

## 🎯 Project Requirements

### Features Implemented:
✅ **5 Independent Electorates** - Each running as a separate process  
✅ **Two Candidates** - Candidate A and Candidate B  
✅ **One Vote Per Electorate** - Vote can only be cast once  
✅ **Multicast Communication** - UDP multicast for broadcasting votes  
✅ **Independent Winner Determination** - Each electorate calculates winner independently  
✅ **Web Interface** - Modern, responsive web UI (no terminal display)  
✅ **Real-time Updates** - Live vote tracking and results

---

## 🛠️ Technical Implementation

### Socket Programming Concepts Used:

#### 1. **UDP Multicast Sockets**
- **Multicast Group**: `224.0.0.1` (Class D IP address)
- **Port**: `5007`
- **Protocol**: UDP (User Datagram Protocol)
- **Purpose**: Broadcasting votes to all electorates simultaneously

#### 2. **Socket Operations**
```python
# Creating multicast socket
socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Joining multicast group
socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Setting TTL for multicast
socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

# Sending multicast message
socket.sendto(message_bytes, (MULTICAST_GROUP, MULTICAST_PORT))
```

#### 3. **Threading**
- Each electorate runs a background thread to listen for incoming votes
- Main thread handles web interface and user interactions
- Thread-safe operations using locks (`threading.Lock()`)

#### 4. **Message Format**
```json
{
    "electorate_id": 1,
    "vote": "A",
    "timestamp": "2025-11-21T10:30:00"
}
```

---

## 🐍 Python Technologies Used

### Core Libraries:
1. **socket** - Network communication
2. **threading** - Concurrent vote listening
3. **struct** - Binary data packing for multicast
4. **json** - Message serialization
5. **Flask** - Web framework
6. **datetime** - Timestamp management

### Flask Framework:
- **Routes**: API endpoints for voting operations
- **Templates**: HTML rendering with Jinja2
- **Static Files**: CSS and JavaScript serving
- **JSON API**: RESTful communication

---

## 📁 Project Structure

```
Socket_Programing_Project/
│
├── app.py                  # Flask web application
├── electorate.py           # Electorate class with socket logic
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── PRESENTATION_GUIDE.md  # Presentation guidelines
│
├── templates/
│   └── index.html         # Main web interface
│
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
│
├── scripts/
│   ├── run_all.sh         # Run all 5 electorates
│   └── stop_all.sh        # Stop all processes
│
└── presentation/
    └── slides_content.md  # Presentation content
```

---

## 🚀 Installation & Setup

### Prerequisites:
- Python 3.7 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, etc.)

### Step 1: Install Dependencies
```bash
cd Socket_Programing_Project
pip install -r requirements.txt
```

### Step 2: Run Individual Electorate
```bash
# Run Electorate 1 (opens at http://localhost:5001)
python app.py 1

# Run Electorate 2 (opens at http://localhost:5002)
python app.py 2

# ... and so on for electorates 3, 4, 5
```

### Step 3: Run All Electorates (Linux/Mac)
```bash
chmod +x scripts/run_all.sh
./scripts/run_all.sh
```

### Step 4: Access Web Interfaces
Open these URLs in your browser:
- Electorate 1: http://localhost:5001
- Electorate 2: http://localhost:5002
- Electorate 3: http://localhost:5003
- Electorate 4: http://localhost:5004
- Electorate 5: http://localhost:5005

---

## 🎮 How to Use

1. **Open all 5 electorate web interfaces** in separate browser tabs
2. **Each electorate casts one vote** for Candidate A or B
3. **Votes are broadcast** via multicast to all other electorates
4. **Real-time updates** show received votes
5. **Winner is determined** independently by each electorate
6. **Results displayed** when all 5 votes are received

---

## 🔄 Working Mechanism

### Vote Casting Process:

1. **User clicks** vote button for Candidate A or B
2. **JavaScript sends** POST request to Flask backend
3. **Flask calls** `electorate.cast_vote()` method
4. **Vote is stored** locally with thread-safe lock
5. **JSON message created** with electorate ID, vote, timestamp
6. **Message broadcast** via UDP multicast socket
7. **All listening electorates** receive the message
8. **Each electorate updates** its local vote tally
9. **Frontend polls** backend every 2 seconds
10. **Results calculated** and displayed when all votes received

### Winner Determination Algorithm:
```python
votes_a = count of 'A' votes
votes_b = count of 'B' votes

if votes_a > votes_b:
    winner = 'A'
elif votes_b > votes_a:
    winner = 'B'
else:
    winner = 'TIE'
```

---

## 🌐 Network Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Electorate 1│     │ Electorate 2│     │ Electorate 3│
│  (Port 5001)│     │  (Port 5002)│     │  (Port 5003)│
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Multicast Group       │
              │   224.0.0.1:5007       │
              └────────────┬────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐     ┌──────▼──────┐
│ Electorate 4│     │ Electorate 5│
│  (Port 5004)│     │  (Port 5005)│
└─────────────┘     └─────────────┘
```

---

## 📊 API Endpoints

### GET `/`
Returns the main web interface

### GET `/api/info`
Returns electorate information
```json
{
    "electorate_id": 1,
    "multicast_group": "224.0.0.1",
    "multicast_port": 5007
}
```

### GET `/api/status`
Returns current voting status
```json
{
    "electorate_id": 1,
    "has_voted": true,
    "my_vote": "A",
    "votes_received": 3,
    "received_from": [1, 2, 3]
}
```

### POST `/api/vote`
Cast a vote (A or B)
```json
Request: {"vote": "A"}
Response: {"success": true, "message": "Vote cast successfully"}
```

### GET `/api/results`
Get election results
```json
{
    "ready": true,
    "total_votes": 5,
    "votes_for_a": 3,
    "votes_for_b": 2,
    "winner": "A",
    "all_votes_received": true
}
```

---

## 🎥 Presentation Guidelines

### Slide Structure (8-10 slides):

1. **Title Slide** - Project name, your name, course
2. **Problem Statement** - Election voting requirements
3. **Socket Programming Concepts** - UDP, Multicast, Threading
4. **System Architecture** - Network diagram
5. **Python Implementation** - Key code snippets
6. **Web Interface Demo** - Live demonstration
7. **Results & Testing** - Show vote casting and winner
8. **Conclusion** - Learning outcomes

### Video Recording Tips:
- Use **OBS Studio** or **Zoom** for recording
- Show your face via **webcam** (picture-in-picture)
- Record **live demo** of all 5 electorates voting
- Explain concepts in **English**
- Keep video under **10 minutes**
- Show **code walkthrough** briefly

---

## 🐛 Troubleshooting

### Issue: "Address already in use"
**Solution**: Change port number or stop existing processes
```bash
# Find process using port
lsof -i :5001
# Kill process
kill -9 <PID>
```

### Issue: Votes not received
**Solution**: Check firewall settings for multicast traffic
```bash
# Allow multicast on Linux
sudo iptables -A INPUT -d 224.0.0.0/4 -j ACCEPT
```

### Issue: Flask not installed
**Solution**: Install requirements
```bash
pip install flask
```

---

## 📚 Learning Outcomes

### Socket Programming:
✅ UDP vs TCP protocols  
✅ Multicast communication  
✅ Socket creation and configuration  
✅ Message broadcasting  

### Python Programming:
✅ Threading and synchronization  
✅ Web framework (Flask)  
✅ JSON serialization  
✅ Class-based design  

### Web Development:
✅ HTML/CSS/JavaScript  
✅ AJAX/Fetch API  
✅ Real-time updates  
✅ Responsive design  

---

## 👨‍💻 Author
**Your Name**  
Student ID: [Your ID]  
Course: CCE-314 Networking Sessional  
Institution: [Your Institution]

---

## 📄 License
This project is for educational purposes as part of CCE-314 coursework.

---

## 🙏 Acknowledgments
- Course Instructor: Swarna Ma'am
- Socket Programming concepts from Stevens' Unix Network Programming
- Flask documentation and examples

---

**Note**: This project demonstrates distributed systems concepts including multicast communication, concurrent programming, and web-based interfaces for network applications.
