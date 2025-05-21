># `Custom Onion URL`
>
>✅ **Valid .onion characters**: `a–z` and `2–7`
>
>❌ **Invalid**: `0`, `1`, `8`, `9`, uppercase letters, symbols are not in the Base32 alphabet Tor uses.
>
>![image](https://github.com/user-attachments/assets/ac03693a-ad02-429b-b935-327f3bda581a)

## Time Comparison for 12 character

    4 cores take 7616 years
    
![image](https://github.com/user-attachments/assets/0eb2ecac-22cf-448b-98bb-e4d2e21c1958)

    40 cores take 761 years
    
![image](https://github.com/user-attachments/assets/1d41b13a-2867-4c9b-a413-f63ff198a25b)

### ✅ 1. Create a Bash Script

You can name it `generate_onion.sh`. Here’s the full content:

```bash
#!/bin/bash

# Prompt for prefix
read -p "Enter your desired .onion prefix (e.g., IMVICKYKUMAR): " PREFIX

# Step 1: Install required packages
echo "Installing dependencies..."
sudo apt update
sudo apt install -y build-essential autoconf automake libsodium-dev git

# Step 2: Clone the mkp224o repo if it doesn't exist
if [ ! -d "mkp224o" ]; then
    echo "Cloning mkp224o repository..."
    git clone https://github.com/cathugger/mkp224o.git
fi

cd mkp224o || exit 1

# Step 3: Run autogen.sh
echo "Preparing build environment..."
chmod +x autogen.sh
./autogen.sh

# Step 4: Configure the build
./configure

# Step 5: Compile mkp224o
make

# Step 6: Run mkp224o with the provided prefix
echo "Generating .onion address with prefix: $PREFIX"
./mkp224o -d onions "$PREFIX"

# Step 7: Output generated address
echo "Your custom .onion address is:"
cat onions/hostname

# Optional: Prompt to open hostname in nano
read -p "Do you want to view/edit the hostname in nano? (y/n): " EDIT
if [ "$EDIT" == "y" ]; then
    nano onions/hostname
fi
```

---

### ✅ 2. Save and Make It Executable

Save the script:

```bash
nano generate_onion.sh
# Paste the above code and save with CTRL + O, Enter, then CTRL + X
```

Make it executable:

```bash
chmod +x generate_onion.sh
```

---

### ✅ 3. Run the Script

```bash
./generate_onion.sh
```

It will guide you through the process, ask for your desired prefix, install dependencies if needed, and generate the vanity `.onion` address.

Once you've successfully generated a custom `.onion` address using `mkp224o`, the next step is to **configure and run a Tor hidden service** on your system to **serve content (e.g., a website) under that `.onion` address**.

Here’s a **complete step-by-step guide** to help you run your server:

---

## 🌐 Step-by-Step: Host Your Custom `.onion` Hidden Service

### ✅ 1. **Check What Was Generated**

After `mkp224o` finishes, you’ll find:

```
onions/
└── <your-onion-folder>/
    ├── hostname                 # Your .onion address
    ├── hs_ed25519_secret_key   # Private key
    └── hs_ed25519_public_key   # Public key
```

### 📝 Example:

```bash
ls onions/
cat onions/hostname  # to see the address
```

---

### ✅ 2. **Install and Enable Tor**

```bash
sudo apt update
sudo apt install tor -y
```

Start and enable Tor:

```bash
sudo systemctl enable tor
sudo systemctl start tor
```

---

### ✅ 3. **Configure Tor Hidden Service**

Edit the Tor config file:

```bash
sudo nano /etc/tor/torrc
```

Add the following at the bottom:

```ini
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:8080
```

**Important**: This means:

* Your web service should run on `localhost:8080`
* Tor will expose it as your `.onion` domain on port 80

---

### ✅ 4. **Replace the Default Hidden Service Keys**

```bash
sudo systemctl stop tor
sudo rm -rf /var/lib/tor/hidden_service
sudo mkdir -p /var/lib/tor/hidden_service
sudo cp onions/<your-onion-folder>/* /var/lib/tor/hidden_service/
sudo chown -R debian-tor:debian-tor /var/lib/tor/hidden_service
sudo chmod 700 /var/lib/tor/hidden_service
```

> Replace `<your-onion-folder>` with the actual folder name (the full `.onion` address)

---

### ✅ 5. **Start Tor Again**

```bash
sudo systemctl start tor
```

Check if it's running:

```bash
sudo systemctl status tor
```

---

### ✅ 6. **Start Your Web Server on Port 8080**

Here’s a simple way using Python:

```bash
cd /var/www/html  # or any directory with your content
python3 -m http.server 8080
```

Or, if using Flask/Django/Node.js etc., make sure your app runs on:

```bash
http://127.0.0.1:8080
```

---

### ✅ 7. **Access Your Hidden Service**

* Open **Tor Browser**
* Visit your `.onion` address (from `hostname` file)

It should load your website!

---

## 🧪 Example Summary Commands

```bash
sudo apt install tor -y
sudo nano /etc/tor/torrc
# Add HiddenService config...

sudo systemctl stop tor
sudo cp onions/<onion-folder>/* /var/lib/tor/hidden_service/
sudo chown -R debian-tor:debian-tor /var/lib/tor/hidden_service
sudo systemctl start tor

# Start your app
python3 -m http.server 8080
```

---

### ✅ **Download Tor Browser for Linux (64-bit)**

#### **Option 1: Using your web browser**

1. Go to the official Tor Project website:
   👉 [https://www.torproject.org/download/](https://www.torproject.org/download/)

2. Click on the **Linux** download button.

   * It will download a file named something like:
     `tor-browser-linux-x86_64-14.5.1.tar.xz`

3. Save it to your desired directory — for example, `~/Documents/TorService`.

---

#### **Option 2: Using the command line with `wget`**

If you prefer downloading from the terminal, use this:

```bash
cd ~/Documents/TorService
wget https://www.torproject.org/dist/torbrowser/14.5.1/tor-browser-linux-x86_64-14.5.1.tar.xz
```

---

### 📝 **Install Tor**

1. **Extract**:

   ```bash
   tar -xf tor-browser-linux-x86_64-14.5.1.tar.xz
   ```

2. **Navigate**:

   ```bash
   cd tor-browser_en-US
   ```

3. **Launch**:

   ```bash
   ./start-tor-browser.desktop
   ```

   If needed:

   ```bash
   chmod +x start-tor-browser.desktop
   ./start-tor-browser.desktop
   ```

---

Here’s a dynamic **reference table** for estimating the time to generate a Tor v3 **vanity `.onion` address** using [`mkp224o`](https://github.com/cathugger/mkp224o), based on:

* ✅ **Machine type** (Laptop / Server / Cloud)
* ✅ **CPU cores (threads)** used
* ✅ **Prefix length** (number of characters you want the `.onion` to start with)
* 🔁 **Estimated average time to generate**

---

### 📊 Vanity `.onion` Address Generation Time Estimator Table

| Machine Type                | Threads | Prefix Length | Est. Time       | Notes                             |
| --------------------------- | ------- | ------------- | --------------- | --------------------------------- |
| **Laptop (i7-6500U)**       | 4       | 6 chars       | \~10–20 minutes | Lightweight usage, older gen      |
|                             | 4       | 7 chars       | \~6–12 hours    | Usable, best kept overnight       |
|                             | 4       | 8 chars       | \~2–3 days      | Start getting impractical         |
|                             | 4       | 10 chars      | \~3–4 weeks     | ⚠ Very long                       |
|                             | 4       | 12 chars      | \~6+ months     | ❌ Not practical                   |
| **Desktop (i7-9700K)**      | 8       | 6 chars       | \~3–5 minutes   | Modern desktop, fast base clock   |
|                             | 8       | 7 chars       | \~3–6 hours     | Good balance                      |
|                             | 8       | 8 chars       | \~1 day         | Long but doable                   |
| **Server (Xeon Gold 6138)** | 40      | 6 chars       | \~1 minute      | Very fast                         |
|                             | 40      | 7 chars       | \~10–30 minutes | Ideal for `imvicky`               |
|                             | 40      | 8 chars       | \~1–2 hours     | Still very reasonable             |
|                             | 40      | 10 chars      | \~4–7 days      | Acceptable for rare branding      |
|                             | 40      | 12 chars      | \~30–60 days    | ⚠ Extremely slow, not recommended |
| **Cloud VM (AVX2, 32vCPU)** | 32      | 6 chars       | \~1 minute      | With AVX2/AVX512 (e.g., AWS C6i)  |
|                             | 32      | 7 chars       | \~5–10 minutes  | Lightning fast                    |
|                             | 32      | 8 chars       | \~30–60 minutes | Great for production vanity names |

---

### 🧠 Key Notes

* ⏱️ **Time grows exponentially**: Each extra character multiplies the search time by **\~32×**.
* 🧮 **Base32 math**: Each character = 5 bits. Prefix of N chars → `1 in 32^N` chance.
* ⚙️ **AVX2/AVX512** support massively improves performance.
* 🔁 **Actual time is probabilistic** — even with 40 threads, it can vary.

---

## Run background process

Screen Usage for Running Long Background Processes (e.g. mkp224o)

This guide explains how to use `screen` to run long-running processes in the background safely.

---

## 📦 Start a New Screen Session

```bash
screen -S <session_name>
````

**Example:**

```bash
screen -S mkp224o-clean
```

Once inside the screen, run your command:

```bash
./mkp224o -d onions IMVICKYKUMAR
```

---

## 🔌 Detach from a Session (Keep It Running in Background)

Press:

```
Ctrl + A, then D
```

This detaches the session. The process keeps running in the background even if you close the terminal.

---

## 🔁 Reconnect to a Session

### If You Know the Name:

```bash
screen -r <session_name>
```

**Example:**

```bash
screen -r mkp224o-clean
```

### If There Are Multiple Sessions:

```bash
screen -ls
```

Then attach with the session ID:

```bash
screen -r <session_id>
```

---

## ❌ Quit a Screen Session (Stop the Process)

### By Session Name:

```bash
screen -X -S <session_name> quit
```

**Example:**

```bash
screen -X -S mkp224o-clean quit
```

### By Session ID:

```bash
screen -X -S <session_id> quit
```

**Example:**

```bash
screen -X -S 123456.quit
```

---

## 🧼 List All Screen Sessions

```bash
screen -ls
```

Use this to see which sessions are active or detached.

---

## 📎 Tip

Use unique session names to avoid confusion when running multiple background tasks.
