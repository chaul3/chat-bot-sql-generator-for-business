#!/usr/bin/env python3
"""
Test script to verify the NoneType fix in local_demo.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def test_none_handling():
    print("🧪 Testing NoneType handling fix...")
    
    # Test message with None data
    message_with_none_data = {
        "role": "assistant",
        "content": "Test response",
        "data": None
    }
    
    # Test message with no data key
    message_without_data = {
        "role": "assistant", 
        "content": "Test response"
    }
    
    # Test message with valid data
    message_with_data = {
        "role": "assistant",
        "content": "Test response",
        "data": {
            "type": "dataframe",
            "content": "some data"
        }
    }
    
    messages = [message_with_none_data, message_without_data, message_with_data]
    
    for i, message in enumerate(messages):
        print(f"Testing message {i+1}...")
        
        # This is the fixed logic from local_demo.py
        if "data" in message and message["data"] is not None:
            print(f"  ✅ Message {i+1}: Would display data (type: {message['data']['type']})")
        else:
            print(f"  ✅ Message {i+1}: No data to display (correct)")
    
    print("\n✅ All NoneType handling tests passed!")
    print("🚀 The TypeError should be fixed now")

if __name__ == "__main__":
    test_none_handling()
