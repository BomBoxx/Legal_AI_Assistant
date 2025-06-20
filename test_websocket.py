#!/usr/bin/env python3
"""
Simple WebSocket test client for the legal assistant API
"""

import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/chat"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            
            # Test message
            test_message = "ما هي الجرائم التي يعاقب عليها القانون"
            print(f"Sending message: {test_message}")
            
            # Send message
            await websocket.send(test_message)
            
            # Wait for response
            response = await websocket.recv()
            print(f"Received response: {response}")
            
            # Parse response
            try:
                response_data = json.loads(response)
                print(f"\nResponse type: {response_data.get('type')}")
                print(f"Content length: {len(response_data.get('content', ''))}")
                print(f"Number of sources: {len(response_data.get('sources', []))}")
                
                print("\nContent preview:")
                print("-" * 50)
                content = response_data.get('content', '')
                print(content[:500] + "..." if len(content) > 500 else content)
                print("-" * 50)
                
                print("\nSources:")
                for i, source in enumerate(response_data.get('sources', []), 1):
                    print(f"  {i}. Article {source.get('article_number', 'N/A')}")
                    print(f"     Preview: {source.get('preview', '')[:100]}...")
                    
            except json.JSONDecodeError:
                print("Response is not valid JSON")
                print(f"Raw response: {response}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing WebSocket connection...")
    asyncio.run(test_websocket()) 