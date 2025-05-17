# CustomOnionURL

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
