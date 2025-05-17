import cv2
import mediapipe as mp
import pyautogui
import os
from datetime import datetime

def update_html_viewer():
    """Updates the standalone HTML file with current screenshots"""
    screenshots = sorted([
        f for f in os.listdir('screenshots') 
        if f.endswith('.png')
    ], reverse=True)

    latest_img = screenshots[0] if screenshots else None
    older_imgs = screenshots[1:]

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Screenshot Viewer</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f4f4f4;
                color: #333;
            }}
            h1 {{
                text-align: center;
            }}
            .screenshot {{
                margin: 20px auto;
                padding: 10px;
                background: white;
                border: 1px solid #ccc;
                max-width: 90%;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            img {{
                max-width: 100%;
                height: auto;
                border-radius: 5px;
            }}
            .button {{
                display: block;
                margin: 20px auto;
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                text-align: center;
                border-radius: 5px;
                text-decoration: none;
                cursor: pointer;
                width: fit-content;
            }}
            #olderScreenshots {{
                display: none;
            }}
        </style>
        <script>
            function toggleMore() {{
                var section = document.getElementById('olderScreenshots');
                var btn = document.getElementById('toggleButton');
                if (section.style.display === 'none') {{
                    section.style.display = 'block';
                    btn.innerText = 'Show Less';
                }} else {{
                    section.style.display = 'none';
                    btn.innerText = 'Show More';
                }}
            }}
        </script>
    </head>
    <body>
        <h1>Your imported picture</h1>
        {f'''
        <div class="screenshot">
            <img src="screenshots/{latest_img}" alt="Latest Screenshot">
            <p><a href="screenshots/{latest_img}" download>Download</a></p>
        </div>
        ''' if latest_img else "<p>No screenshots yet.</p>"}

        {"<button class='button' id='toggleButton' onclick='toggleMore()'>Show More</button>" if older_imgs else ""}

        <div id="olderScreenshots">
            {"".join(
                f'<div class="screenshot">'
                f'<img src="screenshots/{img}" alt="Screenshot">'
                f'<p><a href="screenshots/{img}" download>Download</a></p>'
                f'</div>'
                for img in older_imgs
            )}
        </div>
    </body>
    </html>
    """

    with open('viewer.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

# Setup hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

# Create screenshots directory if not exists
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Variables for gesture detection
fist_closed = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue
    
    # Process image
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        
        # Check for closed fist
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        
        if thumb_tip.y > index_tip.y:  # Fist closed
            if not fist_closed:
                fist_closed = True
                # Take and save screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshots/screenshot_{timestamp}.png"
                pyautogui.screenshot().save(filename)
                print(f"Saved: {filename}")
                update_html_viewer()  # Update the HTML file
        else:
            fist_closed = False
    
    # Display camera feed
    cv2.imshow('Gesture Control', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
