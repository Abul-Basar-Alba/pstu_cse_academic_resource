"""
Election Voting System using Multicast Socket Programming
Each electorate can cast vote and receive votes from others via UDP multicast
"""

import socket
import struct
import threading
import time
import json
from datetime import datetime

class Electorate:
    # Multicast group configuration
    MULTICAST_GROUP = '224.0.0.1'
    MULTICAST_PORT = 5007
    
    def __init__(self, electorate_id):
        self.electorate_id = electorate_id
        self.my_vote = None
        self.received_votes = {}
        self.vote_lock = threading.Lock()
        self.has_voted = False
        
        # Create multicast socket for receiving
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_socket.bind(('', self.MULTICAST_PORT))
        
        # Join multicast group
        mreq = struct.pack('4sL', socket.inet_aton(self.MULTICAST_GROUP), socket.INADDR_ANY)
        self.recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        # Create socket for sending
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
        # Start listening thread
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_for_votes, daemon=True)
        self.listen_thread.start()
        
        print(f"Electorate {self.electorate_id} initialized and listening on {self.MULTICAST_GROUP}:{self.MULTICAST_PORT}")
    
    def _listen_for_votes(self):
        """Listen for multicast vote messages from other electorates"""
        while self.listening:
            try:
                data, address = self.recv_socket.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                
                sender_id = message.get('electorate_id')
                vote = message.get('vote')
                timestamp = message.get('timestamp')
                
                # Don't process our own vote
                if sender_id != self.electorate_id:
                    with self.vote_lock:
                        if sender_id not in self.received_votes:
                            self.received_votes[sender_id] = vote
                            print(f"Electorate {self.electorate_id} received vote from Electorate {sender_id}: {vote}")
                
            except Exception as e:
                if self.listening:
                    print(f"Error receiving vote: {e}")
    
    def cast_vote(self, vote):
        """Cast vote by sending multicast message"""
        if self.has_voted:
            return {"success": False, "message": "You have already voted!"}
        
        if vote not in ['A', 'B']:
            return {"success": False, "message": "Invalid vote! Choose A or B"}
        
        # Record own vote
        with self.vote_lock:
            self.my_vote = vote
            self.received_votes[self.electorate_id] = vote
            self.has_voted = True
        
        # Create vote message
        message = {
            'electorate_id': self.electorate_id,
            'vote': vote,
            'timestamp': datetime.now().isoformat()
        }
        
        # Send multicast message
        try:
            message_bytes = json.dumps(message).encode('utf-8')
            self.send_socket.sendto(message_bytes, (self.MULTICAST_GROUP, self.MULTICAST_PORT))
            print(f"Electorate {self.electorate_id} cast vote: {vote}")
            return {"success": True, "message": f"Vote cast successfully for candidate {vote}"}
        except Exception as e:
            print(f"Error casting vote: {e}")
            return {"success": False, "message": f"Error casting vote: {e}"}
    
    def get_results(self):
        """Calculate and return election results"""
        with self.vote_lock:
            if not self.has_voted:
                return {
                    "ready": False,
                    "message": "You must cast your vote first!"
                }
            
            total_votes = len(self.received_votes)
            votes_a = sum(1 for v in self.received_votes.values() if v == 'A')
            votes_b = sum(1 for v in self.received_votes.values() if v == 'B')
            
            winner = None
            if total_votes == 5:  # All votes received
                if votes_a > votes_b:
                    winner = 'A'
                elif votes_b > votes_a:
                    winner = 'B'
                else:
                    winner = 'TIE'
            
            return {
                "ready": True,
                "total_votes": total_votes,
                "votes_for_a": votes_a,
                "votes_for_b": votes_b,
                "winner": winner,
                "my_vote": self.my_vote,
                "all_votes_received": total_votes == 5,
                "received_votes": dict(self.received_votes)
            }
    
    def get_status(self):
        """Get current voting status"""
        with self.vote_lock:
            return {
                "electorate_id": self.electorate_id,
                "has_voted": self.has_voted,
                "my_vote": self.my_vote,
                "votes_received": len(self.received_votes),
                "received_from": list(self.received_votes.keys())
            }
    
    def cleanup(self):
        """Cleanup resources"""
        self.listening = False
        self.recv_socket.close()
        self.send_socket.close()
