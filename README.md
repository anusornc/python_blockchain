# บล็อกเชนด้วย Python

โปรเจกต์นี้เป็นการสร้างบล็อกเชนอย่างง่ายด้วย Python โดยมีทั้งอินเตอร์เฟซ HTTP และ P2P ออกแบบมาเพื่อวัตถุประสงค์ทางการศึกษาเพื่อสาธิตแนวคิดพื้นฐานของบล็อกเชน ได้รับแรงบันดาลใจจาก https://github.com/lhartikk/naivechain

## คุณสมบัติ

- การทำงานของบล็อกเชนแบบ proof-of-work อย่างง่าย
- API แบบ HTTP สำหรับโต้ตอบกับบล็อกเชน
- ความสามารถเครือข่าย P2P สำหรับการสื่อสารระหว่างโหนด
- ฟังก์ชันการขุดบล็อก

## ความต้องการเบื้องต้น

- Python 3.7 หรือใหม่กว่า

## การติดตั้ง

1. โคลนที่เก็บ:
   ```
   git clone https://github.com/yourusername/python-blockchain.git
   cd python-blockchain
   ```

2. ตั้งค่าสภาพแวดล้อมเสมือน:
   ```
   python -m venv venv
   ```

3. เปิดใช้งานสภาพแวดล้อมเสมือน:
   - บน Windows:
     ```
     venv\Scripts\activate
     ```
   - บน macOS และ Linux:
     ```
     source venv/bin/activate
     ```

4. ติดตั้งแพ็คเกจที่จำเป็น:
   ```
   pip install flask flask-cors websockets
   ```

## การใช้งาน

1. เริ่มต้นโหนดบล็อกเชน:
   ```
   python blockchain.py
   ```
   นี่จะเริ่มทั้งเซิร์ฟเวอร์ HTTP (พอร์ตเริ่มต้น 3001) และเซิร์ฟเวอร์ P2P (พอร์ตเริ่มต้น 6001)

2. โต้ตอบกับบล็อกเชนโดยใช้คำขอ HTTP:
   - ดูบล็อกเชนปัจจุบัน:
     ```
     curl http://localhost:3001/blocks
     ```
   - ขุดบล็อกใหม่:
     ```
     curl -X POST -H "Content-Type: application/json" -d '{"data":"Some block data"}' http://localhost:3001/mineBlock
     ```
   - ดูรายการเพียร์:
     ```
     curl http://localhost:3001/peers
     ```
   - เพิ่มเพียร์ใหม่:
     ```
     curl -X POST -H "Content-Type: application/json" -d '{"peer":"ws://localhost:6001"}' http://localhost:3001/addPeer
     ```

## การรันหลายโหนด

เพื่อสร้างเครือข่ายของหลายโหนด:

1. เริ่มต้นโหนดแรกด้วยการตั้งค่าเริ่มต้น:
   ```
   python blockchain.py
   ```

2. เริ่มต้นโหนดเพิ่มเติมในหน้าต่างเทอร์มินัลใหม่ โดยระบุพอร์ตและเพียร์ที่แตกต่างกัน:
   ```
   HTTP_PORT=3002 P2P_PORT=6002 PEERS=ws://localhost:6001 python blockchain.py
   ```
   ```
   HTTP_PORT=3003 P2P_PORT=6003 PEERS=ws://localhost:6001,ws://localhost:6002 python blockchain.py
   ```


## ใบอนุญาต

โปรเจกต์นี้เป็นโอเพนซอร์สและมีให้ใช้ภายใต้ [MIT License](LICENSE)

## ข้อจำกัดความรับผิดชอบ

การทำงานของบล็อกเชนนี้มีไว้เพื่อวัตถุประสงค์ทางการศึกษาเท่านั้นและไม่เหมาะสำหรับการใช้งานจริง