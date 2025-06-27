Certainly! Let's go through the complete steps from the beginning to generate a **custom .onion** address starting with **IMVICKYKUMAR** using the **mkp224o** tool, assuming you're using a Linux-based system like Ubuntu.

### Step-by-Step Commands for Beginners

1. **Install Required Dependencies**

   First, you'll need to install some development tools and libraries to build the `mkp224o` project. These include compilers and the `libsodium` library.

   Run the following commands to install dependencies:

   ```bash
   sudo apt update
   sudo apt install build-essential autoconf automake libsodium-dev git
   ```

   * `build-essential`: Installs the essential tools for compiling software (like `gcc` and `make`).
   * `autoconf` and `automake`: These are needed for generating build files.
   * `libsodium-dev`: This is the required library for cryptographic functions.
   * `git`: Used to clone the repository.

2. **Clone the Repository**

   Use `git` to clone the `mkp224o` repository:

   ```bash
   git clone https://github.com/cathugger/mkp224o.git
   ```

   This will create a directory called `mkp224o` in your current directory.

3. **Navigate to the Project Directory**

   Change to the `mkp224o` directory:

   ```bash
   cd mkp224o
   ```

4. **Run `autogen.sh` to Generate Build Files**

   Before you can compile the project, run the `autogen.sh` script to generate the necessary configuration files:

   ```bash
   chmod +x autogen.sh  # Make sure the script is executable
   ./autogen.sh
   ```

   This script will create the `configure` script, which is used to configure the build environment.

5. **Run `configure` to Set Up the Build**

   Run the `configure` script to prepare the environment for building the project:

   ```bash
   ./configure
   ```

   This will check if your system has the required libraries and tools.

6. **Build the Project with `make`**

   Once the configuration is done, you can compile the project by running:

   ```bash
   make
   ```

   This will compile the `mkp224o` tool and generate the executable.

7. **Generate the Vanity .onion Address**

   After building the tool, you can use it to generate a custom .onion address. For example, to generate a .onion address starting with `IMVICKYKUMAR`, use the following command:

   ```bash
   ./mkp224o -d onions IMVICKYKUMAR
   ```

   This command:

   * **`-d onions`**: Tells `mkp224o` to create a directory named `onions` to store the generated private key and .onion address.
   * **`IMVICKYKUMAR`**: Specifies the desired prefix for the .onion address.

8. **Wait for the Process to Complete**

   Depending on your system's power and the complexity of the prefix, it may take some time. You will see output like this while the process is running:

   ```bash
   set workdir: onions/
   sorting filters... done.
   filters:
   imvickykumar
   in total, 1 filter
   using 4 threads
   ```

   The process is working, but it may take time depending on the number of threads available and your system’s performance.

9. **Check for the Generated Address**

   Once the process is finished, you can find the private key and the generated **.onion** address in the `onions/` directory.

   Check the `onions/` folder for the generated files:

   ```bash
   ls onions/
   ```

   You should see something like:

   * `hs_ed25519_secret_key`: The private key file.
   * `hs_ed25519_public_key`: The public key.
   * `hostname`: The generated .onion address.

10. **Set Up Tor Hidden Service**

Now, to use your custom .onion address, you need to configure your Tor hidden service.

* **Open the `torrc` file** (located at `/etc/tor/torrc`):

  ```bash
  sudo nano /etc/tor/torrc
  ```

* **Add the following lines** to configure your hidden service to use the generated private key and start the service on port 80:

  ```txt
  HiddenServiceDir /var/lib/tor/hidden_service/
  HiddenServicePort 80 127.0.0.1:8080
  ```

  This configuration tells Tor to use the directory `/var/lib/tor/hidden_service/` for your hidden service.

* **Save and close the file** by pressing `CTRL + O`, then `Enter`, and `CTRL + X` to exit.

11. **Copy the Private Key**

Move the private key you generated into the hidden service directory:

```bash
sudo cp onions/hs_ed25519_secret_key /var/lib/tor/hidden_service/hs_ed25519_secret_key
```

12. **Restart the Tor Service**

Restart Tor for the changes to take effect:

```bash
sudo systemctl restart tor
```

13. **Access Your Hidden Service**

After restarting Tor, you can now access your custom .onion address using the Tor browser. The address will be saved in the `hostname` file within the `onions/` directory.

To get your .onion address, run:

```bash
cat onions/hostname
```

This will display the full **.onion** address you just generated.

### Summary of Commands:

```bash
# Install dependencies
sudo apt update
sudo apt install build-essential autoconf automake libsodium-dev git

# Clone the repository
git clone https://github.com/cathugger/mkp224o.git
cd mkp224o

# Run autogen.sh to prepare the build
chmod +x autogen.sh
./autogen.sh

# Configure the project
./configure

# Build the project
make

# Generate the vanity .onion address
./mkp224o -d onions IMVICKYKUMAR

# Check the generated address
cat onions/hostname

# Configure Tor hidden service
sudo nano /etc/tor/torrc
# Add the following lines:
# HiddenServiceDir /var/lib/tor/hidden_service/
# HiddenServicePort 80 127.0.0.1:8080

# Copy the private key to the hidden service directory
sudo cp onions/hs_ed25519_secret_key /var/lib/tor/hidden_service/hs_ed25519_secret_key

# Restart Tor
sudo systemctl restart tor
```

Now you should have your custom .onion address live and accessible via the Tor browser!

Let me know if you need further clarification or run into any issues.
