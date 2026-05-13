<!-- Source: https://docs.expo.dev/llms-full.txt (llms-full.txt) -->
<!-- Downloaded: 2026-03-21 -->

# Expo Documentation

Expo is an open-source React Native framework for apps that run natively on Android, iOS, and the web. Expo brings together the best of mobile and the web and enables many important features for building and scaling an app such as live updates, instantly sharing your app, and web support. The company behind Expo also offers Expo Application Services (EAS), which are deeply integrated cloud services for Expo and React Native apps.

---
modificationDate: March 10, 2026
title: Create a project
description: Learn how to create a new Expo project.
---

# Create a project

Learn how to create a new Expo project.

Expo is a React Native framework that makes developing Android and iOS apps easier. Our framework provides file-based routing, a standard library of native modules, and much more. Expo is open source with an active community on [GitHub](https://github.com/expo/expo) and [Discord](https://chat.expo.dev).

We also make [Expo Application Services (EAS)](https://expo.dev/eas), a set of services that complement the Expo framework in each step of the development process.

## System requirements

-   [Node.js (LTS)](https://nodejs.org/en/).
-   macOS, Windows (Powershell and [WSL 2](https://expo.fyi/wsl)), and Linux are supported.

We recommend starting with the default project created by `create-expo-app`. The default project includes example code to help you get started.

To create a new project, run the following command:

```sh
npx create-expo-app@latest --template default@sdk-55
```

> **Note:** During the SDK 55 transition period, `create-expo-app@latest` without the `--template` flag creates an SDK 54 project. If you plan to use Expo Go on a physical device, use an SDK 54 project. Otherwise, use `--template default@sdk-55` to create an SDK 55 project. You can also choose a different template by adding the [`--template` option](/more/create-expo#--template).

## Next step

You have a project. Now it's time to set up your development environment so that you can start developing.

---

---
modificationDate: January 29, 2026
title: Set up your environment
description: Learn how to set up your development environment to start building with Expo.
---

# Set up your environment

Learn how to set up your development environment to start building with Expo.

Let's set up a local development environment for running your project on Android and iOS.

## Where would you like to develop?

We recommend using a real device to develop, since you'll get to see exactly what your users will see.

## How would you like to develop?

Expo Go is a playground for students and learners to try Expo quickly. A development build is a build of your own app that includes Expo's developer tools.

## Android device with Expo Go

### Set up an Android device with Expo Go

Scan the QR code to download the app from the Google Play Store, or visit the Expo Go page on the [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent&referrer=docs).

  Download link: [https://play.google.com/store/apps/details?id=host.exp.exponent&referrer=docs](https://play.google.com/store/apps/details?id=host.exp.exponent&referrer=docs)

---

## Android device with a development build (EAS)

### Set up an Android device with a development build

#### Install EAS CLI

To build your app, you will need to install EAS CLI. You can do this by running the following command in your terminal:

```sh
npm install -g eas-cli
```

#### Create an Expo account and login

To build your app, you will need to create an Expo account and login to the EAS CLI.

1. [Sign up](https://expo.dev/signup) for an Expo account.
2. Run the following command in your terminal to log in to the EAS CLI:

```sh
eas login
```

#### Configure your project

Run the following command to create an EAS config in your project:

```sh
eas build:configure
```

#### Create a build

Run the following command to create a development build:

```sh
eas build --platform android --profile development
```

#### Install the development build on your device

After the build is complete, scan the QR code in your terminal or open the link on your device. Tap **Install** to download the build on your device, then tap **Open** to install it.

---

## Android device with a development build (local)

### Set up an Android device with a development build

### Install Watchman and JDK

##### macOS

##### Prerequisites

Use a package manager such as [Homebrew](https://brew.sh/) to install the following dependency.

##### Install dependencies

[Install Watchman](https://facebook.github.io/watchman/docs/install#macos) using a tool such as Homebrew:

```sh
brew install watchman
```

Install OpenJDK distribution called Azul Zulu using Homebrew. This distribution offers JDKs for both Apple Silicon and Intel Macs.

Run the following commands in a terminal:

```sh
brew install --cask zulu@17
```

After you install the JDK, add the `JAVA_HOME` environment variable in **~/.bash_profile** (or **~/.zshrc** if you use Zsh):

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
```

##### Windows

##### Prerequisites

Use a package manager such as [Chocolatey](https://chocolatey.org/) to install the following dependencies.

##### Install dependencies

Install [Java SE Development Kit (JDK)](https://openjdk.org/):

```sh
choco install -y microsoft-openjdk17
```

##### Linux

##### Install dependencies

Follow [instructions from the Watchman documentation](https://facebook.github.io/watchman/docs/install#linux) to compile and install it from the source.

Install [Java SE Development Kit (JDK)](https://openjdk.org/):

You can download and install [OpenJDK@17](http://openjdk.java.net/) from [AdoptOpenJDK](https://adoptopenjdk.net/) or your system packager.

### Set up Android Studio

##### macOS

Download and install [Android Studio](https://developer.android.com/studio).

Open the **Android Studio** app, you will see the **SDK Components setup** screen. Click **Next** to continue to install the Android SDK and Android SDK Platform. Click **Next** again to verify the settings and install.

By default, Android Studio will install the latest version of the Android SDK. However, Android 15 (`VanillaIceCream`) SDK is required to compile a React Native app.

Open Android Studio, go to **Settings** > **Languages & Frameworks** > **Android SDK**. From the **SDK Platforms** tab, and under **Android 15 (`VanillaIceCream`)**, select **Android SDK Platform 35** and **Sources for Android 35**.

Then, click on the **SDK Tools** tab and make sure you have at least one version of the **Android SDK Build-Tools** and **Android Emulator** installed.

Copy or remember the path listed in the box that says **Android SDK Location**.

Add the following lines to your **/.zprofile** or **~/.zshrc** (if you are using bash, then **~/.bash_profile** or **~/.bashrc**) config file:

```sh
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

Reload the path environment variables in your current shell:

```sh
source $HOME/.zshrc
source $HOME/.bashrc
```

Finally, make sure that you can run `adb` from your terminal.

**Troubleshooting: Android Studio not recognizing JDK**

If Android Studio doesn't recognize your homebrew installed JDK, you can create a Gradle configuration file to explicitly set the Java path:

1.  Create a Gradle properties file in your home directory:


```sh
touch ~/.gradle/gradle.properties
```

2.  Add the following line to the **gradle.properties** file, replacing the path with your actual Java installation path:

    ```bash gradle.properties
    java.home=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
    ```

3.  If you have an existing `.gradle` folder in your project directory, delete it and reopen your project in Android Studio:


```sh
rm -rf .gradle
```

This should resolve issues with Android Studio not detecting your JDK installation.

##### Windows

Download [Android Studio](https://developer.android.com/studio).

Open **Android Studio Setup**. Under **Select components to install**, select Android Studio and Android Virtual Device. Then, click **Next**.

In the Android Studio Setup Wizard, under **Install Type**, select **Standard** and click **Next**.

The Android Studio Setup Wizard will ask you to verify the settings, such as the version of Android SDK, platform-tools, and so on. Click **Next** after you have verified.

In the next window, accept licenses for all available components.

By default, Android Studio will install the latest version of the Android SDK. However, Android 15 (`VanillaIceCream`) SDK is required to compile a React Native app.

Open Android Studio, go to **Settings** > **Languages & Frameworks** > **Android SDK**. From the **SDK Platforms** tab, and under **Android 15 (`VanillaIceCream`)**, select **Android SDK Platform 35** and **Sources for Android 35**.

Then, click on the **SDK Tools** tab and make sure you have at least one version of the **Android SDK Build-Tools** and **Android Emulator** installed.

After the tools installation is complete, configure the `ANDROID_HOME` environment variable. Go to **Windows Control Panel** > **User Accounts** > **User Accounts** (again) > **Change my environment variables** and click **New** to create a new `ANDROID_HOME` user variable. The value of this variable will point to the path to your Android SDK:

**How to find installed SDK location?**

By default, the Android SDK is installed at the following location:

```bash
%LOCALAPPDATA%\Android\Sdk
```

To find the location of the SDK in Android Studio manually, go to **Settings** > **Languages & Frameworks** > **Android SDK**. See the location next to **Android SDK Location**.

To verify that the new environment variable is loaded, open **PowerShell**, and copy and paste the following command:

```sh
Get-ChildItem -Path Env:
```

The command will output all user environment variables. In this list, see if `ANDROID_HOME` has been added.

To add platform-tools to the Path, go to **Windows Control Panel** > **User Accounts** > **User Accounts** (again) > **Change my environment variables** > **Path** > **Edit** > **New** and add the path to the platform-tools to the list as shown below:

**How to find installed platform-tools location**

By default, the platform-tools are installed at the following location:

```bash
%LOCALAPPDATA%\Android\Sdk\platform-tools
```

Finally, make sure that you can run `adb` from the PowerShell. For example, run the `adb --version` to see which version of the `adb` your system is running.

### Running your app on an Android device

#### Install expo-dev-client

Run the following command in your project's root directory:

```sh
npx expo install expo-dev-client
```

#### Enable debugging over USB

Most Android devices can only install and run apps downloaded from Google Play, by default. You will need to enable USB Debugging on your device to install your app during development.

To enable USB debugging on your device, you will first need to enable the "Developer options" menu by going to **Settings** > **About phone** > **Software information** and then tapping the `Build number` row at the bottom seven times. You can then go back to **Settings** > **Developer options** to enable "USB debugging".

#### Plug in your device via USB

Plug in your Android device via USB to your computer.

Check that your device is properly connecting to ADB, the Android Debug Bridge, by running `adb devices` in your terminal. You should see your device listed with `device` listed next to it. For example:

```sh
adb devices
List of devices attached
8AHX0T32K	device
```

#### Run your app

Run the following from your terminal:

```sh
npx expo run:android
```

> This command runs a development server after building your app. You can skip running `npx expo start` on the next page.

---

## Android Emulator with Expo Go

### Set up an Android Emulator with Expo Go

### Set up Android Studio

##### macOS

Download and install [Android Studio](https://developer.android.com/studio).

Open the **Android Studio** app, you will see the **SDK Components setup** screen. Click **Next** to continue to install the Android SDK and Android SDK Platform. Click **Next** again to verify the settings and install.

By default, Android Studio will install the latest version of the Android SDK. However, Android 15 (`VanillaIceCream`) SDK is required to compile a React Native app.

Open Android Studio, go to **Settings** > **Languages & Frameworks** > **Android SDK**. From the **SDK Platforms** tab, and under **Android 15 (`VanillaIceCream`)**, select **Android SDK Platform 35** and **Sources for Android 35**.

Then, click on the **SDK Tools** tab and make sure you have at least one version of the **Android SDK Build-Tools** and **Android Emulator** installed.

Copy or remember the path listed in the box that says **Android SDK Location**.

Add the following lines to your **/.zprofile** or **~/.zshrc** (if you are using bash, then **~/.bash_profile** or **~/.bashrc**) config file:

```sh
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

Reload the path environment variables in your current shell:

```sh
source $HOME/.zshrc
source $HOME/.bashrc
```

Finally, make sure that you can run `adb` from your terminal.

**Troubleshooting: Android Studio not recognizing JDK**

If Android Studio doesn't recognize your homebrew installed JDK, you can create a Gradle configuration file to explicitly set the Java path:

1.  Create a Gradle properties file in your home directory:


```sh
touch ~/.gradle/gradle.properties
```

2.  Add the following line to the **gradle.properties** file, replacing the path with your actual Java installation path:

    ```bash gradle.properties
    java.home=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
    ```

3.  If you have an existing `.gradle` folder in your project directory, delete it and reopen your project in Android Studio:


```sh
rm -rf .gradle
```

This should resolve issues with Android Studio not detecting your JDK installation.

##### Windows

Download [Android Studio](https://developer.android.com/studio).

Open **Android Studio Setup**. Under **Select components to install**, select Android Studio and Android Virtual Device. Then, click **Next**.

In the Android Studio Setup Wizard, under **Install Type**, select **Standard** and click **Next**.

The Android Studio Setup Wizard will ask you to verify the settings, such as the version of Android SDK, platform-tools, and so on. Click **Next** after you have verified.

In the next window, accept licenses for all available components.

By default, Android Studio will install the latest version of the Android SDK. However, Android 15 (`VanillaIceCream`) SDK is required to compile a React Native app.

Open Android Studio, go to **Settings** > **Languages & Frameworks** > **Android SDK**. From the **SDK Platforms** tab, and under **Android 15 (`VanillaIceCream`)**, select **Android SDK Platform 35** and **Sources for Android 35**.

Then, click on the **SDK Tools** tab and make sure you have at least one version of the **Android SDK Build-Tools** and **Android Emulator** installed.

After the tools installation is complete, configure the `ANDROID_HOME` environment variable. Go to **Windows Control Panel** > **User Accounts** > **User Accounts** (again) > **Change my environment variables** and click **New** to create a new `ANDROID_HOME` user variable. The value of this variable will point to the path to your Android SDK:

**How to find installed SDK location?**

By default, the Android SDK is installed at the following location:

```bash
%LOCALAPPDATA%\Android\Sdk
```

To find the location of the SDK in Android Studio manually, go to **Settings** > **Languages & Frameworks** > **Android SDK**. See the location next to **Android SDK Location**.

To verify that the new environment variable is loaded, open **PowerShell**, and copy and paste the following command:

```sh
Get-ChildItem -Path Env:
```

The command will output all user environment variables. In this list, see if `ANDROID_HOME` has been added.

To add platform-tools to the Path, go to **Windows Control Panel** > **User Accounts** > **User Accounts** (again) > **Change my environment variables** > **Path** > **Edit** > **New** and add the path to the platform-tools to the list as shown below:

**How to find installed platform-tools location**

By default, the platform-tools are installed at the following location:

```bash
%LOCALAPPDATA%\Android\Sdk\platform-tools
```

Finally, make sure that you can run `adb` from the PowerShell. For example, run the `adb --version` to see which version of the `adb` your system is running.

### Set up an emulator

On the Android Studio main screen, click **More Actions**, then **Virtual Device Manager** in the dropdown.

Click the **Create device** button.

Under **Add device**, choose the type of hardware you'd like to emulate. We recommend testing against a variety of devices, but if you're unsure where to start, the newest device in the Pixel line could be a good choice.

Select an OS version to load on the emulator (probably one of the system images), and download the image (if required).

Change any other settings you'd like, and press **Finish** to create the emulator. You can now run this emulator anytime by pressing the Play button in the AVD Manager window.

### Install Expo Go

When you start a development server with `npx expo start` on the [start developing](/get-started/start-developing) page, press <kbd>a</kbd> to open the Android Emulator. Expo CLI will install Expo Go automatically.

---

## Android Emulator with a development build (EAS)

### Set up an Android Emulator with a development build

### Set up Android Studio

##### macOS

Download and install [Android Studio](https://developer.android.com/studio).

Open the **Android Studio** app, you will see the **SDK Components setup** screen. Click **Next** to continue to install the Android SDK and Android SDK Platform. Click **Next** again to verify the settings and install.

By default, Android Studio will install the latest version of the Android SDK. However, Android 15 (`VanillaIceCream`) SDK is required to compile a React Native app.

Open Android Studio, go to **Settings** > **Languages & Frameworks** > **Android SDK**. From the **SDK Platforms** tab, and under **Android 15 (`VanillaIceCream`)**, select **Android SDK Platform 35** and **Sources for Android 35**.

Then, click on the **SDK Tools** tab and make sure you have at least one version of the **Android SDK Build-Tools** and **Android Emulator** installed.

Copy or remember the path listed in the box that says **Android SDK Location**.

Add the following lines to your **/.zprofile** or **~/.zshrc** (if you are using bash, then **~/.bash_profile** or **~/.bashrc**) config file:

```sh
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

Reload the path environment variables in your current shell:

```sh
source $HOME/.zshrc
source $HOME/.bashrc
```

Finally, make sure that you can run `adb` from your terminal.

**Troubleshooting: Android Studio not recognizing JDK**

If Android Studio doesn't recognize your homebrew installed JDK, you can create a Gradle configuration file to explicitly set the Java path:

1.  Create a Gradle properties file in your home directory:


```sh
touch ~/.gradle/gradle.properties
```

2.  Add the following line to the **gradle.properties** file, replacing the path with your actual Java installation path:

    ```bash gradle.properties
    java.home=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
    ```

3.  If you have an existing `.gradle` folder in your project directory, delete it and reopen your project in Android Studio:


```sh
rm -rf .gradle
```

This should resolve issues with Android Studio not detecting your JDK installation.

##### Windows

Download [Android Studio](https://developer.android.com/studio).

Open **Android Studio Setup**. Under **Select components to install**, select Android Studio and Android Virtual Device. Then, click **Next**.

In the Android Studio Setup Wizard, under **Install Type**, select **Standard** and click **Next**.

The Android Studio Setup Wizard will ask you to verify the settings, such as the version of Android SDK, platform-tools, and so on. Click **Next** after you have verified.

In the next window, accept licenses for all available components.

By default, Android Studio will install the latest version of the Android SDK. However, Android 15 (`VanillaIceCream`) SDK is required to compile a React Native app.

Open Android Studio, go to **Settings** > **Languages & Frameworks** > **Android SDK**. From the **SDK Platforms** tab, and under **Android 15 (`VanillaIceCream`)**, select **Android SDK Platform 35** and **Sources for Android 35**.

Then, click on the **SDK Tools** tab and make sure you have at least one version of the **Android SDK Build-Tools** and **Android Emulator** installed.

After the tools installation is complete, configure the `ANDROID_HOME` environment variable. Go to **Windows Control Panel** > **User Accounts** > **User Accounts** (again) > **Change my environment variables** and click **New** to create a new `ANDROID_HOME` user variable. The value of this variable will point to the path to your Android SDK:

**How to find installed SDK location?**

By default, the Android SDK is installed at the following location:

```bash
%LOCALAPPDATA%\Android\Sdk
```

To find the location of the SDK in Android Studio manually, go to **Settings** > **Languages & Frameworks** > **Android SDK**. See the location next to **Android SDK Location**.

To verify that the new environment variable is loaded, open **PowerShell**, and copy and paste the following command:

```sh
Get-ChildItem -Path Env:
```

The command will output all user environment variables. In this list, see if `ANDROID_HOME` has been added.

To add platform-tools to the Path, go to **Windows Control Panel** > **User Accounts** > **User Accounts** (again) > **Change my environment variables** > **Path** > **Edit** > **New** and add the path to the platform-tools to the list as shown below:

**How to find installed platform-tools location**

By default, the platform-tools are installed at the following location:

```bash
%LOCALAPPDATA%\Android\Sdk\platform-tools
```

Finally, make sure that you can run `adb` from the PowerShell. For example, run the `adb --version` to see which version of the `adb` your system is running.

### Set up an emulator

On the Android Studio main screen, click **More Actions**, then **Virtual Device Manager** in the dropdown.

Click the **Create device** button.

Under **Add device**, choose the type of hardware you'd like to emulate. We recommend testing against a variety of devices, but if you're unsure where to start, the newest device in the Pixel line could be a good choice.

Select an OS version to load on the emulator (probably one of the system images), and download the image (if required).

Change any other settings you'd like, and press **Finish** to create the emulator. You can now run this emulator anytime by pressing the Play button in the AVD Manager window.

### Create a development build

#### Install EAS CLI

To build your app, you will need to install EAS CLI. You can do this by running the following command in your terminal:

```sh
npm install -g eas-cli
```

#### Create an Expo account and login

To build your app, you will need to create an Expo account and login to the EAS CLI.

1. [Sign up](https://expo.dev/signup) for an Expo account.
2. Run the following command in your terminal to log in to the EAS CLI:

```sh
eas login
```

#### Configure your project

Run the following command to create an EAS config in your project:

```sh
eas build:configure
```

#### Create a build

Run the following command to create a development build:

```sh
eas build --platform android --profile development
```

#### Install the development build on your emulator

After the build is complete, the CLI will prompt you to automatically download and install it on the Android Emulator. When prompted, press <kbd>Y</kbd> to directly install it on the emulator.

If you miss this prompt, you can download the build from the link provided in the terminal and drag and drop it onto the Android Emulator to install it.

---

## Android Emulator with a development build (local)

### Set up an Android Emulator with a development build

### Install Watchman and JDK

##### macOS

##### Prerequisites

Use a package manager such as [Homebrew](https://brew.sh/) to install the following dependency.

##### Install dependencies

[Install Watchman](https://facebook.github.io/watchman/docs/install#macos) using a tool such as Homebrew:

```sh
brew install watchman
```

Install OpenJDK distribution called Azul Zulu using Homebrew. This distribution offers JDKs for both Apple Silicon and Intel Macs.

Run the following commands in a terminal:

```sh
brew install --cask zulu@17
```

After you install the JDK, add the `JAVA_HOME` environment variable in **~/.bash_profile** (or **~/.zshrc** if you use Zsh):

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
```

##### Windows

##### Prerequisites

Use a package manager such as [Chocolatey](https://chocolatey.org/) to install the following dependencies.

##### Install dependencies

Install [Java SE Development Kit (JDK)](https://openjdk.org/):

```sh
choco install -y microsoft-openjdk17
```

##### Linux

##### Install dependencies

Follow [instructions from the Watchman documentation](https://facebook.github.io/watchman/docs/install#linux) to compile and install it from the source.

Install [Java SE Development Kit (JDK)](https://openjdk.org/):

You can download and install [OpenJDK@17](http://openjdk.java.net/) from [AdoptOpenJDK](https://adoptopenjdk.net/) or your system packager.

### Set up Android Studio

##### macOS

Download and install [Android Studio](https://developer.android.com/studio).

Open the **Android Studio** app, you will see the **SDK Components setup** screen. Click **Next** to continue to install the Android SDK and Android SDK Platform. Click **Next** again to verify the settings and install.

By default, Android Studio will install the latest version of the Android SDK. However, Android 15 (`VanillaIceCream`) SDK is required to compile a React Native app.

Open Android Studio, go to **Settings** > **Languages & Frameworks** > **Android SDK**. From the **SDK Platforms** tab, and under **Android 15 (`VanillaIceCream`)**, select **Android SDK Platform 35** and **Sources for Android 35**.

Then, click on the **SDK Tools** tab and make sure you have at least one version of the **Android SDK Build-Tools** and **Android Emulator** installed.

Copy or remember the path listed in the box that says **Android SDK Location**.

Add the following lines to your **/.zprofile** or **~/.zshrc** (if you are using bash, then **~/.bash_profile** or **~/.bashrc**) config file:

```sh
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

Reload the path environment variables in your current shell:

```sh
source $HOME/.zshrc
source $HOME/.bashrc
```

Finally, make sure that you can run `adb` from your terminal.

**Troubleshooting: Android Studio not recognizing JDK**

If Android Studio doesn't recognize your homebrew installed JDK, you can create a Gradle configuration file to explicitly set the Java path:

1.  Create a Gradle properties file in your home directory:


```sh
touch ~/.gradle/gradle.properties
```

2.  Add the following line to the **gradle.properties** file, replacing the path with your actual Java installation path:

    ```bash gradle.properties
    java.home=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
    ```

3.  If you have an existing `.gradle` folder in your project directory, delete it and reopen your project in Android Studio:


```sh
rm -rf .gradle
```

This should resolve issues with Android Studio not detecting your JDK installation.

##### Windows

Download [Android Studio](https://developer.android.com/studio).

Open **Android Studio Setup**. Under **Select components to install**, select Android Studio and Android Virtual Device. Then, click **Next**.

In the Android Studio Setup Wizard, under **Install Type**, select **Standard** and click **Next**.

The Android Studio Setup Wizard will ask you to verify the settings, such as the version of Android SDK, platform-tools, and so on. Click **Next** after you have verified.

In the next window, accept licenses for all available components.

By default, Android Studio will install the latest version of the Android SDK. However, Android 15 (`VanillaIceCream`) SDK is required to compile a React Native app.

Open Android Studio, go to **Settings** > **Languages & Frameworks** > **Android SDK**. From the **SDK Platforms** tab, and under **Android 15 (`VanillaIceCream`)**, select **Android SDK Platform 35** and **Sources for Android 35**.

Then, click on the **SDK Tools** tab and make sure you have at least one version of the **Android SDK Build-Tools** and **Android Emulator** installed.

After the tools installation is complete, configure the `ANDROID_HOME` environment variable. Go to **Windows Control Panel** > **User Accounts** > **User Accounts** (again) > **Change my environment variables** and click **New** to create a new `ANDROID_HOME` user variable. The value of this variable will point to the path to your Android SDK:

**How to find installed SDK location?**

By default, the Android SDK is installed at the following location:

```bash
%LOCALAPPDATA%\Android\Sdk
```

To find the location of the SDK in Android Studio manually, go to **Settings** > **Languages & Frameworks** > **Android SDK**. See the location next to **Android SDK Location**.

To verify that the new environment variable is loaded, open **PowerShell**, and copy and paste the following command:

```sh
Get-ChildItem -Path Env:
```

The command will output all user environment variables. In this list, see if `ANDROID_HOME` has been added.

To add platform-tools to the Path, go to **Windows Control Panel** > **User Accounts** > **User Accounts** (again) > **Change my environment variables** > **Path** > **Edit** > **New** and add the path to the platform-tools to the list as shown below:

**How to find installed platform-tools location**

By default, the platform-tools are installed at the following location:

```bash
%LOCALAPPDATA%\Android\Sdk\platform-tools
```

Finally, make sure that you can run `adb` from the PowerShell. For example, run the `adb --version` to see which version of the `adb` your system is running.

### Set up an emulator

On the Android Studio main screen, click **More Actions**, then **Virtual Device Manager** in the dropdown.

Click the **Create device** button.

Under **Add device**, choose the type of hardware you'd like to emulate. We recommend testing against a variety of devices, but if you're unsure where to start, the newest device in the Pixel line could be a good choice.

Select an OS version to load on the emulator (probably one of the system images), and download the image (if required).

Change any other settings you'd like, and press **Finish** to create the emulator. You can now run this emulator anytime by pressing the Play button in the AVD Manager window.

### Running your app on an Android Emulator

#### Install expo-dev-client

Run the following command in your project's root directory:

```sh
npx expo install expo-dev-client
```

Run the following from your terminal:

```sh
npx expo run:android
```

> This command runs a development server after building your app. You can skip running `npx expo start` on the next page.

---

## iOS device with Expo Go

### Set up an iOS device with Expo Go

#### Enroll in the Apple Developer Program

To install Expo Go on your iOS device, you will need an active subscription to the Apple Developer Program. Sign up for the [Apple Developer Program here](https://developer.apple.com/programs/).

#### Build Expo Go for iOS

Run the following command to build Expo Go:

```sh
npx eas-cli@latest go
```

#### Install TestFlight

Download and install the [TestFlight app](https://apps.apple.com/us/app/testflight/id899247664). You can also scan the QR code below on your iOS device:

Download link: [https://apps.apple.com/us/app/testflight/id899247664](https://apps.apple.com/us/app/testflight/id899247664)

#### Add yourself as a tester

1. Go to [App Store Connect](https://appstoreconnect.apple.com).
2. Select the Expo Go app.
3. Navigate to the "TestFlight" tab.
4. Add your Apple ID email as an internal tester.

Once you do, you should receive an email invitation to join the TestFlight beta. When you accept the invitation, you can install Expo Go on your iOS device.

---

## iOS device with a development build (EAS)

### Set up an iOS device with a development build

#### Enroll in the Apple Developer Program

To install a development build on your iOS device, you will need an active subscription to the Apple Developer Program. Sign up for the [Apple Developer Program here](https://developer.apple.com/programs/).

#### Install EAS CLI

To build your app, you will need to install EAS CLI. You can do this by running the following command in your terminal:

```sh
npm install -g eas-cli
```

#### Create an Expo account and login

Next, you will need to create an Expo account and login to the EAS CLI.

1. [Sign up](https://expo.dev/signup) for an Expo account.
2. Run the following command in your terminal to log in to the EAS CLI:

```sh
eas login
```

#### Configure your project

Run the following command to create an EAS config in your project:

```sh
eas build:configure
```

#### Create an ad hoc provisioning profile

To install a development build on your iOS device, you will need to create an ad hoc provisioning profile. Create one by running the following command in your terminal:

```sh
eas device:create
```

#### Create a development build

Run the following command to create a development build:

```sh
eas build --platform ios --profile development
```

#### Install the development build on your device

After the build is complete, scan the QR code in your terminal and tap **Open with iTunes** when it appears inside the Camera app. Alternatively, open the link displayed in the terminal on your device.

After confirming the installation, the app will appear in your device's app library.

#### Turn on developer mode

1. Open **Settings** > **Privacy & Security**, scroll down to the **Developer Mode** list item and navigate into it.
2. Tap the switch to enable **Developer Mode**. After you do so, Settings presents an alert to warn you that Developer Mode reduces your device's security. To continue enabling **Developer Mode**, tap the alert's **Restart** button.
3. After the device restarts and you unlock it, the device shows an alert confirming that you want to enable Developer Mode. Tap **Turn On**, and enter your device passcode when prompted.

> Alternatively, if you have Xcode installed on your Mac, you can use it to [enable iOS developer mode](/guides/ios-developer-mode/#connect-an-ios-device-with-a-mac).

---

## iOS device with a development build (local)

### Set up an iOS device with a development build

### Set up Xcode and Watchman

#### Install Xcode

Open up the Mac App Store, search for [Xcode](https://apps.apple.com/us/app/xcode/id497799835), and click **Install** (or **Update** if you have it already).

#### Install Xcode Command Line Tools

Open Xcode, choose **Settings...** from the Xcode menu (or press <kbd>cmd ⌘</kbd> + <kbd>,</kbd>). Go to the **Locations** and install the tools by selecting the most recent version in the **Command Line Tools** dropdown.

#### Install an iOS Simulator in Xcode

To install an iOS Simulator, open **Xcode > Settings... > Components**, and under **Platform Support > iOS ...**, click **Get**.

#### Install Watchman

[Watchman](https://facebook.github.io/watchman/docs/install#macos) is a tool for watching changes in the filesystem. Installing it will result in better performance. You can install it with:

```sh
brew update
brew install watchman
```

### Configure your project

#### Install expo-dev-client

Run the following command in your project's root directory:

```sh
npx expo install expo-dev-client
```

#### Plug in your device via USB and enable developer mode

1. Connect your iOS device to your Mac using a USB cable. Unlock the device and tap **Trust** if prompted.

2. Open Xcode. From the menu bar, select **Window** > **Devices and Simulators**. You will see a warning in Xcode to enable developer mode.

3. On your iOS device, open **Settings** > **Privacy & Security**, scroll down to the **Developer Mode** list item and navigate into it.

4. Tap the switch to enable **Developer Mode**. After you do so, Settings presents an alert to warn you that Developer Mode reduces your device's security. To continue enabling **Developer Mode**, tap the alert's **Restart** button.

5. After the device restarts and you unlock it, the device shows an alert confirming that you want to enable Developer Mode. Tap **Turn On**, and enter your device passcode when prompted.

#### Run the project on your device

1. Add the `ios.bundleIdentifier` in the **app.json** file in the root directory to a unique value so that Xcode generates the provisioning profile for the app signing step.

2. Run the following command in your project's root directory and select your plugged in device from the list:

```sh
npx expo run:ios --device
```

> This command runs a development server after building your app. You can skip running `npx expo start` on the next page.

---

## iOS Simulator with Expo Go

### Set up an iOS Simulator with Expo Go

### Set up Xcode

#### Install Xcode

Open up the Mac App Store, search for [Xcode](https://apps.apple.com/us/app/xcode/id497799835), and click **Install** (or **Update** if you have it already).

#### Install Xcode Command Line Tools

Open Xcode, choose **Settings...** from the Xcode menu (or press <kbd>cmd ⌘</kbd> + <kbd>,</kbd>). Go to the **Locations** and install the tools by selecting the most recent version in the **Command Line Tools** dropdown.

#### Install an iOS Simulator in Xcode

To install an iOS Simulator, open **Xcode > Settings... > Components**, and under **Platform Support > iOS ...**, click **Get**.

#### Install Watchman

[Watchman](https://facebook.github.io/watchman/docs/install#macos) is a tool for watching changes in the filesystem. Installing it will result in better performance. You can install it with:

```sh
brew update
brew install watchman
```

### Install Expo Go

When you start a development server with `npx expo start` on the [start developing](/get-started/start-developing) page, press <kbd>i</kbd> to open the iOS Simulator. Expo CLI will install Expo Go automatically.

---

## iOS Simulator with a development build (EAS)

### Set up an iOS Simulator with a development build

### Set up Xcode

#### Install Xcode

Open up the Mac App Store, search for [Xcode](https://apps.apple.com/us/app/xcode/id497799835), and click **Install** (or **Update** if you have it already).

#### Install Xcode Command Line Tools

Open Xcode, choose **Settings...** from the Xcode menu (or press <kbd>cmd ⌘</kbd> + <kbd>,</kbd>). Go to the **Locations** and install the tools by selecting the most recent version in the **Command Line Tools** dropdown.

#### Install an iOS Simulator in Xcode

To install an iOS Simulator, open **Xcode > Settings... > Components**, and under **Platform Support > iOS ...**, click **Get**.

#### Install Watchman

[Watchman](https://facebook.github.io/watchman/docs/install#macos) is a tool for watching changes in the filesystem. Installing it will result in better performance. You can install it with:

```sh
brew update
brew install watchman
```

### Create a development build

#### Install EAS CLI

To build your app, you will need to install EAS CLI. You can do this by running the following command in your terminal:

```sh
npm install -g eas-cli
```

#### Create an Expo account and login

Next, you will need to create an Expo account and login to the EAS CLI.

1. [Sign up](https://expo.dev/signup) for an Expo account.
2. Run the following command in your terminal to log in to the EAS CLI:

```sh
eas login
```

#### Configure your project

Run the following command to create an EAS config in your project:

```sh
eas build:configure
```

#### Adjust your build profile

To create a simulator-compatible development build, you'll need to update your build profile in **eas.json** to set the `ios.simulator` property to `true`:

```json eas.json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      /* @info */
      "ios": {
        "simulator": true
      }
      /* @end */
    }
  }
}
```

#### Create a development build

Run the following command to create a development build:

```sh
eas build --platform ios --profile development
```

#### Install the development build on your simulator

After the build is complete, the CLI will prompt you to automatically download and install it on the iOS Simulator. When prompted, press <kbd>Y</kbd> to directly install it on the simulator.

If you miss this prompt, you can download the build from the link provided in the terminal and drag and drop it onto the iOS Simulator to install it.

---

## iOS Simulator with a development build (local)

### Set up an iOS Simulator with a development build

### Set up Xcode and Watchman

#### Install Xcode

Open up the Mac App Store, search for [Xcode](https://apps.apple.com/us/app/xcode/id497799835), and click **Install** (or **Update** if you have it already).

#### Install Xcode Command Line Tools

Open Xcode, choose **Settings...** from the Xcode menu (or press <kbd>cmd ⌘</kbd> + <kbd>,</kbd>). Go to the **Locations** and install the tools by selecting the most recent version in the **Command Line Tools** dropdown.

#### Install an iOS Simulator in Xcode

To install an iOS Simulator, open **Xcode > Settings... > Components**, and under **Platform Support > iOS ...**, click **Get**.

#### Install Watchman

[Watchman](https://facebook.github.io/watchman/docs/install#macos) is a tool for watching changes in the filesystem. Installing it will result in better performance. You can install it with:

```sh
brew update
brew install watchman
```

### Running your app on an iOS Simulator

#### Install expo-dev-client

Run the following command in your project's root directory:

```sh
npx expo install expo-dev-client
```

Run the following from your terminal:

```sh
npx expo run:ios
```

> This command runs a development server after building your app. You can skip running `npx expo start` on the next page.

## Next step

You have a project and a development environment. Now it's time to start developing.

---

---
modificationDate: February 26, 2026
title: Start developing
description: Make your first change to an Expo project and see it live on your device.
---

# Start developing

Make your first change to an Expo project and see it live on your device.

## Start a development server

To start the development server, run the following command:

```sh
npx expo start
```

## Open the app on your device

After running the command above, you will see a QR code in your terminal. Scan this QR code to open the app on your device.

If you're using an Android Emulator or iOS Simulator, you can press a or i respectively to open the app.

Having problems?

Make sure you are on the same Wi-Fi network on your computer and your device.

If it still doesn't work, it may be due to the router configuration — this is common for public networks. You can work around this by choosing the **Tunnel** connection type when starting the development server, then scanning the QR code again.

```sh
npx expo start --tunnel
```

> Using the **Tunnel** connection type will make the app reloads considerably slower than on **LAN** or **Local**, so it's best to avoid tunnel when possible. You may want to install and use an emulator or simulator to speed up development if **Tunnel** is required to access your machine from another device on your network.

## Make your first change

Open the **src/app/index.tsx** file in your code editor and make a change.

```diff
- Welcome to Expo
+ Hello World!
```

Changes not showing up on your device?

Expo Go is configured by default to automatically reload the app whenever a file is changed, but let's make sure to go over the steps to enable it in case somehow things aren't working.

-   Make sure you have the [development mode enabled in Expo CLI](/workflow/development-mode#development-mode).

-   Close the Expo app and reopen it.

-   Once the app is open again, shake your device to reveal the developer menu. Press Cmd ⌘ + D.

-   If you see **Fast Refresh** enabled, toggle it. If you see **Disable Fast Refresh**, dismiss the developer menu. Now try making another change.


## File structure

Below, you can get familiar with the default project's file structure:

Files

### app

Contains the app's navigation, which is file-based. The file structure of the **src/app** directory determines the app's navigation.

The app has two routes defined by two files: **src/app/index.tsx** and **src/app/explore.tsx**. The layout file in **src/app/_layout.tsx** sets up the tab navigator using the platform-specific **AppTabs** component.

## Features

The default project template has the following features:

Default project

### File-based routing

The app has two screens: **src/app/index.tsx** and **src/app/explore.tsx**. The layout file in **src/app/_layout.tsx** sets up navigation using a platform-specific **AppTabs** component that uses native tabs on Android and iOS, and Expo Router UI tabs on web.

---

---
modificationDate: May 22, 2024
title: Next steps
description: Develop, review, and submit your project.
---

# Next steps

Develop, review, and submit your project.

Here are next steps to continue building your app:

### Reset your project

You can remove the boilerplate code and start fresh with a new project. Run the following command to reset your project:

```sh
npm run reset-project
```

This command will move the existing files in **app** to **app-example**, then create a new **app** directory with a new **index.tsx** file.

### Develop, review, and deploy

Learn how to develop by reading the docs in the Develop section. You'll learn how to create [UI elements](/develop/user-interface/splash-screen-and-app-icon), add [unit tests](/develop/unit-testing), include [native modules](/config-plugins/introduction), and more.

Once you've developed your app, you can share it with your teammates for [review](/review/overview).

Finally, you can [build](/deploy/build-project) and [submit](/deploy/submit-to-app-stores) your project to the app stores.

### Step-by-step guide

For a guided, step-by-step walkthrough of building an app with Expo from start to finish, check out the [tutorial](/tutorial/introduction).

---

---
modificationDate: March 18, 2026
title: Expo Skills for AI agents
description: A list of official AI agent skills provided by Expo for building, deploying, and debugging Expo and React Native apps.
---

# Expo Skills for AI agents

A list of official AI agent skills provided by Expo for building, deploying, and debugging Expo and React Native apps.

Expo Skills are structured instruction files that teach AI agents how to build, deploy, and debug Expo and React Native apps accurately and efficiently. They work with Claude Code, Cursor, Codex, and other AI agents.

## Install Expo Skills

Run the following commands to add and install Expo Skills from the plugin marketplace:

```sh
/plugin marketplace add expo/skills
/plugin install expo
```

## Available Expo Skills

The following skills are available in the `expo` plugin:

| Skill | Description |
| --- | --- |
| [`building-native-ui`](https://github.com/expo/skills/blob/main/plugins/expo/skills/building-native-ui/SKILL.md) | Complete guide for building beautiful apps with Expo Router. Covers fundamentals, styling, components, navigation, animations, patterns, and native tabs. |
| [`expo-api-routes`](https://github.com/expo/skills/blob/main/plugins/expo/skills/expo-api-routes/SKILL.md) | Guidelines for creating API routes in Expo Router with EAS Hosting. |
| [`expo-cicd-workflows`](https://github.com/expo/skills/blob/main/plugins/expo/skills/expo-cicd-workflows/SKILL.md) | Helps understand and write EAS workflow YAML files for Expo projects. Use this skill when the user asks about CI/CD or workflows in an Expo or EAS context, mentions .eas/workflows/, or wants help with EAS build pipelines or deployment automation. |
| [`expo-deployment`](https://github.com/expo/skills/blob/main/plugins/expo/skills/expo-deployment/SKILL.md) | Deploying Expo apps to iOS App Store, Android Play Store, web hosting, and API routes. |
| [`expo-dev-client`](https://github.com/expo/skills/blob/main/plugins/expo/skills/expo-dev-client/SKILL.md) | Build and distribute Expo development clients locally or via TestFlight. |
| [`expo-tailwind-setup`](https://github.com/expo/skills/blob/main/plugins/expo/skills/expo-tailwind-setup/SKILL.md) | Set up Tailwind CSS v4 in Expo with react-native-css and NativeWind v5 for universal styling. |
| [`expo-ui-jetpack-compose`](https://github.com/expo/skills/blob/main/plugins/expo/skills/expo-ui-jetpack-compose/SKILL.md) | `@expo/ui/jetpack-compose` package lets you use Jetpack Compose Views and modifiers in your app. |
| [`expo-ui-swift-ui`](https://github.com/expo/skills/blob/main/plugins/expo/skills/expo-ui-swift-ui/SKILL.md) | `@expo/ui/swift-ui` package lets you use SwiftUI Views and modifiers in your app. |
| [`native-data-fetching`](https://github.com/expo/skills/blob/main/plugins/expo/skills/native-data-fetching/SKILL.md) | Use when implementing or debugging ANY network request, API call, or data fetching. Covers fetch API, React Query, SWR, error handling, caching, offline support, and Expo Router data loaders (useLoaderData). |
| [`upgrading-expo`](https://github.com/expo/skills/blob/main/plugins/expo/skills/upgrading-expo/SKILL.md) | Guidelines for upgrading Expo SDK versions and fixing dependency issues. |
| [`use-dom`](https://github.com/expo/skills/blob/main/plugins/expo/skills/use-dom/SKILL.md) | Use Expo DOM components to run web code in a webview on native and as-is on web. Migrate web code to native incrementally. |

## Example prompts

Try the following prompts after installing Expo Skills. Your AI agent will automatically use the appropriate skill:

| Example prompt | Skill used |
| --- | --- |
| Build a settings screen with a form and navigation | `building-native-ui` |
| Set up Tailwind CSS in my Expo project | `expo-tailwind-setup` |
| Embed a recharts chart in my native app using web code | `use-dom` |
| Add a SwiftUI picker component to my Expo app | `expo-ui-swift-ui` |
| Use Material Design 3 components with Jetpack Compose | `expo-ui-jetpack-compose` |
| How do I deploy my Expo app to the Apple App Store? | `expo-deployment` |
| Create a CI/CD workflow that builds on every PR | `expo-cicd-workflows` |
| Upgrade my project to the latest Expo SDK | `upgrading-expo` |

## Additional resources

[expo/skills GitHub repository](https://github.com/expo/skills) — expo/skills — Browse the source for all available Expo Skills, or report issues.

[Expo MCP Server](/eas/ai/mcp) — Companion AI tooling that gives coding agents direct access to Expo and EAS services.

---

---
modificationDate: March 06, 2026
title: Documentation for AI agents and LLMs
description: Efficient ways for AI agents and LLMs to access and consume Expo documentation.
---

# Documentation for AI agents and LLMs

Efficient ways for AI agents and LLMs to access and consume Expo documentation.

Use the following endpoints and tools to give AI agents and LLMs access to Expo documentation at lower token cost than fetching full web pages.

## Quick start

Pick the method that matches your tool:

| Method | Best for | How |
| --- | --- | --- |
| Per-page markdown | Chat interfaces (ChatGPT, Claude.ai) and coding agents | Append `/index.md` to any documentation page URL. |
| Copy Markdown dropdown | Quick prompts with a single page | Click **Copy page** > **Copy Markdown** at the top of any documentation page. |
| Section bundles | Project rules and coding agents | Add a section-level `llms-*.txt` URL to your AI tool configuration or the general-purpose index (`/llms.txt`). |

## Per-page markdown

Every documentation page has a lightweight markdown version accessible by appending `/index.md` to the page URL. For example:

```text
https://documentation.expo.dev/develop/development-builds/create-a-build/index.md
```

The above method is useful when you want to give an AI agent context about a specific topic or page without overwhelming it with the full HTML of that page.

## Documentation bundles

At Expo, we support the [llms.txt](https://llmstxt.org/) initiative to provide documentation for large language models (LLMs) and apps that use them. Below is a list of documentation files available.

### Site-wide bundles

| Endpoint | Description | Size |
| --- | --- | --- |
| [/llms.txt](/llms.txt) | Index page with a list of all available documentation files. | ~94 kB |
| [/llms-full.txt](/llms-full.txt) | Complete documentation for Expo, including Expo Router, Expo Modules API, development process, and more. | ~1.9 MB |

### Section-wide bundles

| Endpoint | Description | Size |
| --- | --- | --- |
| [/llms-eas.txt](/llms-eas.txt) | Complete documentation for Expo Application Services (EAS). | ~974 kB |
| [/llms-sdk.txt](/llms-sdk.txt) | Complete documentation for the latest Expo SDK. | ~2.6 MB |

Looking for deprecated Expo SDK versions?

-   [/llms-sdk-v54.0.0.txt](/llms-sdk-v54.0.0.txt): Documentation for the Expo SDK v54.0.0

-   [/llms-sdk-v53.0.0.txt](/llms-sdk-v53.0.0.txt): Documentation for the Expo SDK v53.0.0

-   [/llms-sdk-v52.0.0.txt](/llms-sdk-v52.0.0.txt): Documentation for the Expo SDK v52.0.0

-   [/llms-sdk-v51.0.0.txt](/llms-sdk-v51.0.0.txt): Documentation for the Expo SDK v51.0.0

---

---
modificationDate: March 01, 2026
title: Tools for development
description: An overview of Expo tools and websites that will help you during various aspects of your project-building journey.
---

# Tools for development

An overview of Expo tools and websites that will help you during various aspects of your project-building journey.

When you create a new project with Expo, learning about the following essential tools and websites can help you during your app development journey. This page provides an overview of a list of recommended tools.

## Expo CLI

Expo CLI is a development tool and is installed automatically with the `expo` package when you create a new project. You can use it by leveraging `npx` (a Node.js package runner).

It is designed to help you move faster during the app development phase. For example, your first interaction with Expo CLI is starting the development server by running the command: `npx expo start`.

The following is a list of common commands that you will use with Expo CLI while developing your app:

| Command | Description |
| --- | --- |
| `npx expo start` | Starts the development server (whether you are using a development build or Expo Go). |
| `npx expo prebuild` | Generates native Android and iOS directories using [Prebuild](/workflow/continuous-native-generation). |
| `npx expo run:android` | Compiles native Android app locally. |
| `npx expo run:ios` | Compiles native iOS app locally. |
| `npx expo install package-name` | Used to install a new library or validate and update specific libraries in your project by adding `--fix` option to this command. |
| `npx expo lint` | [Setup and configures](/guides/using-eslint) ESLint. If ESLint is already configured, this command will [lint your project files](/guides/using-eslint#usage). |

In a nutshell, Expo CLI allows you to develop, compile, start your app, and more. See [Expo CLI reference](/more/expo-cli) for more available options and actions you can perform with the CLI.

## EAS CLI

EAS CLI is used to log in to your Expo account and compile your app using different EAS services such as Build, Update, or Submit. You can also use this tool to:

-   Publish your app to the app stores
-   Create a development, preview, or production build of your app
-   Create over-the-air (OTA) updates
-   Manage your app credentials
-   Create an ad hoc provisioning profile for an iOS device

To use EAS CLI, you need to install it globally on your local machine by running the command:

```sh
npm install -g eas-cli
```

You can use `eas --help` in your terminal window to learn more about the available commands. For a complete reference, see [`eas-cli` npm page](https://www.npmjs.com/package/eas-cli).

## Expo Doctor

Expo Doctor is a command line tool used to diagnose issues in your Expo project. To use it, run the following command in your project's root directory:

```sh
npx expo-doctor
```

This command performs checks and analyzes your project's codebase for common issues in [app config](/workflow/configuration) and **package.json** files, dependency compatibility, configuration files, and the overall health of the project. Once the check is complete, Expo Doctor outputs the results.

If Expo Doctor finds an issue, it provides a description of the problem along with advice on how to fix it or where to find help.

By default, Expo Doctor validates your project's packages against the [React Native directory](https://reactnative.directory/) and checks if app config properties are properly synced when native directories exist. You can configure these checks in your project's **package.json** file. See [`reactNativeDirectoryCheck`](/versions/latest/config/package-json#reactnativedirectorycheck) and [`appConfigFieldsNotSyncedCheck`](/versions/latest/config/package-json#appconfigfieldsnotsynced) for more details.

You can also use `npx expo-doctor --help` to display usage information.

## Orbit

Orbit is a macOS and Windows app that enables:

-   Install and launch builds from EAS on physical devices and emulators.
-   Install and launch updates from EAS on Android Emulators or iOS Simulators.
-   Launch snack projects on Android Emulators or iOS Simulators.
-   Use local files to install and launch apps. Orbit supports any Android **.apk**, iOS Simulator compatible **.app**, or ad hoc signed apps.
-   See a list of pinned projects from your EAS dashboard.

### Installation

You can download Orbit with Homebrew for macOS, or directly from the [GitHub releases](https://github.com/expo/orbit/releases).

```sh
brew install expo-orbit
```

If you want Orbit to start when you log in automatically, click on the Orbit icon in the menu bar, then **Settings** and select the **Launch on Login** option.

> Orbit relies on the Android SDK on both macOS and Windows and `xcrun` for device management only on macOS, which requires setting up both [Android Studio](/workflow/android-studio-emulator) and [Xcode](/workflow/ios-simulator).

## Expo Tools for VS Code

Expo Tools is a VS Code extension to improve your development experience when working with app config files. It provides features such as autocomplete and intellisense for files such as app config, EAS config, store config and Expo Module config files.

[Install Expo Tools VS Code extension](https://marketplace.visualstudio.com/items?itemName=expo.vscode-expo-tools) — Use this link to install the extension or search Expo Tools directly in your VS Code editor.

You can also use it to debug your app using VS Code's built-in debugger to set breakpoints, inspect variables, execute code through the debug console, and more. See [Debugging with VS Code](/debugging/tools#debugging-with-vs-code) for how to use this extension for debugging.

## Test prototypes with Snack and Expo Go

### Snack

Snack is an in-browser development environment that works similarly to Expo Go. It's a great way to share code snippets and experiment with React Native without downloading any tools on your computer.

To use it, go to [snack.expo.dev](https://snack.expo.dev/), edit the `<Text>` component in **App.js**, choose a platform (Android, iOS, or web) in the right panel and see the changes live.

### Expo Go

[Expo Go](https://expo.dev/go) is a free, open-source playground for students and learners to try out React Native. It works with Android and iOS.

For more information on how to use it:

-   Click [this link](/get-started/set-up-your-environment?mode=expo-go) to go to Set up your environment guide
-   Select a platform to develop under **Where would you like to develop?**
-   Select Expo Go under **How would you like to develop?**
-   Follow the instructions described in that guide

> **Note:** Expo Go is limited and not useful for building production-grade projects. Use [development builds](/get-started/set-up-your-environment?mode=development-build) instead.

What if I open a project with an unsupported SDK version?

When running a project that was created for an unsupported SDK version in Expo Go, you'll see the following error:

```sh
"Project is incompatible with this version of Expo Go"
```

To fix this, upgrading your project to a [supported SDK version](/versions/latest#each-expo-sdk-version-depends-on-a-react-native-version) is recommended. If you want to learn how to do it, see [Upgrade the project to a new SDK Version](/develop/tools#how-do-i-upgrade-my-project-from).

How do I upgrade my project from an unsupported SDK version?

See [Upgrading Expo SDK guide](/workflow/upgrading-expo-sdk-walkthrough) for instructions for upgrading to a specific SDK version.

## React Native directory

Any library that is compatible with React Native works in an Expo project when you use a development build to create your project.

[reactnative.directory](https://reactnative.directory/) is a searchable database for React Native libraries. If a library you are looking for is not included in Expo SDK, use the directory to find a compatible library for your project.

[Use libraries](/workflow/using-libraries) — See this guide to learn more about the difference between React Native core libraries, Expo SDK libraries, and third-party libraries. It also explains how to determine third-party library compatibility.

---

---
modificationDate: February 26, 2026
title: Navigation in Expo and React Native apps
description: Learn about the recommended approach for integrating navigation in an Expo and React Native project.
---

# Navigation in Expo and React Native apps

Learn about the recommended approach for integrating navigation in an Expo and React Native project.

The core React Native library does not include a built-in navigation solution, so you can choose a navigation library that best fits your needs. For Expo and React Native apps, it is generally a choice between [React Navigation](https://reactnavigation.org/) or [Expo Router](/router/introduction).

## Why React Native apps needs a navigation library

React Native core includes basic UI components, touch handling, device APIs and networking, but excludes, among other things, storage, camera, maps, most device sensors, and **navigation**! These are intended to be covered by community libraries.

## React Navigation

React Navigation is a component-based navigation library widely used across the React Native ecosystem. It lets you compose stack, tab, and drawer navigators entirely in code so you can implement complex flows, custom transitions, and app-specific UX patterns.

The library offers platform-specific look-and-feel with smooth animations and gestures, unified mobile and web routing, automatic deep links, type routes with static configuration, and is highly customizable.

[React Navigation: Getting started](https://reactnavigation.org/docs/getting-started) — Learn how to get started with React Navigation.

## Expo Router (recommended for Expo projects)

Expo Router is a file-based routing library for Expo and React Native projects and is a built on top of React Navigation. By following the **app** directory convention, it turns files into routes and is integrated with Expo for [Expo CLI](/more/expo-cli) and bundling without additional setup. The library also adds features such as typed routes, dynamic routes, lazy bundling in development, static rendering for the web, and automatic deep linking.

New Expo projects created with `npx create-expo-app@latest --template default@sdk-55` include Expo Router by default so you can ship cross-platform navigation quickly while still being able to reach for React Navigation APIs when needed.

[Introduction to Expo Router](/router/introduction) — Expo Router is an open-source routing library for Universal React Native applications built with Expo.

[Installation](/router/installation) — Learn how to quickly get started by creating a new project with Expo Router or adding the library to an existing project.

[Core concepts](/router/basics/core-concepts) — Learn about the core concepts of file-based routing in Expo.

---

---
modificationDate: March 01, 2026
title: Splash screen and app icon
description: Learn how to add a splash screen and app icon to your Expo project.
---

# Splash screen and app icon

Learn how to add a splash screen and app icon to your Expo project.

A splash screen and an app icon are fundamental elements of a mobile app. They play an important role in the user experience and branding of the app. This guide provides steps on how to create and add them to your app.

[Create an App Icon and Splash Screen](https://www.youtube.com/watch?v=3Bsw8a1BJoQ) — See a detailed walkthrough on how to create an app icon and splash screen for an Expo project.

## Splash screen

A splash screen, also known as a launch screen, is the first screen a user sees when they open your app. It stays visible while the app is loading. You can also control the behavior of when a splash screen disappears by using the native [SplashScreen API](/versions/latest/sdk/splash-screen).

The [`expo-splash-screen`](/versions/latest/sdk/splash-screen) has a built-in [config plugin](/config-plugins/introduction) that lets you configure properties such as the splash icon and background color.

> **Do not use Expo Go or a development build to test your splash screen**. Expo Go renders your app icon while the splash screen is visible, which can interfere with testing. Development builds include `expo-dev-client`, which has its own splash screen and may cause conflicts. **Instead, use a [preview build](/build/eas-json#preview-builds) or a [production build](/build/eas-json#production-builds)**.

### Create a splash screen icon

To create a splash screen icon, you can use this [Figma template](https://www.figma.com/community/file/1466490409418563617). It provides a bare minimum design for an icon and splash images for Android and iOS.

**Recommended:**

-   Use a 1024x1024 image.
-   Use a **.png** file.
-   Use a transparent background.

### Export the splash icon as a .png

After creating a splash screen icon, export it as a **.png** and save it in the **assets/images** directory. By default, Expo uses **splash-icon.png** as the file name. If you decide to change the name of your splash screen file, make sure to use that in the next step.

> **Note:** **Currently, only .png images are supported** to use as a splash screen icon in an Expo project. If you use another image format, making a production build of your app will fail.

### Configure the splash screen icon

Open the app config file, and under plugins, set the following properties:

```json
{
  "expo": {
    "plugins": [
      [
        "expo-splash-screen",
        {
          "backgroundColor": "#232323",
          "image": "./assets/images/splash-icon.png",
          "dark": {
            "image": "./assets/images/splash-icon-dark.png",
            "backgroundColor": "#000000"
          },
          "imageWidth": 200
        }
      ]
    ]
  }
}
```

To test your new splash screen, build your app for [internal distribution](/tutorial/eas/internal-distribution-builds) or for production, see guides on [Android](/tutorial/eas/android-production-build) and [iOS](/tutorial/eas/ios-production-build).

[Configurable splash screen properties](/versions/latest/sdk/splash-screen#configurable-properties) — Learn about the configurable properties of the SplashScreen API.

Configuring `expo-splash-screen` properties separately for Android and iOS

[`expo-splash-screen`](/versions/latest/sdk/splash-screen) also supports `android` and `ios` properties for configuring the splash screen for a specific platform. See the following example:

```json
{
  "expo": {
    "plugins": [
      [
        "expo-splash-screen",
        {
          "ios": {
            "backgroundColor": "#ffffff",
            "image": "./assets/images/splash-icon.png",
            "resizeMode": "cover"
          },
          "android": {
            "backgroundColor": "#0c7cff",
            "image": "./assets/images/splash-android-icon.png",
            "imageWidth": 150
          }
        }
      ]
    ]
  }
}
```

Not using prebuild?

If your app does not use [Expo Prebuild](/more/glossary-of-terms#prebuild) (formerly the _managed workflow_) to generate the native **android** and **ios** directories, then changes in the app config will have no effect. For more information, see [how you can customize the configuration manually](https://github.com/expo/expo/tree/main/packages/expo-splash-screen#-installation-in-bare-react-native-projects).

Troubleshooting: New splash screen not appearing on iOS

For SDK 52 and earlier, in iOS development builds, launch screens can sometimes remain cached between builds, making it harder to test new images. Apple recommends clearing the _derived data_ directory before rebuilding, this can be done with Expo CLI by running:

```sh
npx expo run:ios --no-build-cache
```

See [Apple's guide on testing launch screens](https://developer.apple.com/documentation/technotes/tn3118-debugging-your-apps-launch-screen) for more information.

## App icon

An app's icon is what your app users see on their device's home screen and app stores. Android and iOS have different and strict requirements.

### Create an app icon

To create an app icon, you can use this [Figma template](https://www.figma.com/community/file/1466490409418563617). It provides a bare minimum design for an icon and splash images for Android and iOS.

### Export the icon image as a .png

After creating an app icon, export it as **.png** and save it in the **assets/images** directory. By default, Expo uses **icon.png** as the file name. If you decide to use a different file name, make sure to use that in the next step.

### Add the icon in app config

Open the app config and add the local path as the value of [`icon`](/versions/latest/config/app#icon) property to point it to your new app icon:

```json
{
  "icon": "./assets/images/icon.png"
}
```

Custom configuration tips for Android and iOS

#### Android

Further customization of the Android icon is possible using the [`android.adaptiveIcon`](/versions/latest/config/app#adaptiveicon) property, which will override both of the previously mentioned settings.

The Android Adaptive Icon is formed from two separate layers — a foreground image and a background color or image. This allows the OS to mask the icon into different shapes and also supports visual effects. For Android 13 and later, the OS supports a themed app icon that uses a wallpaper and theme to determine the color set by the device's theme.

The design you provide should follow the [Android Adaptive Icon Guidelines](https://developer.android.com/develop/ui/views/launch/icon_design_adaptive) for launcher icons. You should also:

-   Use **.png** files.
-   Use the `android.adaptiveIcon.foregroundImage` property to specify the path to your foreground image.
-   Use the `android.adaptiveIcon.monochromeImage` property to specify the path to your monochrome image.
-   The default background color is white; to specify a different background color, use the `android.adaptiveIcon.backgroundColor` property. You can instead specify a background image using the `android.adaptiveIcon.backgroundImage` property. Make sure that it has the same dimensions as your foreground image.

You may also want to provide a separate icon for older Android devices that do not support Adaptive Icons. You can do so with the `android.icon` property. This single icon would be a combination of your foreground and background layers.

> See [Apple best practices](https://developer.apple.com/design/human-interface-guidelines/app-icons/#Best-practices) to ensure your icon looks professional, such as testing your icon on different wallpapers and avoiding text beside your product's wordmark. Provide an icon that's at least 512x512 pixels.

#### iOS

[Icon Composer](https://www.youtube.com/watch?v=RZ_QMym3adw) — Learn how to use the new Icon Composer to create app icons for an Expo project.

For iOS, your app's icon should follow the [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/app-icons/). You can use the [Icon Composer](https://developer.apple.com/icon-composer/) app to create your app icon. This will output a **.icon** directory that you can add to your project's **assets** directory. You can then provide the path to this directory in your app config. Adding support for dark mode is handled in Icon Composer, so you do not need to provide variants when using this approach.

> **Note:** Providing an Icon Composer **.icon** directory via `ios.icon` is supported **in SDK 54** and later.

```json
{
  "expo": {
    "ios": {
      "icon": "./assets/app.icon"
    }
  }
}
```

Alternatively, the previous approach of providing an image is still supported. You should:

-   Use a **.png** file.
-   1024x1024 is a good size. If you have an Expo project created using `npx create-expo-app`, [EAS Build](/build/setup) will generate the other sizes for you. In case of a bare React Native project, generate the icons on your own. The largest size EAS Build generates is 1024x1024.
-   The icon must be exactly square. For example, a 1023x1024 icon is not valid.
-   Make sure the icon fills the whole square, with no rounded corners or other transparent pixels. The operating system will mask your icon when appropriate.
-   Use `ios.icon` to specify different icons for various system appearances (for example, dark and tinted) can be provided. If specified, this overrides the top-level icon key in the app config file. See the example below:

```json
{
  "expo": {
    "ios": {
      "icon": {
        "dark": "./assets/images/ios-dark.png",
        "light": "./assets/images/ios-light.png",
        "tinted": "./assets/images/ios-tinted.png"
      }
    }
  }
}
```

---

---
modificationDate: February 26, 2026
title: Safe areas
description: Learn how to add safe areas for screen components inside your Expo project.
---

# Safe areas

Learn how to add safe areas for screen components inside your Expo project.

Creating a safe area ensures your app screen's content is positioned correctly. This means it doesn't get overlapped by notches, status bars, home indicators, and other interface elements that are part of the device's physical hardware or are controlled by the operating system. When the content gets overlapped, it gets concealed by these interface elements.

Here's an example of an app screen's content getting concealed by the status bar on Android. On iOS, the same content is concealed by rounded corners, notch, and the status bar.

## Use `react-native-safe-area-context` library

[`react-native-safe-area-context`](https://github.com/AppAndFlow/react-native-safe-area-context) provides a flexible API for handling Android and iOS device's safe area insets. It also provides a `SafeAreaView` component that you can use instead of a [`<View>`](https://reactnative.dev/docs/view) to account for safe areas automatically in your screen components.

Using the library, the result of the previous example changes as it displays the content inside a safe area, as shown below:

### Installation

You can skip installing `react-native-safe-area-context` if you have created a project using [the default template](/get-started/create-a-project). This library is installed as peer dependency for Expo Router library. Otherwise, install it by running the following command:

```sh
npx expo install react-native-safe-area-context
```

### Usage

You can directly use [`SafeAreaView`](https://appandflow.github.io/react-native-safe-area-context/api/safe-area-view) to wrap the content of your screen's component. It is a regular `<View>` with the safe area insets applied as extra padding or margin.

```tsx
import { Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function HomeScreen() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <Text>Content is in safe area.</Text>
    </SafeAreaView>
  );
}
```

Using a different Expo template and don't have Expo Router installed?

Import and add [`SafeAreaProvider`](https://appandflow.github.io/react-native-safe-area-context/api/safe-area-provider) to the root component file (such as **App.tsx**) before using `SafeAreaView` in your screen component.

```tsx
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function App() {
  return (
    return <SafeAreaProvider>...</SafeAreaProvider>;
  );
}
```

## Alternate: `useSafeAreaInsets` hook

Alternate to `SafeAreaView`, you can use [`useSafeAreaInsets`](https://appandflow.github.io/react-native-safe-area-context/api/use-safe-area-insets) hook in your screen component. It provides direct access to the safe area insets, allowing you to apply padding for each edge of the `<View>` using an inset from this hook.

The example below uses the `useSafeAreaInsets` hook. It applies top padding to a `<View>` using `insets.top`.

```tsx
import { Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function HomeScreen() {
  const insets = useSafeAreaInsets();

  return (
    <View style={{ flex: 1, paddingTop: insets.top }}>
      <Text>Content is in safe area.</Text>
    </View>
  );
}
```

The hook provides the insets in the following object:

```ts
{
  top: number,
  right: number,
  bottom: number,
  left: number
}
```

## Additional information

### Minimal example

Below is a minimal working example that uses the `useSafeAreaInsets` hook to apply top padding to a view.

```tsx
import { Text, View } from 'react-native';
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';

function HomeScreen() {
  const insets = useSafeAreaInsets();
  return (
    <View style={{ flex: 1, paddingTop: insets.top }}>
      <Text style={{ fontSize: 28 }}>Content is in safe area.</Text>
    </View>
  );
}

export default function App() {
  return (
    <SafeAreaProvider>
      <HomeScreen />
    </SafeAreaProvider>
  );
}
```

### Usage with React Navigation

By default, React Navigation supports safe areas and uses `react-native-safe-area-context` as a peer dependency. For more information, see the [React Navigation documentation](https://reactnavigation.org/docs/handling-safe-area/).

### Usage with web

If you are targeting the web, set up `SafeAreaProvider` as described in the [usage section](/develop/user-interface/safe-areas#usage). If you are doing server-side rendering (SSR), see the [Web SSR section](https://appandflow.github.io/react-native-safe-area-context/optimizations#web-ssr) in the library's documentation.

---

---
modificationDate: February 26, 2026
title: System bars
description: Learn how to handle and customize system bars for safe areas and edge-to-edge layout in your Expo project.
---

# System bars

Learn how to handle and customize system bars for safe areas and edge-to-edge layout in your Expo project.

System bars are the UI elements at the edges of the screen that provide essential device information and navigation controls. Depending on the mobile OS, they include the status bar ([Android](https://developer.android.com/design/ui/mobile/guides/foundations/system-bars) and [iOS](https://developer.apple.com/design/human-interface-guidelines/status-bars)), caption bar ([Android](https://medium.com/androiddevelopers/insets-handling-tips-for-android-15s-edge-to-edge-enforcement-872774e8839b#:~:text=or%20SHORT_EDGES.-,Caption%20bars,-When%20your%20app) only), navigation bar ([Android](https://developer.android.com/design/ui/mobile/guides/foundations/system-bars#navigation-bar) and [iOS](https://developer.apple.com/design/human-interface-guidelines/navigation-bars)), and home indicator (iOS only).

These components are used to display device information such as battery level, time, notification alerts, and provide direct interaction with the device from anywhere in the device's interface. For example, an app user can pull down the status bar to access quick settings and notifications regardless of which app they're currently using.

System bars are fundamental to the mobile experience, and understanding how to work with them properly is important for creating your app.

## Handling overlaps using safe areas

Some of your app's content may draw behind the system bars. To handle this, you need to position your app's content correctly by avoiding the overlap and ensuring that the controls from the system bars are present.

The following guide walks you through how to use `SafeAreaView` or a hook to apply insets directly for each edge of the screen.

[Safe areas](/develop/user-interface/safe-areas) — Learn how to add safe areas for screen components inside your Expo project.

### Safe areas and edge-to-edge layout on Android

Before [edge-to-edge on Android](https://expo.dev/blog/edge-to-edge-display-now-streamlined-for-android), it was common to have a translucent status bar and navigation bar. With this approach, the content drawn behind these bars was already underneath them, and it was typically not necessary to factor in safe areas.

Now, [with edge-to-edge on Android](https://expo.dev/blog/edge-to-edge-display-now-streamlined-for-android), you will need to use safe areas to ensure that content does not overlap with system bars.

## Customizing system bars

System bars can be customized to match your app's design and provide better visibility in different scenarios. When using Expo, there are two libraries available for this: `expo-status-bar` and `expo-navigation-bar` (Android only).

### Status bar configuration

The status bar appears at the top of the screen on both Android and iOS. You can customize it using [`expo-status-bar`](/versions/latest/sdk/status-bar). It provides a `StatusBar` component that you can use to control the appearance of the status bar while your app is running using the [`style`](/versions/latest/sdk/status-bar#style) property or the [`setStatusBarStyle`](/versions/latest/sdk/status-bar#statusbarsetstatusbarstylestyle-animated) method:

```tsx
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  <>
    {/* Use light text instead of dark text in the status bar to provide more contrast with a dark background. */}
    <StatusBar style="light" />
  </>;
}
```

> **Note:** In Expo default template, the `style` property is set to `auto`. It automatically picks the appropriate style depending on the color scheme (light or dark mode) currently used by your app.

To control the `StatusBar` visibility, you can set the [`hidden`](/versions/latest/sdk/status-bar#hidden) property to `true` or use the [`setStatusBarHidden`](/versions/latest/sdk/status-bar#statusbarsetstatusbarhiddenhidden-animation) method.

**With edge-to-edge enabled on Android, features from `expo-status-bar` that depend on an opaque status bar [are unavailable](https://developer.android.com/about/versions/15/behavior-changes-15#edge-to-edge)**. It's only possible to customize the style and visibility. Other properties will no-op and warn.

### Navigation bar configuration (Android only)

On Android devices, the Navigation Bar appears at the bottom of the screen. You can customize it using the [`expo-navigation-bar`](/versions/latest/sdk/navigation-bar) library. It provides a `NavigationBar` component that you can use to set the style of the navigation bar using the [`setStyle`](/versions/latest/sdk/navigation-bar#navigationbarsetstylestyle) method:

```tsx
import { Platform } from 'react-native';
import * as NavigationBar from 'expo-navigation-bar';
import { useEffect } from 'react';

useEffect(() => {
  if (Platform.OS === 'android') {
    // Set the navigation bar style
    NavigationBar.setStyle('dark');
  }
}, []);
```

To control the `NavigationBar` visibility, you can use the [`setVisibilityAsync`](/versions/latest/sdk/navigation-bar#navigationbarsetvisibilityasyncvisibility) method.

**With edge-to-edge enabled on Android, features from `expo-navigation-bar` that depend on an opaque navigation bar [are unavailable](https://developer.android.com/about/versions/15/behavior-changes-15#edge-to-edge)**. It's only possible to customize the style and visibility. Other properties will no-op and warn.

---

---
modificationDate: February 26, 2026
title: Fonts
description: Learn how to integrate custom fonts in your app using local files or Google Font packages
---

# Fonts

Learn how to integrate custom fonts in your app using local files or Google Font packages

Android and iOS come with their own set of platform fonts. To provide a consistent user experience and enhance your app's branding, you can use custom fonts.

This guide covers different ways you can add and load a custom font into your project and also provides additional information related to fonts.

## Add a custom font

There are two ways you can add a custom font into your project:

-   Add a font file into your local assets. For example, a font file in the **assets/fonts** directory.
-   Install a Google Font package. For example, installing [`@expo-google-fonts/inter`](https://www.npmjs.com/package/@expo-google-fonts/inter) package.

### Supported font formats

Expo SDK officially supports OTF and TTF font formats across Android, iOS and web platforms. If your font is in another font format, you have to set up advanced configuration to support that format in your project.

### Variable fonts

Variable fonts, including variable font implementations in OTF and TTF, do not have support across all platforms. For full platform support, use static fonts. Alternatively, use a utility such as [fontTools](https://fonttools.readthedocs.io/en/latest/varLib/mutator.html) to extract the specific axis configuration you want to use from the variable font and save it as a separate font file.

### How to choose between OTF and TTF

If the font you're using has both OTF and TTF versions, prefer OTF. The **.otf** files are smaller than **.ttf** files. Sometimes, OTF also renders slightly better in certain contexts.

## Use a local font file

Copy the file into your project's **assets/fonts** directory.

> **assets/fonts** directory path is a common convention in React Native apps to put font files. You can place these files elsewhere if you follow a custom convention.

Two ways to use the local font file in your project:

-   Embed the font file with [`expo-font` config plugin](/versions/latest/sdk/font#configuration-in-app-config) (Android and iOS only).
-   Load the font file with [`useFonts`](/versions/latest/sdk/font#usefontsmap) hook at runtime (Android, iOS, and web).

### With `expo-font` config plugin

The `expo-font` config plugin allows embedding one or more font files in your project's native code. It supports `ttf` and `otf` for both Android and iOS, and `woff` and `woff2` are supported on iOS only.

> **Note:** Config plugins only run on native platforms (Android and iOS). For web, use the [`useFonts` hook](/develop/user-interface/fonts#with-usefonts-hook) instead.

This is the recommended method for adding fonts to your app due to its benefits:

-   Fonts are available immediately when the app starts on a device.
-   No additional code required to load fonts in a project asynchronously when the app starts.
-   Fonts are consistently available across all devices where the app is installed because they're bundled within the app.

However, this method also has some limitations:

-   Doesn't work with Expo Go since this method requires [creating a development build](/develop/development-builds/create-a-build).

To embed a font in a project, follow the steps below:

After adding a custom font file in your project, install the `expo-font` library.

```sh
npx expo install expo-font
```

Add the config plugin to your [app config](/versions/latest/config/app#plugins) file. The configuration must contain the path to the font file using [`fonts`, `android` or `ios`](/versions/latest/sdk/font#configurable-properties) properties which take an array of one or more font definitions. The path to each font file is relative to the project's root.

The example below showcases all valid ways a font can be specified: as an array of objects that specify `fontFamily` and other properties, or an array of paths to font files.

For Android, you can specify the `fontFamily`, `weight`, and optionally `style` (defaults to `"normal"`), which will embed the fonts as native [XML resources](https://developer.android.com/develop/ui/views/text-and-emoji/fonts-in-xml). If you provide only the font file paths in an array, the file name becomes the font family name on Android. iOS always extracts the font family name from the font file itself.

If you plan to refer to fonts using just the `fontFamily`, provide an array of font paths (see `FiraSans-MediumItalic.ttf` below) and follow our [recommendation for file naming](/develop/user-interface/fonts#how-to-determine-which-font-family-name-to-use).

If you want to refer to fonts using a combination of `fontFamily`, `weight`, and `style`, provide an array of objects (see `Inter` below).

```json
{
  "expo": {
    "plugins": [
      [
        "expo-font",
        {
          "fonts": [
            "./assets/fonts/FiraSans-MediumItalic.ttf"
          ],
          "android": {
            "fonts": [
              {
                "fontFamily": "Inter",
                "fontDefinitions": [
                  {
                    "path": "./assets/fonts/Inter-BoldItalic.ttf",
                    "weight": 700,
                    "style": "italic"
                  },
                  {
                    "path": "./assets/fonts/Inter-Bold.ttf",
                    "weight": 700
                  }
                ]
              }
            ]
          },
          "ios": {
            "fonts": ["./assets/fonts/Inter-Bold.ttf", "./assets/fonts/Inter-BoldItalic.ttf"]
          }
        }
      ]
    ]
  }
}
```

After embedding the font with the config plugin, create a [new development build](/develop/development-builds/create-a-build) and install it on your device or Android Emulator or iOS Simulator.

You can use the font with `<Text>` by specifying the `fontFamily` style prop. The examples below correspond to the fonts defined in the configuration above.

```tsx
<Text style={{ fontFamily: 'Inter', fontWeight: '700' }}>Inter Bold</Text>
<Text style={{ fontFamily: 'Inter', fontWeight: '700', fontStyle: 'italic' }}>Inter Bold Italic</Text>
<Text style={{ fontFamily: 'FiraSans-MediumItalic' }}>Fira Sans Medium Italic</Text>
```

Using this method in an existing React Native project?

-   **Android:** Copy font files to **android/app/src/main/assets/fonts**.
-   **iOS:** See [Adding a Custom Font to Your App](https://developer.apple.com/documentation/uikit/text_display_and_fonts/adding_a_custom_font_to_your_app) in the Apple Developer documentation.

#### How to determine which font family name to use

-   If you provide fonts as an array of file paths (as described above), on Android, the file name (without the extension) becomes the font family name. On iOS, the font family name is read from the font file itself. We recommend naming the font file same as its [PostScript name](/develop/user-interface/fonts#what-is-postscript-name-of-a-font) so the font family name is consistent on both platforms.

-   If you use the object syntax, provide the "Family Name". This can be found in the Font Book app on macOS, [fontdrop.info](https://fontdrop.info/) or other programs.


What is PostScript name of a font file?

The **PostScript name** of a font file is a unique identifier assigned to the font that follows Adobe's PostScript standard. It is used by operating systems and apps to refer to the font. It is not a font's **display name**.

For example, Inter Black font file's PostScript name is `Inter-Black`.

_Screenshot from Font Book app on macOS._

### With `useFonts` hook

The `useFonts` hook from `expo-font` library allows loading the font file asynchronously. This hook keeps track of the loading state and loads the font when an app is initialized.

It works with all Expo SDK versions and with Expo Go. To load a font in a project using `useFonts` hook, follow the steps below:

After adding a custom font file in your project, install the `expo-font` and `expo-splash-screen` libraries.

```sh
npx expo install expo-font expo-splash-screen
```

The [`expo-splash-screen`](/versions/latest/sdk/splash-screen) library provides `SplashScreen` component that you can use to prevent rendering the app until the font is loaded and ready.

Map the font file using the `useFonts` hook in a top-level component such as the root layout (**src/app/_layout.tsx**) file in your project:

```tsx
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import {useEffect} from 'react';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [loaded, error] = useFonts({
    'Inter-Black': require('./assets/fonts/Inter-Black.otf'),
  });

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error]);

  if (!loaded && !error) {
    return null;
  }

  return (
    ...
  )
}
```

Use the font on the `<Text>` by using `fontFamily` style prop in a React component:

```tsx
<Text style={{ fontFamily: 'Inter-Black' }}>Inter Black</Text>
```

## Use Google Fonts

Expo has first-class support for all fonts listed in [Google Fonts](https://fonts.google.com/). They are available using [`@expo-google-fonts`](https://github.com/expo/google-fonts) library. With any of the font package from this library, you can quickly integrate that font and its variants.

Two ways to use a Google Font in your project:

-   Embed the installed font with [`expo-font` config plugin](/versions/latest/sdk/font#configuration-in-appjsonappconfigjs).
-   Load the installed font with [`useFonts`](/versions/latest/sdk/font#usefontsmap) hook at runtime asynchronously.

### With `expo-font` config plugin

> **Note:** Embedding a Google Font using `expo-font` config plugin has same benefits and limitations as embedding a custom font on your own. See [using a local font file with `expo-font` config plugin](/develop/user-interface/fonts#with-expo-font-config-plugin) for more information.

Install the font package. For example, to use Inter Black font, install the [`@expo-google-fonts/inter`](https://www.npmjs.com/package/@expo-google-fonts/inter) package with the command below.

```sh
npx expo install expo-font @expo-google-fonts/inter
```

Add the config plugin to your [app config](/versions/latest/config/app#plugins) file. The configuration must contain the path to the font file using [`fonts`](/versions/latest/sdk/font#configurable-properties) property which takes an array of one or more font files. The path to the font file is defined from the font package inside the `node_modules` directory. For example, if you have a font package named `@expo-google-fonts/inter`, then the name of the file is **Inter_900Black.ttf**.

```json
{
  "plugins": [
    [
      "expo-font",
      {
        "fonts": ["node_modules/@expo-google-fonts/inter/900Black/Inter_900Black.ttf"]
      }
    ]
  ]
}
```

After embedding the font with the config plugin, create a [new development build](/develop/development-builds/create-a-build) and install it on your device or Android Emulator or iOS Simulator.

On Android, you can use the font file name. For example, `Inter_900Black`. On iOS, use the font and its weight name ([PostScript name](/develop/user-interface/fonts#what-is-postscript-name-of-a-font)). The example below demonstrates how to use [`Platform`](https://reactnative.dev/docs/platform-specific-code#platform-module) to select the correct font family name for each platform:

```tsx
import { Platform } from 'react-native';

// Inside a React component:
<Text
  style={{
    fontFamily: Platform.select({
      android: 'Inter_900Black',
      ios: 'Inter-Black',
    }),
  }}>
  Inter Black
</Text>
```

### With `useFonts` hook

> **Note:** Loading a Google Font using `useFonts` hook has same benefits and limitations as embedding a custom font on your own. See [using a local font file with `useFonts` hook](/develop/user-interface/fonts#with-usefonts-hook) for more information.

Each google Fonts package provides the `useFonts` hook to load the fonts asynchronously. This hook keeps track of the loading state and loads the font when an app is initialized. The font package also imports the font file so you don't have to explicitly import it.

Install the Google Fonts package, `expo-font` and `expo-splash-screen` libraries.

```sh
npx expo install @expo-google-fonts/inter expo-font expo-splash-screen
```

The [`expo-splash-screen`](/versions/latest/sdk/splash-screen) library provides `SplashScreen` component that you can use to prevent rendering the app until the font is loaded and ready.

After installing the font package, map the font using the `useFonts` hook in a top-level component such as the root layout (**src/app/_layout.tsx**) file in your project:

```tsx
// Rest of the import statements
import { Inter_900Black, useFonts } from '@expo-google-fonts/inter';
import * as SplashScreen from 'expo-splash-screen';
import {useEffect} from 'react';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [loaded, error] = useFonts({
    Inter_900Black,
  });

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error]);

  if (!loaded && !error) {
    return null;
  }

  return (
    ...
  )
}
```

Use the font on the `<Text>` by using `fontFamily` style prop in a React component:

```tsx
<Text style={{ fontFamily: 'Inter_900Black' }}>Inter Black</Text>
```

## Additional information

### Minimal example

[expo-font usage](/versions/latest/sdk/font#usage) — expo-font — See usage section in Expo Fonts API reference for a minimal example of using a custom font.

### Beyond OTF and TTF

If your font is in format other than OTF or TTF, you have to [customize the Metro bundler configuration to include it as an extra asset](/guides/customizing-metro#adding-more-file-extensions-to-assetexts) for it to work. In some cases, rendering a font format that a platform doesn't support may cause your app to crash.

For reference, the following table provides the list formats that work on each native platform:

| Format | Android | iOS | Web |
| --- | --- | --- | --- |
| bdf | ✗ | ✗ | ✗ |
| dfont | ✓ | ✗ | ✗ |
| eot | ✗ | ✗ | ✓ |
| fon | ✗ | ✗ | ✗ |
| otf | ✓ | ✓ | ✓ |
| ps | ✗ | ✗ | ✗ |
| svg | ✗ | ✗ | ✓ |
| ttc | ✗ | ✗ | ✗ |
| ttf | ✓ | ✓ | ✓ |
| woff | ✗ | ✓ | ✓ |
| woff2 | ✗ | ✓ | ✓ |

### Platform built-in fonts

If you don't want to use a custom font by specifying a `fontFamily`, platform's default font will be used. Each platform has a set of built in fonts. On Android, the default font is Roboto. On iOS, it's SF Pro.

A platform's default font is usually easy-to-read. However, don't be surprised when the system default font is changed to use another font that is not easy to read. In this case, use your custom font so you have precise control over what the user will see.

### Handle `@expo/vector-icons` initial load

When the icons from `@expo/vector-icons` library load for the first time, they appear as invisible icons in your app. Once they load, they're cached for all the app's subsequent usage. To avoid showing invisible icons on your app's first load, preload during the initial loading screen with [`useFonts`](/versions/latest/sdk/font#usefontsmap). For example:

```tsx
import { useFonts } from 'expo-font';
import Ionicons from '@expo/vector-icons/Ionicons';

export default function RootLayout() {
  useFonts([require('./assets/fonts/Inter-Black.otf', Ionicons.font)]);

  return (
    ...
  )
}
```

Now, you can use any icon from the `Ionicons` library in a React component:

```tsx
<Ionicons name="checkmark-circle" size={32} color="green" />
```

[Icons](/guides/icons) — Learn how to use various types of icons in your Expo app, including vector icons, custom icon fonts, icon images, and icon buttons.

### Loading a remote font directly from the web

> **If you're loading remote fonts, make sure they are being served from an origin with CORS properly configured**. If you don't do this, your remote font might not load properly on the web platform.

Loading fonts from a local asset is the safest way to load a font in your app. When including fonts as local assets, after you submit your app to the app stores, these fonts are bundled with the app download and will be available immediately. You don't have to worry about CORS or other potential issues.

However, loading a font file directly from web is done by replacing the `require('./assets/fonts/FontName.otf')` with the URL of your font as shown in the example below.

```tsx
import { useFonts } from 'expo-font';
import { Text, View, StyleSheet } from 'react-native';

export default function App() {
  const [loaded, error] = useFonts({
    'Inter-SemiBoldItalic': 'https://rsms.me/inter/font-files/Inter-SemiBoldItalic.otf?v=3.12',
  });

  if (!loaded || !error) {
    return null;
  }

  return (
    <View style={styles.container}>
      <Text style={{ fontFamily: 'Inter-SemiBoldItalic', fontSize: 30 }}>Inter SemiBoldItalic</Text>
      <Text style={{ fontSize: 30 }}>Platform Default</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
```

---

---
modificationDate: February 26, 2026
title: Assets
description: Learn about using static assets in your project, including images, videos, sounds, database files, and fonts.
---

# Assets

Learn about using static assets in your project, including images, videos, sounds, database files, and fonts.

A **static asset** is a file that is bundled with your app's binary (native binary). This file type is not part of your app's JavaScript bundle which contain your app's code. Common types of static assets include images, videos, sounds, database files for SQLite, and fonts. These assets can be served locally from your project or remotely over the network.

This guide covers different ways you can load and use static assets in your project and also provides additional information on how to optimize and minify assets.

## Serve an asset locally

When an asset is stored in your project's file system, it can be embedded in your app binary at build time or loaded at runtime. You can import it like a JavaScript module using `require` or `import` statements.

For example, to render an image called **example.png** in **App.js**, you can use `require` to import the image from the project's **assets/images** directory and pass it to the `<Image>` component:

```tsx
<Image source={require('./assets/images/example.png')} />
```

In the above example, the bundler reads the imported image's metadata and automatically provides the width and height. For more information, see [Static Image Resources](https://reactnative.dev/docs/images#static-image-resources).

Libraries such as `expo-image` and `expo-file-system` work similarly to the `<Image>` component with local assets.

### How are assets served locally

Locally stored assets are served over HTTP in development. They are automatically bundled into your app binary at the build time for production apps and served from disk on a device.

### Load an asset at build time with `expo-asset` config plugin

To load an asset at build time, you can use the [config plugin](/versions/latest/sdk/asset#example-appjson-with-config-plugin) from the `expo-asset` library. This plugin will embed the asset file in your native project.

Install the `expo-asset` library.

```sh
npx expo install expo-asset
```

Add the config plugin to your project's [app config](/versions/latest/config/app#plugins) file. The configuration must contain the path to the asset file using [`assets`](/versions/latest/sdk/asset#configurable-properties) property which takes an array of one or more files or directories to link to the native project.

The path to each asset file must be relative to your project's root since the app config file is located in the project's root directory.

```json
{
  "expo": {
    "plugins": [
      [
        "expo-asset",
        {
          "assets": ["./assets/images/example.png"]
        }
      ]
    ]
  }
}
```

After embedding the asset with the config plugin, [create a new development build](/develop/development-builds/create-a-build). Now, you can import and use the asset in your project without using a `require` or an `import` statement.

For example, the **example.png** is linked by the above config plugin. You can directly import it into your component and use its resource name as the URI. Note that when rendering assets without using `require`, you need to explicitly provide a width / height.

```tsx
import { Image } from 'expo-image';
...

export default function HomeScreen() {
  return <Image source={{ uri: 'example' }} style={{ width: 100, height: 100 }} />;
}
```

> Different file formats are supported with the `expo-asset` config plugin. For more information on these formats, see [Assets API reference](/versions/latest/sdk/asset#configurable-properties). If you don't see a file format supported by the config plugin, you can use the [`useAssets`](/develop/user-interface/assets#load-an-asset-at-runtime-with-useassets-hook) hook to load the asset at runtime.

### Load an asset at runtime with `useAssets` hook

The `useAssets` hook from `expo-asset` library allows loading assets asynchronously. This hook downloads and stores an asset locally and after the asset is loaded, it returns a list of that asset's instances.

Install the `expo-asset` library.

```sh
npx expo install expo-asset
```

Import the [`useAssets`](/versions/latest/sdk/asset#useassetsmoduleids) hook from the `expo-asset` library in your screen component:

```tsx
import { useAssets } from 'expo-asset';

export default function HomeScreen() {
  const [assets, error] = useAssets([
    require('path/to/example-1.jpg'),
    require('path/to/example-2.png'),
  ]);

  return assets ? <Image source={assets[0]} /> : null;
}
```

## Serve an asset remotely

When an asset is served remotely, it is not bundled into the app binary at build time. You can use the URL of the asset resource in your project if it is hosted remotely. For example, pass the URL to the `<Image>` component to render a remote image:

```jsx
import { Image } from 'expo-image';
...

function App() {
  return (
    <Image source={{ uri: 'https://example.com/logo.png' }} style={{ width: 50, height: 50 }} />
  );
}
```

There is no guarantee about the availability of images served remotely using a web URL because an internet connection may not be available, or the asset might be removed.

Additionally, loading assets remotely also requires you to provide an asset's metadata. In the above example, since the bundler cannot retrieve the image's width and height, those values are passed explicitly to the `<Image>` component. If you don't, the image will default to 0px by 0px.

## Additional information

### Manual optimization methods

#### Images

You can compress images using the following:

-   [`guetzli`](https://github.com/google/guetzli)
-   [`pngcrush`](https://pmt.sourceforge.io/pngcrush/)
-   [`optipng`](http://optipng.sourceforge.net/)

Some image optimizers are lossless. They re-encode your image to be smaller without any change or loss in the pixels displayed. When you need each pixel to be untouched from the original image, a lossless optimizer and a lossless image format like PNG are a good choice.

Other image optimizers are lossy. The optimized image differs from the original image. Often, lossy optimizers are more efficient because they discard visual information that reduces file size while making the image look nearly identical to humans. Tools like `imagemagick` can use comparison algorithms like [SSIM](https://en.wikipedia.org/wiki/Structural_similarity) to show how similar two images look. It's quite common for an optimized image that is over 95% similar to the original image to be far less than 95% of the original file size.

#### Other assets

For assets like GIFs or videos, or non-code and non-image assets, it's up to you to optimize and minify those assets.

> **Note**: GIFs are a very inefficient format. Modern video codecs can produce significantly smaller file sizes with better quality.

### Fonts

See [Add a custom font](/develop/user-interface/fonts#add-a-custom-font) for more information on how to add a custom font to your app.

---

---
modificationDate: February 26, 2026
title: Color themes
description: Learn how to support light and dark modes in your app.
---

# Color themes

Learn how to support light and dark modes in your app.

It's common for apps to support light and dark color schemes. Here is an example of how supporting both modes looks in an Expo project:

## Configuration

> For Android and iOS projects, additional configuration is required to support switching between light and dark mode. For web, no additional configuration is required.

To configure supported appearance styles, you can use the [`userInterfaceStyle`](/versions/latest/config/app#userinterfacestyle) property in your project's [app config](/versions/latest/config/app). By default, this property is set to `automatic` when you create a new project with the [default template](/get-started/create-a-project).

Here is an example configuration:

```json
{
  "expo": {
    "userInterfaceStyle": "automatic"
  }
}
```

You can also configure `userInterfaceStyle` property for a specific platforms by setting either [`android.userInterfaceStyle`](/versions/latest/config/app#userinterfacestyle-2) or [`ios.userInterfaceStyle`](/versions/latest/config/app#userinterfacestyle-1) to the preferred value.

> The app will default to the `light` style if this property is absent.

When you are creating a development build, you have to install [`expo-system-ui`](/versions/latest/sdk/system-ui#installation) to support the appearance styles for Android. Otherwise, the `userInterfaceStyle` property is ignored.

```sh
npx expo install expo-system-ui
```

If the project is misconfigured and doesn't have `expo-system-ui` installed, the following warning will be shown in the terminal:

```sh
» android: userInterfaceStyle: Install expo-system-ui in your project to enable this feature.
```

You can also use the following command to check if the project is misconfigured:

```sh
npx expo config --type introspect
```

Using bare React Native app?

#### Android

Ensure that the `uiMode` flag is present on your `MainActivity` (and any other activities where this behavior is desired) in **AndroidManifest.xml**:

```xml
<activity android:configChanges="keyboard|keyboardHidden|orientation|screenSize|uiMode">
```

Implement the `onConfigurationChanged` method in **MainActivity.java**:

```java
import android.content.Intent;
import android.content.res.Configuration;
public class MainActivity extends ReactActivity {
  ...

  @Override
  public void onConfigurationChanged(Configuration newConfig) {
    super.onConfigurationChanged(newConfig);
    Intent intent = new Intent("onConfigurationChanged");
    intent.putExtra("newConfig", newConfig);
    sendBroadcast(intent);
  }
  ...
}
```

#### iOS

You can configure supported styles with the [`UIUserInterfaceStyle`](https://developer.apple.com/documentation/bundleresources/information_property_list/uiuserinterfacestyle) key in your app **Info.plist**. Use `Automatic` to support both light and dark modes.

### Supported appearance styles

The `userInterfaceStyle` property supports the following values:

-   `automatic`: Follow system appearance settings and notify about any change the user makes.
-   `light`: Restrict the app to support light theme only.
-   `dark`: Restrict the app to support dark theme only.

## Detect the color scheme

To detect the color scheme in your project, use `Appearance` or `useColorScheme` from `react-native`:

```tsx
import { Appearance, useColorScheme } from 'react-native';
```

Then, you can use `useColorScheme()` hook as shown below:

```tsx
function MyComponent() {
  let colorScheme = useColorScheme();

  if (colorScheme === 'dark') {
    // render some dark thing
  } else {
    // render some light thing
  }
}
```

In some cases, you will find it helpful to get the current color scheme imperatively with [`Appearance.getColorScheme()` or listen to changes with `Appearance.addChangeListener()`](https://reactnative.dev/docs/appearance).

## Additional information

### Minimal example

```tsx
import { Text, StyleSheet, View, useColorScheme } from 'react-native';
import { StatusBar } from 'expo-status-bar';

export default function App() {
  const colorScheme = useColorScheme();

  const themeTextStyle = colorScheme === 'light' ? styles.lightThemeText : styles.darkThemeText;
  const themeContainerStyle =
    colorScheme === 'light' ? styles.lightContainer : styles.darkContainer;

  return (
    <View style={[styles.container, themeContainerStyle]}>
      <Text style={[styles.text, themeTextStyle]}>Color scheme: {colorScheme}</Text>
      <StatusBar />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontSize: 20,
  },
  lightContainer: {
    backgroundColor: '#d0d0c0',
  },
  darkContainer: {
    backgroundColor: '#242c40',
  },
  lightThemeText: {
    color: '#242c40',
  },
  darkThemeText: {
    color: '#d0d0c0',
  },
});
```

### Tips

While you are developing your project, you can change your simulator's or device's appearance by using the following shortcuts:

-   If using an Android Emulator, you can run `adb shell "cmd uimode night yes"` to enable dark mode, and `adb shell "cmd uimode night no"` to disable dark mode.
-   If using a physical Android device or an Android Emulator, you can toggle the system dark mode setting in the device's settings.
-   If working with an iOS emulator locally, you can use the Cmd ⌘ + Shift + a shortcut to toggle between light and dark modes.

---

---
modificationDate: December 18, 2024
title: Animation
description: Learn how to integrate React Native animations and use it in your Expo project.
---

# Animation

Learn how to integrate React Native animations and use it in your Expo project.

Animations are a great way to enhance and provide a better user experience. In your Expo projects, you can use the [Animated API](https://reactnative.dev/docs/next/animations) from React Native. However, if you want to use more advanced animations with better performance, you can use the [`react-native-reanimated`](https://docs.swmansion.com/react-native-reanimated/) library. It provides an API that simplifies the process of creating smooth, powerful, and maintainable animations.

## Installation

You can skip installing `react-native-reanimated` if you have created a project using [the default template](/get-started/create-a-project). This library is already installed. Otherwise, install it by running the following command:

```sh
npx expo install react-native-reanimated
```

## Usage

### Minimal example

The following example shows how to use the `react-native-reanimated` library to create a simple animation. For more information on the API and advanced usage, see [`react-native-reanimated` documentation](https://docs.swmansion.com/react-native-reanimated/docs/fundamentals/your-first-animation).

```tsx
import Animated, {
  useSharedValue,
  withTiming,
  useAnimatedStyle,
  Easing,
} from 'react-native-reanimated';
import { View, Button, StyleSheet } from 'react-native';

export default function AnimatedStyleUpdateExample() {
  const randomWidth = useSharedValue(10);

  const config = {
    duration: 500,
    easing: Easing.bezier(0.5, 0.01, 0, 1),
  };

  const style = useAnimatedStyle(() => {
    return {
      width: withTiming(randomWidth.value, config),
    };
  });

  return (
    <View style={styles.container}>
      <Animated.View style={[styles.box, style]} />
      <Button
        title="toggle"
        onPress={() => {
          randomWidth.value = Math.random() * 350;
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  box: {
    width: 100,
    height: 80,
    backgroundColor: 'black',
    margin: 30,
  },
});
```

## Other animation libraries

You can use other animation packages such as [Moti](https://moti.fyi/) in your Expo project. It works on Android, iOS, and web.

---

---
modificationDate: March 09, 2026
title: Store data
description: Learn about different libraries available to store data in your Expo project.
---

# Store data

Learn about different libraries available to store data in your Expo project.

Storing data can be essential to the features implemented in your mobile app. There are different ways to save data in your Expo project depending on the type of data you want to store and the security requirements of your app. This page lists a variety of libraries to help you decide which solution is best for your project.

## Expo SecureStore

`expo-secure-store` provides a way to encrypt and securely store key-value pairs locally on the device.

[Expo SecureStore API reference](/versions/latest/sdk/securestore) — For more information on how to install and use expo-secure-store, see its API documentation.

## Expo FileSystem

`expo-file-system` provides access to a file system stored locally on the device. Within Expo Go, each project has a separate file system and no access to other Expo projects' files. However, it can save content shared by other projects to the local filesystem and share local files with other projects. It is also capable of uploading and downloading files from network URLs.

[Expo FileSystem API reference](/versions/latest/sdk/filesystem) — For more information on how to install and use expo-file-system, see its API documentation.

## Expo SQLite

`expo-sqlite` package gives your app access to a database that can be queried through a WebSQL-like API. The database is persisted across restarts of your app. You can use it for importing an existing database, opening databases, creating tables, inserting items, querying and displaying results, and using prepared statements.

[Expo SQLite API reference](/versions/latest/sdk/sqlite) — For more information on how to install and use expo-sqlite, see its API documentation.

## Async Storage

[Async Storage](https://react-native-async-storage.github.io/2.0/integrations/expo/) is an asynchronous, unencrypted, persistent key-value storage for React Native apps. It has a simple API and is a good choice for storing small amounts of data. It is also a good choice for storing data that does not need encryption, such as user preferences or app state.

[Async Storage documentation](https://react-native-async-storage.github.io/2.0/api/usage/) — For more information on how to install and use Async Storage, see its documentation.

## Other libraries

There are other libraries available for storing data for different purposes. For example, you might not need encryption in your project or are looking for a faster solution similar to Async Storage.

We recommend checking out [React Native for a list of libraries](https://reactnative.directory/?search=storage) to help you store your project's data.

---

---
modificationDate: December 12, 2024
title: Next steps
description: A list of useful resources to learn more about implementing navigation and UI in your app.
---

# Next steps

A list of useful resources to learn more about implementing navigation and UI in your app.

[Use TypeScript](/guides/typescript) — An in-depth guide on configuring an Expo project with TypeScript or migrating an existing JavaScript project.

[Icons](/guides/icons) — Learn how to use various types of icons in your Expo app, including vector icons, custom icon fonts, icon images, and icon buttons.

[ESLint and Prettier](/guides/using-eslint) — A guide on configuring ESLint and Prettier to format Expo projects.

---

---
modificationDate: January 29, 2026
title: Introduction to development builds
description: Why use development builds and how to get started.
---

# Introduction to development builds

Why use development builds and how to get started.

**Development build** is the term that we use for a "Debug" build of an app that includes the [`expo-dev-client`](/versions/latest/sdk/dev-client) library. This library augments the built-in React Native development tooling with additional capabilities, such as support for inspecting network requests and a "launcher" UI that lets you switch between different development servers (such as between a server running on your machine or a teammate's machine) and deployments of your app (such as published updates with EAS Update).

Difference between Expo Go and development builds

[Expo Go](https://expo.dev/go) is a playground app for students and learners to get started quickly. It comes with a fixed set of native libraries built in, so you can write JavaScript code and see changes instantly without building a native app yourself. A development build is a fully featured development environment for working on your production-grade Expo apps.

Native app and JavaScript bundle

The **native app** is what you install on your device. Expo Go is a pre-built native app that works like a playground — it can't be changed after you install it. To add new native libraries or change things like your app name and icon, you need to build your own native app (a development build).

The **JavaScript bundle (`npx expo start`)** is where your app's UI code and business logic are. In production apps, there is one **main.js** bundle that is shipped with the app itself. In development, this JS bundle is live reloaded from your local machine. The main role of React Native is to provide a way for the JavaScript code to access the native APIs (Image, Camera, Notifications, and more). However, only APIs and libraries that were bundled in the **native app** can be used.

[Expo Go & Development Builds: which should you use?](https://www.youtube.com/watch?v=FdjczjkwQKE) — In this tutorial video Beto explains what each of them is, and when to choose a development build.

## Why use a development build (a.k.a what _can't_ you do in Expo Go and why)

Expo Go is a playground for students and learners to understand the basics of React Native. It's limited and not useful for building production-grade projects, so most apps will convert to using development builds. It helps to know exactly what is _impossible_ in Expo Go and _why_, so you can make an informed decision on when and why to make this move.

Use libraries with native code that aren't in Expo Go

Consider [`react-native-webview`](/versions/latest/sdk/webview) as an example, a library that contains native code, but [is included in Expo Go](https://github.com/expo/expo/blob/main/apps/expo-go/package.json#L23). When you run `npx expo install react-native-webview` command in your project, it will install the library in your **node_modules** directory, which includes both the JS code and the native code. But the JS bundle you are building _only_ uses the JS code. Then, your JS bundle gets uploaded to Expo Go, and it interacts with the native code that was already bundled with the app.

Instead, when you try to use a library that is not included, for example, [`react-native-firebase`](/guides/using-firebase#using-react-native-firebase), then you can use the JS code and hot reload the new bundle into Expo Go but it will immediately error because the JS code tries to call the native code from the React Native Firebase package that does not exist in Expo Go. There is no way to get the native code into the Expo Go app unless it was already included in the bundle that was uploaded to the app stores.

Test changes in app icon, name, splash screen

If you're developing your app in Expo Go only, you can build a store version that will use your provided values and images; it just won't be possible to test it in Expo Go.

These native assets are shipped with the native bundle and are immutable once the app is installed. The Expo Go app does show a splash screen, which is your app icon on a solid color background. This is a dev-only emulation to view how the splash screen will probably look. However, it is limited, for example, you cannot test `SplashScreen.setOptions` to animate the splash screen.

Remote push notifications

While [in-app notifications](/versions/latest/sdk/notifications) are available in Expo Go, remote push notifications (that is, sending a push notification from a server to the app) are not. This is because a push notification service should be tied to your own push notification certificates, and while it is possible to make it work in Expo Go, it often causes confusion for production builds. It is recommended to test remote push notifications in development builds so you can ensure parity in behavior between development and production.

Implementing App/Universal links

Both [Android App Links](/linking/android-app-links) and [iOS Universal Links](/linking/ios-universal-links) require a two-way association between the native app and the website. In particular, it requires the native app to include the linked website's URL. This is impossible with Expo Go due to the aforementioned native code immutability.

Open projects using older SDKs (iOS device only)

Expo Go can only support one SDK version at a time. When a new SDK version is released, Expo Go is updated to support the newer version, and this will be the only version of Expo Go available to install from the stores.

If you're developing on an Android Device, Android Emulator, or iOS Simulator, a compatible version of Expo Go can be [downloaded and installed](https://expo.dev/go). The only platform where this is impossible is iPhone devices because Apple does not support side-loading older versions of apps.

[Expo Go to development build](/develop/development-builds/expo-go-to-dev-build) — Learn how to migrate an existing Expo Go project to using development builds

[Local app development](/guides/local-app-development) — How to build a development client on your local machine

[Development builds on EAS](/develop/development-builds/create-a-build) — How to build a development client on EAS

---

---
modificationDate: February 17, 2026
title: Switch from Expo Go to a development build
description: How to switch from your Expo Go project to use development builds.
---

# Switch from Expo Go to a development build

How to switch from your Expo Go project to use development builds.

To switch from Expo Go to a development build, you'll need to follow the steps below:

## Install the `expo-dev-client`

The Expo Dev Client library includes the launcher UI (shown in the screenshots below), dev menu, extensions to test over-the-air updates, and more. The Expo Go app has the dev menu built in, and that's why you need to install it separately for a development build.

```sh
npx expo install expo-dev-client
```

When you run a development build it will look like this, only with your app name and icon included rather than "Microfoam". The launcher UI is pictured in iOS on the left and Android on the right. In between, you can see an app running inside of the development build, with the customizable developer menu open.

> We recommend using the `expo-dev-client` for the best development experience, but it is possible to use development builds without installing this library. If not using the dev client, in [Step 3](/develop/development-builds/expo-go-to-dev-build#start-the-dev-client), start the bundler with `--dev-client`. Otherwise, it will default to opening in Expo Go.

## Build your native app

With Expo Go, you only needed to build the JavaScript bundle, but with development builds you also need to compile the native app. With Expo, there are two parts to building your native app:

1.  Generate the native **android** and/or **ios** directories ([read more](/develop/development-builds/expo-go-to-dev-build#prebuild) on when and how you'll need to do this)
2.  Use native build tools to compile the native app(s)

Once you've built your native app, you won't need to build it again unless you add or update a library with native code, or change any native code or configuration, such as the app name.

> The **android** and **ios** directories are automatically added to **.gitignore** when you create a new project, so they won't be checked into Git. This ensures you can always regenerate the code locally or on CI with [CNG](/workflow/continuous-native-generation) when needed and never have to edit native code manually.

### Option 1: Build on your local machine

To build a native app on your local machine, follow the setup your environment guides for [Android](/workflow/android-studio-emulator) and [iOS](/workflow/ios-simulator) platforms. This involves setting up and configuring native build tools like Android Studio for Android and Xcode for iOS.

Once you have everything set up, run the following command:

```sh
npx expo run:android
```

By default, this will build and install the app on an Android Emulator/iOS Simulator. If you need to run the build on your phone, plug it into your computer (on Android, select trust device and allow USB debugging if prompted, and on iOS, enable [developer mode](/get-started/set-up-your-environment?mode=development-build&buildEnv=local&platform=ios&device=physical#plug-in-your-device-via-usb-and-enable-developer-mode)) and run the above commands with the `--device` flag.

### Option 2: Build on EAS

Building on EAS servers is useful when:

-   You can't or don't want to set up your local development environment
-   You want to build an iOS app but don't own a Mac
-   You want to share the development builds with your team

[Build on EAS](/develop/development-builds/create-a-build) — How to create your Development Build on EAS

## Start the bundler

After building locally, `npx expo run:android|ios` will start the bundler automatically. But if you closed the bundler or are working on a dev client you built earlier, (re)start the Metro bundler with:

```sh
npx expo start
```

When your project has `expo-dev-client` installed, the bundler will print out **Using development build**, and the QR code it shows will link into the development build you created instead of Expo Go.

## Prebuild

[**Prebuild**](/workflow/continuous-native-generation#prebuild) is a concept unique to Expo projects. It refers to the process of generating the **android** and **ios** directories based on your local configuration and properties.

### When should you run prebuild

You will need to run prebuild locally if you are building via `npx expo run:android|ios`, and change any native dependencies or configuration, such as:

-   Installing or updating a library containing native code
-   Changing [app config](/workflow/configuration)(`app.json`)
-   Upgrading your Expo SDK version

In these cases, you'll want to rebuild the native directories with:

```sh
npx expo prebuild --clean
```

Then, rebuild your app with the updated native code, with:

```sh
npx expo run:android
```

### When you don't need to run prebuild

All Expo build tools (`npx expo run:android|ios` and `eas build`) will **prebuild** automatically if no existing native folders are found. This means that there is no need to run prebuild manually when you're running `npx expo run:android|ios` for the first time or `eas build`.

[Continuous Native Generation (CNG)](/workflow/continuous-native-generation) — Learn about the philosophy and benefits of Continuous Native Generation (CNG) and Prebuild

---

---
modificationDate: March 06, 2026
title: Create a development build on EAS
description: Learn how to create development builds for a project.
---

# Create a development build on EAS

Learn how to create development builds for a project.

When you create a new Expo app with `npx create-expo-app`, you start off with a project where you update the JavaScript code on your local machine and view the changes in the Expo Go app. A **development build** is essentially **your own version of Expo Go** where you are free to use any native libraries and change any native config. In this guide, you will learn how to convert your project that runs on Expo Go into a development build, which will make the native side of your app fully customizable.

[How to create a development build](https://www.youtube.com/watch?v=uQCE9zl3dXU) — Configure and create a development build for your Expo project using EAS Build.

## Prerequisites

The instructions assume you already have an existing Expo project that runs on Expo Go.

The requirements for building the native app depend on which platform you are using, which platform you are building for, and whether you want to build on EAS or on your local machine.

Build on EAS

This is the easiest way to build your native app, as it requires no native build tools on your side. The builds happen on the EAS servers, which makes it possible to trigger iOS builds from non-macOS platforms.

|  | Android | iOS Simulator | iPhone device |
| --- | --- | --- | --- |
| **macOS** | ✓ | ✓ | ✓ (\*) |
| **Windows** | ✓ | ✓ | ✓ (\*) |
| **Linux** | ✓ | ✓ | ✓ (\*) |

(\*) All builds that run on an iPhone device require a paid [Apple Developer](https://developer.apple.com) account for build signing.

Build locally using the EAS CLI

Any EAS CLI command can be built on your local machine with the `--local` flag. This requires your local [development environment](https://reactnative.dev/docs/set-up-your-environment?os=macos&platform=ios) to be set up with native build tools. Read more about [local app development](/build-reference/local-builds).

|  | Android | iOS Simulator | iPhone device |
| --- | --- | --- | --- |
| **macOS** | ✓ | ✓ | ✓ (\*) |
| **Windows** | ✓ (\*\*) | ✗ | ✗ |
| **Linux** | ✓ | ✗ | ✗ |

(\*) All builds that run on an iPhone device require a paid [Apple Developer](https://developer.apple.com) account for build signing.

(\*\*) No first-class support, but possible with [WSL](http://expo.fyi/wsl.md).

Build locally without EAS

To build locally without EAS requires your local [development environment](https://reactnative.dev/docs/set-up-your-environment?os=macos&platform=ios) to be set up with native build tools. This is the only way to test your iOS build on an iPhone device without a paid Apple Developer Account (only possible on macOS). Read more about [local app compilation](/guides/local-app-development#local-app-compilation) and see the [Expo Go to Development Build](/develop/development-builds/expo-go-to-dev-build) guide.

|  | Android | iOS Simulator | iPhone device |
| --- | --- | --- | --- |
| **macOS** | ✓ | ✓ | ✓ |
| **Windows** | ✓ | ✗ | ✗ |
| **Linux** | ✓ | ✗ | ✗ |

## Get started

For detailed, step-by-step instructions, see our [EAS Tutorial](/tutorial/eas/introduction). Available also as a [tutorial series](https://www.youtube.com/playlist?list=PLsXDmrmFV_AS14tZCBin6m9NIS_VCUKe2) on YouTube.

### Install expo-dev-client

```sh
npx expo install expo-dev-client
```

Are you using this library in a existing (bare) React Native apps?

Apps that don't use [Continuous Native Generation](/workflow/continuous-native-generation) or are created with `npx react-native`, require further configuration after installing this library. See steps 1 and 2 from [Install `expo-dev-client` in an existing React Native app](/bare/install-dev-builds-in-bare).

### Build the native app (Android)

Prerequisites

3 requirements

1.

Expo account

Sign up for an [Expo](https://expo.dev/signup) account, if you haven't already.

2.

EAS CLI

The [EAS CLI](/build/setup#install-the-latest-eas-cli) installed and logged in.

```sh
npm install -g eas-cli && eas login
```

3.

An Android Emulator (optional)

An [Android Emulator](/workflow/android-studio-emulator) is optional if you want to test your app on an emulator.

```sh
eas build --platform android --profile development
```

Read more about [Android builds on EAS](/tutorial/eas/android-development-build).

### Build the native app (iOS Simulator)

Prerequisites

3 requirements

1.

Expo account

Sign up for an [Expo](https://expo.dev/signup) account, if you haven't already.

2.

EAS CLI

The [EAS CLI](/build/setup#install-the-latest-eas-cli) installed and logged in.

```sh
npm install -g eas-cli && eas login
```

3.

macOS with iOS Simulator installed

iOS Simulators are available only on macOS. Make sure you have the [iOS Simulator](/workflow/ios-simulator) installed.

Edit `development` profile in **eas.json** and set the [`simulator`](/eas/json#simulator) option to `true` (you have to create a separate profile for simulator builds if you also want to create iOS device builds for this project).

```json
{
  "build": {
    "development": {
      "ios": {
        "simulator": true
      }
    }
  }
}
```

```sh
eas build --platform ios --profile development
```

iOS Simulator builds can only be installed on simulators and not on real devices.

Read more about [iOS Simulator builds on EAS](/tutorial/eas/ios-development-build-for-simulators).

### Build the native app (iOS device)

Prerequisites

3 requirements

1.

Expo account

Sign up for an [Expo](https://expo.dev/signup) account, if you haven't already.

2.

EAS CLI

The [EAS CLI](/build/setup#install-the-latest-eas-cli) installed and logged in.

```sh
npm install -g eas-cli && eas login
```

3.

Apple Developer account

A paid [Apple Developer](https://developer.apple.com/) account for creating [signing credentials](/app-signing/managed-credentials#generating-app-signing-credentials) so the app could be installed on an iOS device.

```sh
eas build --platform ios --profile development
```

iOS device builds can only be installed on iPhone devices and not on iOS Simulators.

Read more about [iOS device builds on EAS](/tutorial/eas/ios-development-build-for-devices).

### Install the app

You'll need to install the native app on your device, emulator, or simulator.

#### When building on EAS

If you create your development build on EAS, the CLI will prompt you to install the app after the build is finished. You can also install previous builds from the [expo.dev](https://expo.dev/) dashboard or using [Expo Orbit](https://expo.dev/orbit).

#### When building locally using EAS CLI

When building locally the output of the build will be an archive. You may drag and drop this on your Android Emulator/iOS Simulator to install it, or use [Expo Orbit](https://expo.dev/orbit) to install a build from your local machine.

### Start the bundler

The development client built in **step 2** is the native side of your app (basically your own version of Expo Go). To continue developing, you'll also want to start the JavaScript bundler.

Depending on how you built the app, this may already be running, but if you close the process for any reason, there is no need to rebuild your development client. Simply restart the JavaScript bundler with:

```sh
npx expo start
```

This is the same command you would have used with Expo Go. It detects whether your project has `expo-dev-client` installed, in which case it will default to targeting your development build instead of Expo Go.

## Video walkthroughs

["EAS Tutorial Series"](https://www.youtube.com/playlist?list=PLsXDmrmFV_AS14tZCBin6m9NIS_VCUKe2) — A course on YouTube: learn how to speed up your development with Expo Application Services.

["Async Office Hours: How to make a development build with EAS Build"](https://www.youtube.com/watch?v=LUFHXsBcW6w) — Learn how to make a development build with EAS Build in this video tutorial hosted by Developer Success Engineer: Keith Kurak.

---

---
modificationDate: August 26, 2025
title: Use a development build
description: Learn how to use development builds for a project.
---

# Use a development build

Learn how to use development builds for a project.

Usually, creating a new native build from scratch takes long enough that you'll be tempted to switch tasks and lose your focus. However, with the development build installed on your device or an emulator/simulator, you won't have to wait for the native build process until you [change the underlying native code](/develop/development-builds/use-development-builds#rebuild-a-development-build) that powers your app.

## Start the development server

To start developing, run the following command to start the development server:

```sh
npx expo start
```

To open the project inside your development client:

-   Press a or i keys to open your project on an Android Emulator or an iOS Simulator.
-   On a physical device, scan the QR code from your system's camera or a QR code reader to open the project on your device.

## The launcher screen

If you launch the development build from your device's Home screen, you will see your launcher screen, which looks similar to the following:

If a bundler is detected on your local network, or if you have signed in to an Expo account in both Expo CLI and your development build, you can connect to it directly from this screen. Otherwise, you can connect by scanning the QR code displayed by the Expo CLI.

## Rebuild a development build

If you add a library to your project that contains native code APIs, for example, [`expo-secure-store`](/versions/latest/sdk/securestore), you will have to rebuild the development client. This is because the native code of the library is not included in the development client automatically when installing the library as a dependency on your project.

## Debug a development build

When you need to, you can access the menu by pressing Cmd ⌘ + d or Ctrl + d in Expo CLI or by shaking your phone or tablet. Here you'll be able to access all of the functions of your development build, any debugging functionality you need, or switch to a different version of your app.

See [Debugging](/debugging/runtime-issues) guide for more information.

---

---
modificationDate: March 05, 2026
title: Share a development build with your team
description: Learn how to install and share the development with your team or run it on multiple devices.
---

# Share a development build with your team

Learn how to install and share the development with your team or run it on multiple devices.

Android and iOS both offer ways to install a build of your application directly on devices. This gives you full control of putting specific builds on devices, allowing you to iterate quickly and have multiple builds of your application available for review at the same time. You can also share it with your team or run it on multiple test devices.

## Share the URL

When a development build is ready, a shareable URL is generated for your build with instructions on how to get it up and running. You can use this URL with a teammate or send it to your test device to install the build. The URL generated is unique to the build for your project.

> If you register any new iOS devices after creating a development build, you'll need to create a new development build to install it on those devices. For more information, see [internal distribution](/build/internal-distribution).

### Use the EAS dashboard

You can also direct your teammate to the build page in the EAS dashboard. From there, they can download the build artifact directly on their device.

### Use EAS CLI

Your teammate can also download and install the development build using EAS CLI. They have to make sure that they are signed from the Expo account associated with the development build and then can run the following command:

```sh
eas build:run --profile development
```

If the profile name for the development build is different from `development`, use it instead with `--profile`.

### iOS-only instructions

> If you're running iOS 16 or above and haven't yet turned on Developer Mode, you'll need to [enable it](/guides/ios-developer-mode) before you can run your build. (This doesn't apply if you're using enterprise provisioning.)

You can use `eas build:resign` to codesign an existing **.ipa** for iOS to a new ad hoc provisioning profile. This helps reduce time when distributing with your team. For example, if you want to add a new test device to an existing build, you can use this command to update the provisioning profile to include the device without rebuilding the entire app from scratch. For more information, see [Re-signing new credentials](/app-signing/app-credentials#re-signing-new-credentials).

## Next steps

[Install multiple app variants on the same device](/build-reference/variants) — Learn how to install multiple variants (development, preview, production) of an app on the same device side by side by converting app.json to app.config.js and additional configuration that is required to start the development server for each variant. — app.json — app.config.js

[Sharing pre-release versions of your app](/build/internal-distribution) — Learn more about sharing pre-release versions of your app.

---

---
modificationDate: February 26, 2026
title: Tools, workflows and extensions
description: Learn more about different tools, workflows and extensions available when working with development builds.
---

# Tools, workflows and extensions

Learn more about different tools, workflows and extensions available when working with development builds.

Development builds allow you to iterate quickly. However, you can extend the capabilities of your development build to provide a better developer experience when working in teams or customize the build to suit your needs.

## Tools

### Tunnel URLs

Sometimes, restrictive network conditions make it difficult to connect to the development server. The `npx expo start` command exposes your development server on a publicly available URL that is accessible through firewalls from around the globe. This option is helpful if you are not able to connect to your development server with the default LAN option or if you want to get feedback on your implementation while you are developing.

To get a tunneled URL, pass the [`--tunnel` flag](/more/expo-cli#tunneling) to `npx expo start` from the command line.

### Published updates

EAS CLI's `eas update` command bundles the current state of your JavaScript and asset files into an optimized "update". This update is stored on a hosting service by Expo. A development build of your app can load published updates without needing to check out a particular commit or leave a development machine running.

### Manually entering an update's URL

When a development build launches, it will expose UI to load a development server, or to "Enter URL manually". You can provide a URL manually that will launch a specific branch. The URL follows this pattern:

```text
https://u.expo.dev/[your-project-id]?channel-name=[channel-name]

# Example
https://u.expo.dev/F767ADF57-B487-4D8F-9522-85549C39F43F?channel-name=main
```

To get your project's ID, use the URL in the [app config's `expo.updates.url`](/versions/latest/config/app#url) field. To see a list of channels, run `eas channel:list`.

### Deep linking to an update's URL

You can load your app on a device that has a compatible build of your custom client by opening a URL of the form `{scheme}://expo-development-client/?url={manifestUrl}`. You'll need to pass the following parameters:

| parameter | value |
| --- | --- |
| `scheme` | URL scheme of your client (defaults to `exp+{slug}` where [`slug`](/versions/latest/config/app#slug) is the value set in the app config) |
| `manifestUrl` | URL-encoded URL of an update manifest to load. The URL will be `https://u.expo.dev/[your-project-id]?channel-name=[channel-name]` |

Example:

```text
exp+app-slug://expo-development-client/?url=https%3A%2F%2Fu.expo.dev%2F767ADF57-B487-4D8F-9522-85549C39F43F%2F%3Fchannel-name%3Dmain
```

In the example above, the `scheme` is `exp+app-slug`, and the `manifestUrl` is a project with an ID of `F767ADF57-B487-4D8F-9522-85549C39F43F` and a channel of `main`.

#### Using updates deep links in automation scenarios

When launching an update URL in a development build on an emulator or simulator using automation, such as in a CI/CD workflow, you can add the `disableOnboarding=1` query parameter to the URL to skip the onboarding screen that appears on the first launch of a development build after installation.

#### App-specific deep links

When testing deep links in your development build, such as when navigating to a specific screen in an Expo Router app or testing redirecting back to your app during an Oauth login flow, construct the URL exactly as you would if you were deep-linking into a standalone build of your app (for example, `myscheme://path/to/screen`).

Your project must be already open in the development build for an app-specific deep link to work. Cold-launching a development build with an app-specific deep link is not currently supported. Avoid using `expo-development-client` in your app-specific deep links in the path, as it is a reserved path used for launching an updated URL.

### QR codes

You can use our endpoint to generate a QR code that can be easily loaded by a development build.

Requests send to `https://qr.expo.dev/development-client` when supplied the query parameters such as `appScheme` and `url` will receive a response with an SVG image containing a QR code that can be easily scanned to load a version of your project in your development build.

| parameter | value |
| --- | --- |
| `appScheme` | URL-encoded deeplinking scheme of your development build (defaults to `exp+{slug}` where [`slug`](/versions/latest/config/app#slug) is the value set in the app config) |
| `url` | URL-encoded URL of an update manifest to load. The URL will be `https://u.expo.dev/[your-project-id]?channel-name=[channel-name]` |

Example:

```text
https://qr.expo.dev/development-client?appScheme=exp%2Bapps-slug&url=https%3A%2F%2Fu.expo.dev%2FF767ADF57-B487-4D8F-9522-85549C39F43F0%3Fchannel-name%3Dmain
```

In the example above, the `scheme` is `exp+app-slug`, and the `url` is a project with an ID of `F767ADF57-B487-4D8F-9522-85549C39F43F` and a channel of `main`.

## Example workflows

These are a few examples of workflows to help your team get the most out of your development build. If you come up with others that would be useful for other teams, [submit a PR](https://github.com/expo/expo/tree/main/CONTRIBUTING.md#-updating-documentation) to share your knowledge!

### PR previews

You can set up your CI process to publish an EAS Update whenever a pull request is updated and add a QR code that is used to view the change in a compatible development build.

See [instructions for publishing app previews on pull requests](/eas-update/github-actions#publish-previews-on-pull-requests) to implement this workflow in your project using GitHub Actions or serve as a template in your CI of choice.

## Extensions

Extensions allow you to extend your development client with additional capabilities.

### Extending the dev menu

The dev menu can be extended to include extra buttons by using the `registerDevMenuItems` API:

```tsx
import { registerDevMenuItems } from 'expo-dev-menu';

const devMenuItems = [
  {
    name: 'My Custom Button',
    callback: () => console.log('Hello world!'),
  },
];

registerDevMenuItems(devMenuItems);
```

This will create a new section in the dev menu that includes the buttons you have registered:

> Subsequent calls of `registerDevMenuItems` will override all previous entries.

### EAS Update

The EAS Update extension provides the ability to view and load published updates in your development client. To install it, you'll need the most recent publish of `expo-updates`:

```sh
npx expo install expo-dev-client expo-updates
```

#### Configure EAS Update

If you have not yet configured EAS Updates in your project, you can find [additional instructions on how to do so here.](/eas-update/getting-started)

You can now view and load EAS Updates in your development build via the `Extensions` panel.

## Set runtimeVersion in app config

When you create a development build of your project, you'll get a stable environment to load any changes to your app that are defined in JavaScript or other asset-related changes. Other changes to your app, whether defined directly in **android** and **ios** directories or by packages or SDKs you choose to install, will require you to create a new build of your development build.

To enforce an API contract between the JavaScript and native layers of your app, you should set the [`runtimeVersion`](/eas-update/runtime-versions) value in the app config. Each build you make will have this value embedded and will only load bundles with the same `runtimeVersion`, in both development and production.

---

---
modificationDate: July 01, 2024
title: Next steps
description: A list of useful resources to learn more about development builds and EAS Build.
---

# Next steps

A list of useful resources to learn more about development builds and EAS Build.

[Configuring EAS Build with eas.json](/build/eas-json) — Learn how a project using EAS services is configured with eas.json.

[Environment variables](/guides/environment-variables) — Learn about different ways to use environment variables in an Expo project.

[Android build process](/build-reference/android-builds) — Learn how an Android project is built on EAS Build.

[iOS build process](/build-reference/ios-builds) — Learn how an iOS project is built on EAS Build.

[Set up EAS Build with a monorepo](/build-reference/build-with-monorepos) — Learn how to set up EAS Build with a monorepo.

---

---
modificationDate: July 08, 2025
title: Introduction to config plugins
description: An introduction to Expo config plugins.
---

# Introduction to config plugins

An introduction to Expo config plugins.

When using [Continuous Native Generation (CNG)](/workflow/continuous-native-generation) in a project, native project (**android** and **ios** directories) changes are implemented without directly interacting with the native project files. Instead, you can use a config plugin to automatically configure your native project beyond what can be configured using the default app config props.

## What is a config plugin

A config plugin is a top-level custom configuration point that is not built into the [app config](/workflow/configuration). Using a config plugin, you can modify native projects created during the [prebuild](/workflow/continuous-native-generation#usage) process in CNG projects.

A config plugin is referenced in the `plugins` property of the [app config](/workflow/configuration) file and is made up of one or more plugin functions. These plugin functions are written in JavaScript and are executed during the prebuild process.

## Glossary

A typical config plugin is made up of one or more plugin functions that work together. The following diagram shows how the different parts of a config plugin interact with each other:

```
withMyPlugin ("myPlugin") [Config Plugin]
→ withAndroidPlugin, withIosPlugin [Plugin Function]
→ withAndroidManifest, withInfoPlist [Mod Plugin Function]
→ mods.android.manifest, mods.ios.infoplist [Mod]
```

In the following guides, we will use the above diagram to highlight specific terminology explained below:

### Plugin

The top-level config plugin which is referenced in your app config's `plugins` array. This is the entry point for your plugin. Conventionally, it is named `with<Plugin Name>`. For example, `withMyPlugin`. It is made of one or more [plugin functions](/config-plugins/introduction#plugin-function).

### Plugin function

One or more functions inside a config plugin that are called _plugin functions_. They wrap the underlying logic of performing platform-specific modifications. Technically, plugin functions look just like the function for the top-level plugin itself, and could be used as a plugin independently. Breaking plugins into smaller functions is often helpful for testing and debugging.

### Mod plugin function

Wrapper functions from `expo/config-plugins` library that provide a safe way to modify native files using `mods`. As a developer, you will use these functions in your config plugin instead of underlying `mods`.

### Mod

The underlying platform-specific modifiers (like `mods.android.manifest` and `mods.ios.infoplist`) that directly modify native project files during prebuild.

## Why use a config plugin

Config plugins can add native configuration to your project that isn't included by default. They can be used to generate app icons, set the app name, configure **AndroidManifest.xml** and **Info.plist**, and so on.

In CNG projects, it is best to avoid modifying these native projects manually, because you cannot regenerate them safely without potentially overwriting manual modifications. Config plugins allow you to modify these native projects in a _predictable way_ by consolidating your native project changes into a configuration file and applying them when you run `npx expo prebuild` (either manually or automatically during a CI/CD process). For example, when you change the name of your app in app config and run `npx expo prebuild`, the name will change in your native projects automatically without the need to manually update **AndroidManifest.xml** and **Info.plist** files.

## Characteristics of a config plugin

Config plugins have the following characteristics:

-   Plugins are **synchronous** functions that accept an [ExpoConfig](/workflow/configuration) and return a modified `ExpoConfig`. In rare cases, plugins can also be asynchronous if available methods to communicate with native projects are asynchronous, but they won't be performant.
-   Plugins should be named using the following convention: `with<Plugin Functionality>`, for example, `withFacebook`
-   Plugins should be synchronous and their return value should be serializable, except for adding any [`mods`](/config-plugins/introduction#mods)
-   Plugins are always evaluated during the app config evaluation phase.
-   Optionally, a second argument can be passed to the plugin to configure it
-   Mods are only evaluated during the **syncing** phase of `npx expo prebuild` (prebuild process) and modify native files during code generation. Because of that, any modifications made to app config in a config plugin should be outside of a mod to ensure that they are executed in non-prebuild configuration scenarios.

## Get started

[Create a config plugin](/config-plugins/plugins) — Comprehensive guide on how to create and use config plugins in your Expo project.

[Mods](/config-plugins/mods) — Comprehensive guide on how mods work, how to create them, and their best practices.

[Best practices for development and debugging](/config-plugins/development-and-debugging) — Learn about best practices for development and debugging config plugins.

---

---
modificationDate: September 10, 2025
title: Create and use config plugins
description: Learn how to create and use a config plugins in your Expo project.
---

# Create and use config plugins

Learn how to create and use a config plugins in your Expo project.

This guide covers sections on how to create a config plugin, how to pass parameters to a config plugin, and how to chain multiple config plugins together. It also covers how to use a config plugin from an Expo library.

Using the diagram below, in this guide, you will learn the first two parts of the config plugin hierarchy:

```
withMyPlugin ("myPlugin") [Config Plugin]
→ withAndroidPlugin, withIosPlugin [Plugin Function]
→ withAndroidManifest, withInfoPlist [Mod Plugin Function]
→ mods.android.manifest, mods.ios.infoplist [Mod]
```

> **Note:** The following sections use dynamic [app config](/workflow/configuration) (**app.config.js/app.config.ts** instead of **app.json**), which is not required to use a simple config plugin. However, it is required to use dynamic app config when you want to create/use a function-based config plugin that accepts parameters.

## Creating a config plugin

In the following section, let's create a local config plugin that adds an arbitrary property `HelloWorldMessage` to the **AndroidManifest.xml** for Android and **Info.plist** for iOS.

This example will create and modify the following files. To follow along, create a **plugins** directory in the root of your project, and inside it, create **withAndroidPlugin.ts**, **withIosPlugins.ts**, and **withPlugin.ts** files.

`plugins`

 `withAndroidPlugin.ts``Contains Android-specific modifications`

 `withIosPlugin.ts``Contains iOS-specific modifications`

 `withPlugin.ts``Main plugin file that combines both Android and iOS plugins`

`app.config.ts``Dynamic app config file that uses the plugin`

### Create Android plugin

In **withAndroidPlugin.ts**, add the following code:

```ts
import { ConfigPlugin, withAndroidManifest } from 'expo/config-plugins';

const withAndroidPlugin: ConfigPlugin = config => {
  // Define a custom message
  const message = 'Hello world, from Expo plugin!';

  return withAndroidManifest(config, config => {
    const mainApplication = config?.modResults?.manifest?.application?.[0];

    if (mainApplication) {
      // Ensure meta-data array exists
      if (!mainApplication['meta-data']) {
        mainApplication['meta-data'] = [];
      }

      // Add the custom message as a meta-data entry
      mainApplication['meta-data'].push({
        $: {
          'android:name': 'HelloWorldMessage',
          'android:value': message,
        },
      });
    }

    return config;
  });
};

export default withAndroidPlugin;
```

The example code above adds a meta-data entry `HelloWorldMessage` to the **android/app/src/main/AndroidManifest.xml** file by importing `ConfigPlugin` and `withAndroidManifest` from the `expo/config-plugins` library. The [`withAndroidManifest`](/config-plugins/mods#mod-plugins) mod plugin is an asynchronous function that accepts a config and a data object and modifies the value before returning an object.

### Create iOS plugin

In **withIosPlugin.ts**, add the following code:

```ts
import { ConfigPlugin, withInfoPlist } from 'expo/config-plugins';

const withIosPlugin: ConfigPlugin = config => {
  // Define the custom message
  const message = 'Hello world, from Expo plugin!';

  return withInfoPlist(config, config => {
    // Add the custom message to the Info.plist file
    config.modResults.HelloWorldMessage = message;
    return config;
  });
};

export default withIosPlugin;
```

The example code above adds `HelloWorldMessage` as the custom key with a custom message in **ios/<your-project-name>/Info.plist** file by importing the `ConfigPlugin` and `withInfoPlist` from the `expo/config-plugins` library. The [`withInfoPlist`](/config-plugins/mods#mod-plugins) mod plugin is an asynchronous function that accepts a config and a data object and modifies the value before returning an object.

### Create a combined plugin

Now you can create a combined plugin that applies both platform-specific plugins. This approach allows the maintenance of platform-specific code separately while providing a single entry point.

In **withPlugin.ts**, add the following code:

```ts
import { ConfigPlugin } from 'expo/config-plugins';
import withAndroidPlugin from './withAndroidPlugin';
import withIosPlugin from './withIosPlugin';

const withPlugin: ConfigPlugin = config => {
  // Apply Android modifications first
  config = withAndroidPlugin(config);
  // Then apply iOS modifications and return
  return withIosPlugin(config);
};

export default withPlugin;
```

### Add TypeScript support and convert to dynamic app config

We recommend writing config plugins in TypeScript, since this will provide intellisense for the configuration objects. However, your app config is ultimately evaluated by Node.js, which does not recognize TypeScript code by default. Therefore, you will need to add a parser for the TypeScript files from the **plugins** directory to **app.config.ts** file.

Install `tsx` library by running the following command:

```sh
npm install --save-dev tsx
```

Then, change the static app config (**app.json**) to the [dynamic app config (**app.config.ts**)](/workflow/configuration#dynamic-configuration) file. You can do this by renaming the **app.json** file to **app.config.ts** and changing the content of the file as shown below. Ensure to add the following import statement at the top of your **app.config.ts** file:

```ts
import 'tsx/cjs';

module.exports = () => {
  ... rest of your app config
};
```

### Call the config plugin from your dynamic app config

Now, you can call the config plugin from your dynamic app config. To do this, you need to add the path to the **withPlugin.ts** file to the plugins array in your app config:

```ts
import "tsx/cjs";
import { ExpoConfig } from "expo/config";

module.exports = ({ config }: { config: ExpoConfig }) => {
  ... rest of your app config
  plugins: [
      ["./plugins/withPlugin.ts"],
    ],
};
```

To see the custom config applied in native projects, run the following command:

```sh
npx expo prebuild --clean --no-install
```

To verify the custom config plugins applied, open **android/app/src/main/AndroidManifest.xml** and **ios/<your-project-name>/Info.plist** files:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
<!-- ... rest of the configuration-->
	<application ...>
		<meta-data android:name="HelloWorldMessage" android:value="Hello world, from Expo plugin!"/>
		<!-- ... -->
	</application>
</manifest>
```

```xml
<plist version="1.0">
  <dict>
  <!-- ... -->
    <key>HelloWorldMessage</key>
    <string>Hello world, from Expo plugin!</string>
	<!-- ... -->
	</dict>
</plist>
```

## Passing a parameter to a config plugin

Your config plugin can accept parameters passed from your app config. To do so, you will need to read the parameter in your config plugin function, and then pass an object containing the parameter along with the config plugin function in your app config.

Considering the previous example, let's pass a custom message to the plugin. Add an `options` object in **withAndroidPlugin.ts** and update the `message` variable to use the `options.message` property:

```ts
...
type AndroidProps = {
  message?: string;
};

const withAndroidPlugin: ConfigPlugin<AndroidProps> = (
  config,
  options = {}
) => {
  const message = options.message || 'Hello world, from Expo plugin!';
  return withAndroidManifest(config, config => {
   ... rest of the example remains unchanged
  });
};

export default withAndroidPlugin;
```

Similarly, add an `options` object in **withIosPlugin.ts** and update the `message` variable to use the `options.message` property:

```ts
...
type IosProps = {
  message?: string;
};

const withIosPlugin: ConfigPlugin<IosProps> = (config, options = {}) => {
   const message = options.message || 'Hello world, from Expo plugin!';
  ... rest of the example remains unchanged
};

export default withIosPlugin;
```

Update the **withPlugin.ts** file to pass the `options` object to both plugins:

```ts
...
const withPlugin: ConfigPlugin<{ message?: string }> = (config, options = {}) => {
  config = withAndroidPlugin(config, options);
  return withIosPlugin(config, options);
};
```

To pass a value dynamically to the plugin, you can pass an object with the `message` property to the plugin in your app config:

```ts
{
  ...
  plugins: [
    [
      "./plugins/withPlugin.ts",
      { message: "Custom message from app.config.ts" },
    ],
  ],
}
```

## Chaining config plugins

Config plugins can be chained together to apply multiple modifications. Each plugin in the chain runs in the order it appears, with the output of one plugin becoming the input for the next. This sequential execution ensures that dependencies between plugins are respected and allows you to control the precise order of modifications to your native code.

To chain config plugins, you can pass an array of plugins to the `plugins` array property in your app config. This is also supported in JSON app config file format (**app.json**).

```ts
module.exports = ({ config }: { config: ExpoConfig }) => {
  name: 'my app',
  plugins: [
    [withFoo, 'input 1'],
    [withBar, 'input 2'],
    [withDelta, 'input 3'],
  ],
};
```

The `plugins` array uses `withPlugins` method under the hood to chain the plugins. If your plugins array is getting long or has complex configuration, you can use the `withPlugins` method directly to make your configuration easier to read. `withPlugins` will chain the plugins together and execute them in order.

```ts
import { withPlugins } from 'expo/config-plugins';

// Create a base config object
const baseConfig = {
  name: 'my app',
  ... rest of the config
};

// ❌ Hard to read
withDelta(withFoo(withBar(config, 'input 1'), 'input 2'), 'input 3');

// ✅ Easy to read
withPlugins(config, [
  [withFoo, 'input 1'],
  [withBar, 'input 2'],
  // When no input is required, you can just pass the method
  withDelta,
]);

// Export the base config with plugins applied
module.exports = ({ config }: { config: ExpoConfig }) => {
  return withPlugins(baseConfig, plugins);
};
```

## Using a config plugin

Expo config plugins are usually included in Node.js modules. You can install them just like other libraries in your project.

For example, `expo-camera` has a plugin that adds camera permissions to the **AndroidManifest.xml** and **Info.plist**. To install it in your project, run the following command:

```sh
npx expo install expo-camera
```

In your [app config](/versions/latest/config/app), you can add `expo-camera` to the list of plugins:

```json
{
  "expo": {
    "plugins": ["expo-camera"]
  }
}
```

Some config plugins offer flexibility by allowing you to pass options to customize their configuration. To do this, you can pass an array with the Expo library name as the first argument, and an object containing the options as the second argument. For example, the `expo-camera` plugin allows you to customize the camera permission message:

```json
{
  "expo": {
    "plugins": [
      [
        "expo-camera",
        {
          "cameraPermission": "Allow $(PRODUCT_NAME) to access your camera."
        }
      ]
    ]
  }
}
```

> **Tip**: For every Expo library that has a config plugin, you'll find more information about that in the library's API reference. For example, the [`expo-camera` library has a config plugin section](/versions/latest/sdk/camera#configuration-in-appjsonappconfigjs).

On running the `npx expo prebuild`, the [`mods`](/config-plugins/introduction#mods) are compiled, and the native files change.

The changes don't take effect until you rebuild the native project, for example, with Xcode. **If you're using config plugins in a project without native directories (CNG projects), they will be applied during the prebuild step in EAS Build** or when running `npx expo prebuild|android|ios` locally.

---

---
modificationDate: November 20, 2025
title: Mods
description: Learn about mods and how to use them when creating a config plugin.
---

# Mods

Learn about mods and how to use them when creating a config plugin.

This guide explains what mods and mod plugins are, how they work, and how to use them effectively when creating config plugins for your Expo project.

Using the diagram below, in this guide, you will learn the last two parts of the config plugin hierarchy:

```
withMyPlugin ("myPlugin") [Config Plugin]
→ withAndroidPlugin, withIosPlugin [Plugin Function]
→ withAndroidManifest, withInfoPlist [Mod Plugin Function]
→ mods.android.manifest, mods.ios.infoplist [Mod]
```

## Mod plugins

Mod plugins provide a way to modify native project files during the prebuild process. They are made available from `expo/config-plugins` library and wrap top-level mods (also known as _default [mods](/config-plugins/mods#mods)_) because top-level mods are platform-specific and perform various tasks that can be difficult to understand at first.

> **Tip:** If you are developing a feature that requires mods, you should use _mod plugins_ instead of interacting with top-level mods directly.

### Available mod plugins

The following mod plugins are available in the `expo/config-plugins` library:

#### Android

| Default Android mod | Mod plugin | Dangerous | Description |
| --- | --- | --- | --- |
| `mods.android.manifest` | `withAndroidManifest` ([Example](https://github.com/expo/expo/blob/main/packages/expo-notifications/plugin/src/withNotificationsAndroid.ts)) | - | Modify the **android/app/src/main/AndroidManifest.xml** as JSON (parsed with [`xml2js`](https://www.npmjs.com/package/xml2js)) |
| `mods.android.strings` | `withStringsXml` ([Example](https://github.com/expo/expo/blob/d7fb5d254d5cb57ab06055136db72b9347d3db1e/packages/expo-navigation-bar/plugin/src/withNavigationBar.ts)) | - | Modify the **android/app/src/main/res/values/strings.xml** as JSON (parsed with [`xml2js`](https://www.npmjs.com/package/xml2js)). |
| `mods.android.colors` | `withAndroidColors` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/config-plugins/src/android/StatusBar.ts#L8)) | - | Modify the **android/app/src/main/res/values/colors.xml** as JSON (parsed with [`xml2js`](https://www.npmjs.com/package/xml2js)). |
| `mods.android.colorsNight` | `withAndroidColorsNight` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/prebuild-config/src/plugins/unversioned/expo-splash-screen/withAndroidSplashStyles.ts#L5)) | - | Modify the **android/app/src/main/res/values-night/colors.xml** as JSON (parsed with [`xml2js`](https://www.npmjs.com/package/xml2js)). |
| `mods.android.styles` | `withAndroidStyles` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/prebuild-config/src/plugins/unversioned/expo-splash-screen/withAndroidSplashStyles.ts#L5)) | - | Modify the **android/app/src/main/res/values/styles.xml** as JSON (parsed with [`xml2js`](https://www.npmjs.com/package/xml2js)). |
| `mods.android.gradleProperties` | `withGradleProperties` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/config-plugins/src/android/BuildProperties.ts#L5)) | - | Modify the **android/gradle.properties** as a `Properties.PropertiesItem[]`. |
| `mods.android.mainActivity` | `withMainActivity` ([Example](https://github.com/expo/expo/blob/main/packages/install-expo-modules/src/plugins/android/withAndroidModulesMainActivity.ts#L2)) |  | Modify the **android/app/src/main/<package>/MainActivity.java** as a string. |
| `mods.android.mainApplication` | `withMainApplication` ([Example](https://github.com/expo/expo/blob/main/packages/expo-web-browser/plugin/src/withWebBrowserAndroid.ts#L8)) |  | Modify the **android/app/src/main/<package>/MainApplication.java** as a string. |
| `mods.android.appBuildGradle` | `withAppBuildGradle` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/config-plugins/src/android/GoogleServices.ts#L5)) |  | Modify the **android/app/build.gradle** as a string. |
| `mods.android.projectBuildGradle` | `withProjectBuildGradle` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/config-plugins/src/android/GoogleServices.ts#L5)) |  | Modify the **android/build.gradle** as a string. |
| `mods.android.settingsGradle` | `withSettingsGradle` ([Example](https://github.com/expo/expo/blob/main/packages/install-expo-modules/src/plugins/android/withAndroidSettingsGradle.ts#L2)) |  | Modify the **android/settings.gradle** as a string. |

#### iOS

| Default iOS mod | Mod plugin | Dangerous | Description |
| --- | --- | --- | --- |
| `mods.ios.infoPlist` | `withInfoPlist` ([Example](https://github.com/expo/expo/blob/main/packages/expo-location/plugin/src/withLocation.ts)) | - | Modify the **ios/<name>/Info.plist** as JSON (parsed with [`@expo/plist`](https://www.npmjs.com/package/@expo/plist)). |
| `mods.ios.entitlements` | `withEntitlementsPlist` ([Example](https://github.com/expo/expo/blob/main/packages/expo-apple-authentication/plugin/src/withAppleAuthIOS.ts)) | - | Modify the **ios/<name>/<product-name>.entitlements** as JSON (parsed with [`@expo/plist`](https://www.npmjs.com/package/@expo/plist)). |
| `mods.ios.expoPlist` | `withExpoPlist` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/config-plugins/src/ios/Updates.ts#L6)) | - | Modify the **ios/<name>/Expo.plist** as JSON (Expo updates config for iOS) (parsed with [`@expo/plist`](https://www.npmjs.com/package/@expo/plist)). |
| `mods.ios.xcodeproj` | `withXcodeProject` ([Example](https://github.com/expo/expo/blob/main/packages/expo-asset/plugin/src/withAssetsIos.ts)) | - | Modify the **ios/<name>.xcodeproj** as an `XcodeProject` object (parsed with [`xcode`](https://www.npmjs.com/package/xcode)). |
| `mods.ios.podfile` | `withPodfile` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/config-plugins/src/ios/Maps.ts#L6) | - | Modify the **ios/Podfile** as a string. |
| `mods.ios.podfileProperties` | `withPodfileProperties` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/config-plugins/src/ios/BuildProperties.ts#L4)) | - | Modify the **ios/Podfile.properties.json** as JSON. |
| `mods.ios.appDelegate` | `withAppDelegate` ([Example](https://github.com/expo/expo/blob/main/packages/%40expo/config-plugins/src/ios/Maps.ts#L6)) |  | Modify the **ios/<name>/AppDelegate.m** as a string. |

> **Note about default Android and iOS mods:**
> Default mods are provided by the mod compiler for common file manipulation. Dangerous modifications rely on regular expressions (regex) to modify application code, which may cause the build to break. Regex mods are also difficult to version, and therefore should be used sparingly. Always opt toward using application code to modify application code, that is, [Expo Modules](https://github.com/expo/expo/tree/main/packages/expo-modules-core) native API.

## Mods

Config plugins use **mods** (short for modifiers) to modify native project files during the prebuild process. Mods are asynchronous functions that allow you to make changes to platform-specific files such as **AndroidManifest.xml** and **Info.plist**, and other native configuration files without having to manually edit them. They execute only during the **syncing** phase of `npx expo prebuild` (prebuild process).

They accept a config and a data object, then modify and return both of them as a single object. For example, in native projects, `mods.android.manifest` modifies **AndroidManifest.xml** and `mods.ios.plist` modifies **Info.plist**.

**You don't use mods as top-level functions (for example `with.android.manifest`) directly in your config plugin.** When you need to use a mod, you use _mod plugins_ in your config plugins. These mod plugins are provided by the `expo/config-plugins` library and wrap top-level mod functions and behind the scenes they perform various tasks. To see a list of available mods, check out the [mod plugins provided by `expo/config-plugins`](/config-plugins/mods#available-mod-plugins).

How default mods work and their key characteristics

When a default mod resolves, it is added to the `mods` object of the app config. This `mods` object is different from the rest of the app config because it doesn't get serialized, which means you can use it to perform actions _during_ code generation. Whenever possible, you should use available mod plugins instead of default mods since they are easier to work with.

Here is a high-level overview of how default mods work:

-   The config is read using [`getPrebuildConfig`](https://github.com/expo/expo/blob/efc2db4eb1c909544e28792a15c89f8d22113c5b/packages/%40expo/prebuild-config/src/getPrebuildConfig.ts#L28) from `@expo/prebuild-config`
-   All of the core functionality supported by Expo is added via plugins in `withIosExpoPlugins`. This includes name, version, icons, locales, and so on.
-   The config is passed to the compiler `compileModsAsync`
-   The compiler adds base mods that are responsible for reading data (like **Info.plist**), executing a named mod (like `mods.ios.infoPlist`), then writing the results to the file system
-   The compiler iterates over all the mods and asynchronously evaluates them, providing some base props like the `projectRoot`
    -   After each mod, error handling asserts if the mod chain was corrupted by an invalid mod

Here are some key characteristics of default mods:

-   `mods` are omitted from the manifest and **cannot** be accessed via `Updates.manifest`. Mods exist for the sole purpose of modifying native project files during code generation!

-   `mods` can be used to read and write files safely during the `npx expo prebuild` command. This is how Expo CLI modifies the **Info.plist**, entitlements, xcproj, and so on.

-   `mods` are platform-specific and should always be added to a platform-specific object:

    ```ts
    module.exports = {
      name: 'my-app',
      mods: {
        ios: {
          /* iOS mods... */
        },
        android: {
          /* Android mods... */
        },
      },
    };
    ```


After mods are resolved, the contents of each mod will be written to disk. Custom mods can be added to support new native files. For example, you can create a mod to support the **GoogleServices-Info.plist**, and pass it to other mods.

### How mod plugins work

When a mod plugin is executed, it gets passed a `config` object with additional properties: `modResults` and `modRequest`.

#### `modResults`

The `modResults` object contains the data to modify and return. Its type depends on the mod that's being used.

#### `modRequest`

The `modRequest` object contains the following additional properties supplied by the mod compiler.

| Property | Type | Description |
| --- | --- | --- |
| `projectRoot` | `string` | Project root directory for the universal app. |
| `platformProjectRoot` | `string` | Project root for the specific platform. |
| `modName` | `string` | Name of the mod. |
| `platform` | `ModPlatform` | Name of the platform used in the mods config. |
| `projectName` | `string` | (iOS only) The path component used for querying project files. For example, `projectRoot/ios/[projectName]/`. |

## Create your own mod

For example, if you want to write a mod to update the Xcode Project's "product name", you'll create a config plugin file that uses the [`withXcodeProject`](/config-plugins/mods#ios) mod plugin.

```ts
import { ConfigPlugin, withXcodeProject, IOSConfig } from 'expo/config-plugins';

const withCustomProductName: ConfigPlugin<string> = (config, customName) => {
  return withXcodeProject(
    config,
    async (
      config
    ) => {
      config.modResults = IOSConfig.Name.setProductName({ name: customName }, config.modResults);
      return config;
    }
  );
};

// Usage:

/// Create a config
const config = {
  name: 'my app',
};

/// Use the plugin
export default withCustomProductName(config, 'new_name');
```

## Plugin module resolution

When implementing plugins, there are two fundamental approaches to consider:

1.  **Plugins defined within your app's project**: These plugins live locally within your project, making them easy to customize and maintain alongside your app's code. They are ideal for project-specific customizations.

2.  **Standalone package plugins**: These plugins exist as separate packages and are published to npm. This approach is ideal for reusable plugins that can be shared across multiple projects.


Both approaches provide the same capabilities for modifying your native configuration, but differ in how they're structured and imported. The sections below explain how module resolution works for each approach.

> Any resolution pattern that isn't specified below is unexpected behavior, and subject to breaking changes.

### Plugins defined within your app's project

With plugins defined within your app's project, you can implement plugins directly in your project in several ways:

#### File import

You can quickly create a plugin in your project by creating a JavaScript/TypeScript file and use it in your config like any other JS/TS file.

`app.config.ts``` `import "./my-config-plugin"` ``

`my-config-plugin.ts``✓ Imported from config`

In the above example, the config plugin file contains a bare minimum function:

```ts
module.exports = ({ config }: { config: ExpoConfig }) => {};
```

#### Inline function inside of dynamic app config

Expo config objects also support passing functions as-is to the `plugins` array. This is useful for testing, or if you want to use a plugin without creating a file.

```js
const withCustom = (config, props) => config;

const config = {
  plugins: [
    [
      withCustom,
      {
        /* props */
      },
    ],
    withCustom,
  ],
};
```

One caveat to using functions instead of strings is that serialization will replace the function with the function's name. This keeps **manifests** (kind of like the **index.html** for your app) working as expected. Here is what the serialized config would look like:

```json
{
  "plugins": [["withCustom", {}], "withCustom"]
}
```

### Standalone package plugins

> See [Create a module with a config plugin](/modules/config-plugin-and-native-module-tutorial) for a step-by-step guide on how to create a standalone package plugin.

Standalone package plugins can be implemented in two ways:

#### 1\. Dedicated config plugin packages

These are npm packages whose sole purpose is to provide a config plugin. For a dedicated config plugin package, you can export your plugin using `app.plugin.js`:

`app.config.ts``` `import "expo-splash-screen"` ``

`node_modules`

 `expo-splash-screen``Node module`

  `app.plugin.js``✓ Entry file for custom plugins`

  `build`

   `index.js``` ✗ Skipped in favor of `app.plugin.js` ``

#### 2\. Config plugins with companion packages

When a config plugin is part of a Node module without an **app.plugin.js**, it uses the package's `main` entry point:

`app.config.ts``` `import "expo-splash-screen"` ``

`node_modules`

 `expo-splash-screen``Node module`

  `package.json``` `"main": "./build/index.js"` ``

  `build`

   `index.js``✓ Node resolve to this file`

### Plugin resolution order

When you import a plugin package, files are resolved in this specific order:

1.  **app.plugin.js in package root**

`app.config.ts``` `import "expo-splash-screen"` ``

`node_modules`

 `expo-splash-screen``Node module`

  `package.json``` `"main": "./build/index.js"` ``

  `app.plugin.js``✓ Entry file for custom plugins`

  `build`

   `index.js``✗ Skipped in favor of app.plugin.js`

2.  **Package's main entry (from package.json)**

`app.config.ts``` `import "expo-splash-screen"` ``

`node_modules`

 `expo-splash-screen``Node module`

  `package.json``` `"main": "./build/index.js"` ``

  `build`

   `index.js``✓ Node resolve to this file`

3.  **Direct internal imports** (not recommended)

> Avoid importing module internals directly as it bypasses the standard resolution order and may break in future updates.

`app.config.ts``` `import "expo-splash-screen/build/index.js"` ``

`node_modules`

 `expo-splash-screen`

  `package.json``` `"main": "./build/index.js"` ``

  `app.plugin.js``✗ Ignored due to direct import`

  `build`

   `index.js``` ✓ `expo-splash-screen/build/index.js` ``

### Why use app.plugin.js for plugins

The `app.plugin.js` approach is preferred for config plugins as it allows different transpilation settings from the main package code. This is particularly important because Node environments often require different transpilation presets compared to Android, iOS, or web JS environments (for example, `module.exports` instead of `import/export`).

---

---
modificationDate: July 16, 2025
title: Using a dangerous mod
description: Learn about dangerous mods and how to use them when creating a config plugin.
---

# Using a dangerous mod

Learn about dangerous mods and how to use them when creating a config plugin.

Dangerous mods in Expo provide direct access to native project files through string manipulation and regular expressions. While [existing mod plugins](/config-plugins/mods) are the recommended approach, dangerous mods serve as an escape hatch for modifications that cannot be achieved through existing mod plugins.

Why are they considered dangerous?

Automated direct source code manipulation does not typically compose well. For example, if a dangerous mod replaces text in a source file, and a subsequent dangerous mod expects the original text to be there (perhaps it uses the original text as an anchor for a regular expression) then it is unlikely produce the desired result — depending on how it is written, it may either throw an error or log. Other types of mods are less prone to this type of problem, although it can happen with mods that manipulate source files directly like `withAndroidManifest` and `withPodfile`.

Unlike standard mods, which can run multiple times safely, dangerous mods are rarely guaranteed to be idempotent. Running the same dangerous mod multiple times may produce different results, cause duplicate modifications, or break the target file entirely.

## When to use a dangerous mod

Consider using a dangerous mod when:

-   **Can't make the modification with a standard mod**: The modification you need isn't supported by existing mod plugins like [`withAndroidManifest`](/config-plugins/mods#android), [`withPodfile`](/config-plugins/mods#ios), and so on, or if a library requires specific native modifications that aren't covered by standard plugins.
-   **Legacy Expo SDK compatibility:** You are targeting an older Expo SDK version that doesn't include the mod plugin you need.
-   **Need to modify text with regexes or replace functions**: You need to perform intricate text manipulations that existing mod plugins do not support. Expo uses dangerous mods internally for large file system refactoring, for example, when a library's name changes.

## How to use a dangerous mod

In a real-world scenario, you can use the example config plugin described in this section directly in your project by following the standard config plugin usage pattern from the [Creating a config plugin section](/config-plugins/plugins#creating-a-config-plugin). However, with the existing mod plugin called [`withPodfile`](/config-plugins/mods#ios), you don't have to use the dangerous mod. The example below is just for demonstration of how a dangerous mod can be created and used.

Let's take a look at an example config plugin to modify a file inside a native directory (**ios**). This is useful when you are using Continuous Native Generation in your Expo project. With the help of this config plugin, the native file (**ios/Podfile**) will update anytime the `npx expo prebuild` command runs, whether you run it manually or using EAS Build). This example is an ideal use case when an existing mod plugin cannot edit and update a file inside a native directory.

Following the directory structure and steps to create a config plugin (steps 3, 4, and 5) from [Creating a config plugin section](/config-plugins/plugins#creating-a-config-plugin), let's assume this config plugin is created inside the **plugins** directory of your Expo project:

```tsx
import { ConfigPlugin, IOSConfig, withDangerousMod } from 'expo/config-plugins';
import fs from 'fs/promises';
import path from 'path';

const withCustomPodfile: ConfigPlugin = config => {
  return withDangerousMod(config, [
    'ios',
    async config => {
      const podfilePath = path.join(config.modRequest.platformProjectRoot, 'Podfile');

      try {
        let contents = await fs.readFile(podfilePath, 'utf8');
        const projectName = IOSConfig.XcodeUtils.getProjectName(config.modRequest.projectRoot);

        contents = addCustomPod(contents, projectName);
        await fs.writeFile(podfilePath, contents);

        console.log('✅ Successfully added custom pod to Podfile');
      } catch (error) {
        console.warn('⚠️ Podfile not found, skipping modification');
      }

      return config;
    },
  ]);
};

function addCustomPod(contents: string, projectName: string): string {
  if (contents.includes("pod 'Alamofire'")) {
    console.log('Alamofire pod already exists, skipping');
    return contents;
  }

  const targetRegex = new RegExp(
    `(target ['"]${projectName}['"] do[\\s\\S]*?use_expo_modules!)`,
    'm'
  );

  return contents.replace(targetRegex, `$1\n  pod 'Alamofire', '~> 5.6'`);
}

export default withCustomPodfile;
```

In the example above, the plugin **withCustomPodfile** will add a CocoaPod dependency automatically to your project's native **ios/Podfile** during the prebuild process. It uses `withDangerousMod` to provide access to the native file system directly and run after the native project is generated, but before any CocoaPod dependency is installed.

The **Podfile** requires direct text manipulation, which is done using a regex pattern inside `addCustomMod` function. This process also requires that the CocoaPod dependency is inserted into the **Podfile** at a specific location, which is after the `use_expo_modules!` statement.

## `withDangerousMod` syntax and requirements

Using `withDangerousMod` requires certain parameters:

1.  A native platform (**android** or **ios**)
2.  An asynchronous function that receives `config` object with file system access
3.  Relative file name/path to access inside the native directory
4.  Reading the existing file, modifying its contents, and writing back to the file
5.  (Optional) Log custom messages for success and failure state when a plugin executes during the prebuild process

The code snippet below provides a skeleton of the required field and how the config plugin can be structured when using `withDangerousMod`:

```tsx
import { ConfigPlugin, withDangerousMod } from 'expo/config-plugins';
import fs from 'fs/promises';
import path from 'path';

const myPlugin: ConfigPlugin = config => {
  return withDangerousMod(config, [
    'platform', // 1. "ios" | "android"
    async config => {
      // 2. Async modification function
      // 3. Build file paths
      const filePath = path.join(
        config.modRequest.platformProjectRoot, // Native project root
        'path/to/file' // Relative path to target file
      );

      try {
        // 4. Read existing file, modify its contents, and write back to the file
        let contents = await fs.readFile(filePath, 'utf8');
        contents = modifyContents(contents);
        await fs.writeFile(filePath, contents);

        // 5. Log success and failure states
        console.log('✅ Successfully modified file');
      } catch (error) {
        console.warn('⚠️ File modification failed:', error);
      }

      return config;
    },
  ]);
};

// Helper functions to use regex to modify the contents of the file
```

### Available paths in config plugins

Different path properties available in config plugins:

| Path | Type | Description |
| --- | --- | --- |
| `config.modRequest.projectRoot` | `string` | Universal app project root directory where **package.json** is located. Used for resolving assets, reading **package.json**, and cross-platform operations. Always verify the directory exists and contains **package.json**. |
| `config.modRequest.platformProjectRoot` | `string` | Platform-specific project root (**projectRoot/android** or **projectRoot/ios**). Used for platform-specific file operations like modifying native configuration files. Ensure the platform directory exists relative to main `projectRoot`. |
| `config.modRequest.projectName` | `string` | [iOS only] Project name component for constructing iOS file paths (for example, **projectRoot/ios/[projectName]/**). Used for iOS-specific file path construction. Only available on iOS platform and should match the actual Xcode project structure. |
| `config.modRequest.introspect` | `boolean` | Whether running in introspection mode where no filesystem changes should be made. When `true`, mods should only read and analyze files without writing. Used during config analysis and validation. |
| `config.modRequest.ignoreExistingNativeFiles` | `boolean` | Whether to ignore existing native files. Used in template-based operations, particularly affects entitlements and other native configs to ensure alignment with prebuild expectations. |

## Considerations when using a dangerous mod

When using a dangerous mod, consider the following:

-   **Limited idempotency guarantees.** Unlike standard mods, which are generally idempotent and can work without the clean flag, dangerous mods are **rarely guaranteed to be idempotent**. This means running the same dangerous mod multiple times may produce different results or cause issues.
-   **Experimental and prone to breakage.** Be careful using `withDangerousMod` as it is subject to change in the future. Test your dangerous mods thoroughly with each SDK release, as they are especially prone to breakage when native template changes occur.
-   **Use standard mod plugins**. Both Android and iOS offer mod plugins like `withAndroidManifest`, `withPodfile`, `withPodfileProperties`, and so on, to perform common native file modifications. Only use a dangerous mod when there are no [existing mod plugins available](/config-plugins/mods#available-mod-plugins) to handle your use case.
-   **Don't assume a file exists**. Always check the native directory and the relative path to the file before reading/writing to it. If you use CNG, you can always run `npx expo prebuild` to create native **android** and **ios** directories and manually verify a file's existence.
-   **Dangerous mods run first**. The order in which dangerous mods execute might be unreliable since dangerous mods run before other modifiers. This can affect the predictability of your build process and may cause conflicts with other modifications.

---

---
modificationDate: September 11, 2025
title: Plugin development for libraries
description: Learn how to develop config plugins for Expo and React Native libraries.
---

# Plugin development for libraries

Learn how to develop config plugins for Expo and React Native libraries.

Expo config plugins in a React Native library represent a transformative approach to automating native project configuration. Rather than requiring library users to manually edit native files, such as **AndroidManifest.xml**, **Info.plist**, and so on, you can provide a plugin that handles these configurations automatically during the prebuild process. This changes developer experience from error-prone manual setup to reliable, automated configuration that can work consistently across different projects.

This guide explains key configuration steps and strategies that you can use to implement a config plugin in your library.

## Strategic value of a config plugin in a library

Config plugins tend to solve interconnected problems that have historically made React Native library adoption more difficult than it should be. At times, when a user installs a React Native library, they face a complex set of native configuration steps that must be performed correctly for the library to function. These steps are platform-specific and sometimes require deep knowledge of native development concepts.

By creating a config plugin within your library, you can transform this complex-looking manual process into a simple configuration declaration that a user can apply in their Expo project's app config file (usually, **app.json**). This reduces the barrier to adoption for your library and simultaneously makes the setup process reliable.

Beyond immediate user experience improvements, config plugins enable compatibility with [Continuous Native Generation](/workflow/continuous-native-generation), where native directories are generated automatically rather than checked into version control. Without a config plugin, developers who have adopted CNG face a difficult choice: either abandon the CNG workflow to manually configure native files, or invest significant effort in creating their own automation solutions. This creates a substantial barrier to library adoption in modern Expo development workflows.

## Project structure

A directory structure is the foundation for maintaining config plugins within your library. Below is an example directory structure:

`.`

 `android``Android native module code`

  `src`

   `main`

    `java`

     `com`

      `your-awesome-library`

  `build.gradle`

 `ios``iOS native module code`

  `YourAwesomeLibrary`

  `YourAwesomeLibrary.podspec`

 `src`

  `index.ts``Main library entry point`

  `YourAwesomeLibrary.ts``Core library implementation`

  `types.ts``TypeScript type definitions`

 `plugin`

  `src`

   `index.ts``Plugin entry point`

   `withAndroid.ts``Android-specific configurations`

   `withIos.ts``iOS-specific configurations`

  `build`

  `__tests__`

  `tsconfig.json``Plugin-specific TypeScript config`

 `example`

  `app.json``Example app configuration`

  `App.tsx``Example app implementation`

  `package.json``Example app dependencies`

 `__tests__`

 `app.plugin.js``Plugin entry point for Expo CLI`

 `package.json``Package configuration`

 `tsconfig.json``Main TypeScript configuration`

 `jest.config.js``Testing configuration`

 `README.md``Documentation`

The directory structure example above highlights the following organizational principles:

-   **Root-level separation**: Clear boundaries between library code (**src**) and plugin implementation (**plugin**)
-   **Plugin directory organization**: Platform-specific files (**withAndroid.ts**, **withIos.ts**) enable focused testing and maintenance
-   **Build output management**: Compiled JavaScript and TypeScript declarations in **plugins/build/** directory
-   **Testing**: Separate plugin tests from library tests to reflect different concerns.

## Installation and configuration for development

The most straightforward approach to leverage Expo's tooling is to use `expo` and [`expo-module-scripts`](https://www.npmjs.com/package/expo-module-scripts).

-   `expo` provides a config plugin API and types that your plugin will use.
-   `expo-module-scripts` provides build tooling specifically designed for Expo modules and config plugins. It also handles TypeScript compilation.

```sh
npx expo install package
```

When using `expo-module-scripts`, it requires the following **package.json** configuration. For any already existing script with the same script name, replace it.

```json
{
  "scripts": {
    "build": "expo-module build",
    "build:plugin": "expo-module build plugin",
    "clean": "expo-module clean",
    "test": "expo-module test",
    "prepare": "expo-module prepare",
    "prepublishOnly": "expo-module prepublishOnly"
  },
  "devDependencies": {
    "expo": "^54.0.0"
  },
  "peerDependencies": {
    "expo": ">=54.0.0"
  },
  "peerDependenciesMeta": {
    "expo": {
      "optional": true
    }
  }
}
```

The next step is to add TypeScript support within the **plugins** directory. Open **plugins/tsconfig.json** file and add the following:

```json
{
  "extends": "expo-module-scripts/tsconfig.plugin",
  "compilerOptions": {
    "outDir": "build",
    "rootDir": "src"
  },
  "include": ["./src"],
  "exclude": ["**/__mocks__/*", "**/__tests__/*"]
}
```

You also need to define the main entry point for your config plugin in the **app.plugin.js** file, which exports the compiled plugin code from the **plugin/build** directory:

```js
module.exports = require('./plugin/build');
```

The above configuration is essential because when the Expo CLI looks for a plugin, it checks for this file in the project root of your library. The **plugin/build** directory contains the JavaScript files generated from your config plugin's TypeScript source code.

## Key implementation patterns

Essential patterns for a successful config plugin implementation include:

-   **Plugin structure**: Core patterns that every plugin should follow
-   **Platform-specific implementations**: Handle Android and iOS configurations effectively
-   **Test strategies:** Validating your plugin code through testing

### Plugin structure and platform-specific implementation

Every config plugin follows the same pattern: receives configuration and parameters, applies transformations through mods, and returns the modified configuration. Consider the following core plugin structure looks like:

```ts
import { type ConfigPlugin, withAndroidManifest, withInfoPlist } from 'expo/config-plugins';

export interface YourLibraryPluginProps {
  customProperty?: string;
  enableFeature?: boolean;
}

const withYourLibrary: ConfigPlugin<YourLibraryPluginProps> = (config, props = {}) => {
  // Apply Android configurations
  config = withAndroidConfiguration(config, props);

  // Apply iOS configurations
  config = withIosConfiguration(config, props);

  return config;
};

export default withYourLibrary;
```

### Testing strategies

Config plugin testing differs from regular library testing because you are testing configuration transformations rather than runtime behavior. Your plugin receives configuration objects and returns modified configuration objects.

Effective testing for a config plugin can be a combination of one or more of the following:

-   **Unit testing:** Test configuration transformation logic with mocked Expo configuration objects
-   **Cross-platform validation**: Use an example app to verify the actual prebuild output
-   **Error condition testing**: Use error handling

Since unit tests focus on a plugin's transformation logic without involving the file system, you can use Jest to create and run mock configuration objects, pass them through your plugin, and verify expected modifications are made correctly. For example:

```ts
import { withYourLibrary } from '../src';

describe('withYourLibrary', () => {
  it('should configure Android with custom property', () => {
    const config = {
      name: 'test-app',
      slug: 'test-app',
      platforms: ['android', 'ios'],
    };

    const result = withYourLibrary(config, {
      customProperty: 'test-value',
    });

    // Verify the plugin was applied correctly
    expect(result.plugins).toBeDefined();
  });
});
```

Errors should be handled gracefully inside your config plugin to provide clear feedback when a configuration fails. Use `try-catch` blocks to intercept errors early:

```ts
const withYourLibrary: ConfigPlugin<YourLibraryPluginProps> = (config, props = {}) => {
  try {
    // Validate configuration early
    validateProps(props);

    // Apply configurations
    config = withAndroidConfiguration(config, props);
    config = withIosConfiguration(config, props);

    return config;
  } catch (error) {
    // Re-throw with more context if needed
    throw new Error(`Failed to configure YourLibrary plugin: ${error.message}`);
  }
};
```

## Alternative build approaches

If your library doesn't use `expo-module-scripts`, you have two options:

### Add a plugin to your main package

For libraries using different build tools (like those created with `create-react-native-library`), add an **app.plugin.js** file and build it along with your main package:

```js
module.exports = require('./lib/plugin');
```

### Create a separate plugin package

Some libraries distribute their config plugin as a separate package from their main library. This approach allows you to maintain your config plugin separately from the rest of your native module. You need to include export in **app.plugin.js** and compile the **build** directory from your plugin.

```js
{
  "name": "your-library-expo-plugin",
  "main": "app.plugin.js",
  "files": ["app.plugin.js", "build/"],
  "peerDependencies": {
    "expo": "*",
    "your-library": "*"
  }
}
```

## Plugin development best practices

-   **Instructions in your README**: If the plugin is tied to a React Native module, then you should document manual setup instructions for the package. If anything goes wrong with the plugin, developers should be able to manually add the project modifications that were automated by the plugin. This also allows you to support projects that are not using [CNG](/workflow/continuous-native-generation).
    -   Document the available properties for the plugin, specifying if any of the properties are required.
    -   If possible, plugins should be idempotent, meaning the changes they make are the same whether they are run on a fresh native project template or run again on a project template where its changes already exist. This allows developers to run `npx expo prebuild` without the `--clean` flag to sync changes to the config, rather than recreating the native project entirely. This may be more difficult with dangerous mods.
-   **Naming conventions**: Use `withFeatureName` for the plugin function name if it applies to all platforms. If the plugin is platform-specific, use a camel case naming with the platform right after "with". For example, `withAndroidSplash`, `withIosSplash`.
-   **Leverage built-in plugins**: If there's already a configuration available in [app config](/versions/latest/config/app) and [prebuild config](https://github.com/expo/expo/blob/main/packages/%40expo/prebuild-config/src/plugins/withDefaultPlugins.ts), you don't need to write a config plugin for it.
-   **Split up plugins by platform**: When using functions within the config plugin, split them by platform. For example, `withAndroidSplash`, `withIosSplash`. This makes using the `--platform` flag in `npx expo prebuild` a bit easier to follow in `EXPO_DEBUG` mode, as the logging will show which platform-specific functions are being executed.
-   **Unit test your plugin**: Write Jest tests for complex modifications. If your plugin requires access to the filesystem, use a mock system (we strongly recommend [`memfs`](https://www.npmjs.com/package/memfs)), you can see examples of this in the [`expo-notifications`](https://github.com/expo/expo/blob/fc3fb2e81ad3a62332fa1ba6956c1df1c3186464/packages/expo-notifications/plugin/src/__tests__/withNotificationsAndroid-test.ts#L34) plugin tests.
    -   Notice the root [\*\*/__mocks__/\*\*/\*](https://github.com/expo/expo/tree/main/packages/expo-notifications/plugin/__mocks__) directory and [**plugin/jest.config.js**](https://github.com/expo/expo/tree/main/packages/expo-notifications/plugin/jest.config.js).
-   A TypeScript plugin is always preferable to a JavaScript due to added type-safety. Check out the [`expo-module-scripts` plugin](https://github.com/expo/expo/tree/main/packages/expo-module-scripts#-config-plugin) tooling for more info.
-   Do not modify the `sdkVersion` via a config plugin, this can break commands like `expo install` and cause other unexpected issues.

---

---
modificationDate: September 11, 2025
title: Developing and debugging a plugin
description: Learn about development best practices and debugging techniques for Expo config plugins.
---

# Developing and debugging a plugin

Learn about development best practices and debugging techniques for Expo config plugins.

Developing a plugin is a great way to extend the Expo ecosystem. However, there are times you'll want to debug your plugin. This page provides some of the best practices for developing and debugging a plugin.

## Plugin development

> Use [modifier previews](https://github.com/expo/vscode-expo#expo-preview-modifier) to debug the results of your plugin live.

To make plugin development easier, we've added plugin support to [`expo-module-scripts`](https://www.npmjs.com/package/expo-module-scripts). Refer to the [config plugins guide](https://github.com/expo/expo/tree/main/packages/expo-module-scripts#-config-plugin) for more info on using TypeScript, and Jest to build plugins.

### Install dependencies

Use the following dependencies in a library that provides a config plugin:

```json
{
  "dependencies": {},
  "devDependencies": {
    "expo": "^54.0.0"
  },
  "peerDependencies": {
    "expo": ">=54.0.0"
  },
  "peerDependenciesMeta": {
    "expo": {
      "optional": true
    }
  }
}
```

-   You may update the exact version of `expo` to build against a specific version.
-   For simple config plugins that depend on core, stable APIs, such as a plugin that only modifies **AndroidManifest.xml** or **Info.plist**, you can use a loose dependency such as in the example above.
-   You may also want to install [`expo-module-scripts`](https://github.com/expo/expo/blob/main/packages/expo-module-scripts/README.md) as a development dependency, but it's not required.

### Import the config plugins package

The `expo/config-plugins` and `expo/config` packages are re-exported from the `expo` package.

```js
const { ... } = require('expo/config-plugins');
const { ... } = require('expo/config');
```

Importing through the `expo` package ensures that you are using the version of the `expo/config-plugins` and `expo/config` packages that are depended on by the `expo` package.

If you do not import the package through the `expo` re-export in this way, you may accidentally be importing an incompatible version (depending on the implementation details of module hoisting in the package manager used by the developer consuming the module) or be unable to import the module at all (if using "plug and play" features of a package manager such as Yarn Berry or pnpm).

Config types are exported directly from `expo/config`, so there is no need to install or import from `expo/config-types`:

```ts
import { ExpoConfig, ConfigContext } from 'expo/config';
```

### Best practices for mods

-   Avoid regex: [static modification](/config-plugins/development-and-debugging#static-modification) is key. If you want to modify a value in an Android gradle file, consider using `gradle.properties`. If you want to modify some code in the Podfile, consider writing to JSON and having the Podfile read the static values.
-   Avoid performing long-running tasks like making network requests or installing Node modules in mods.
-   Do not add interactive terminal prompts in mods.
-   Generate, move, and delete new files in dangerous mods only. Failing to do so will break [introspection](/config-plugins/development-and-debugging#introspection).
-   Utilize built-in config plugins like `withXcodeProject` to minimize the amount of times a file is read and parsed.
-   Stick with the XML parsing libraries that prebuild uses internally, this helps prevent changes where code is rearranged needlessly.

## Plugin structure and scaffolding

### Versioning

By default, `npx expo prebuild` runs transformations on a [source template](https://github.com/expo/expo/tree/main/templates/expo-template-bare-minimum) associated with the Expo SDK version that a project is using. The SDK version is defined in the **app.json** or inferred from the installed version of `expo` that the project has.

When Expo SDK upgrades to a new version of React Native for instance, the template may change significantly to account for changes in React Native or new releases of Android or iOS.

If your plugin is mostly using [static modifications](/config-plugins/development-and-debugging#static-modification) then it will usually work well across SDK versions. If it's using a regular expression to transform application code, then you'll definitely want to document which Expo SDK version your plugin is intended for. During the SDK release cycle, there is a [beta period](https://github.com/expo/expo/blob/main/guides/releasing/Release%20Workflow.md#stage-4---beta-release) where you can test if your plugin works with the new version before it's released.

### Plugin properties

Properties are used to customize the way a plugin works during prebuild. They must always be static values (no functions, or promises). Consider the following types:

```ts
type StaticValue = boolean | number | string | null | StaticArray | StaticObject;

type StaticArray = StaticValue[];

interface StaticObject {
  [key: string]: StaticValue | undefined;
}
```

Static properties are required because the app config must be serializable to JSON for use as the app manifest.

If possible, attempt to make your plugin work without props, this will help resolution tooling like [`expo install`](/config-plugins/development-and-debugging#expo-install) or [VS Code Expo Tools](https://marketplace.visualstudio.com/items?itemName=expo.vscode-expo-tools) work better. Remember that every property you add increases complexity, making it harder to change in the future and increases the amount of features you'll need to test. Good default values are preferred over mandatory configuration when feasible.

## Development environment

### Tooling

We highly recommend installing the [Expo Tools VS Code extension](https://marketplace.visualstudio.com/items?itemName=expo.vscode-expo-tools) as this will perform automatic validation on the plugins and surface error information along with other quality of life improvements for Config Plugin development.

### Set up a playground environment

You can develop plugins easily using JS, but if you want to set up Jest tests and use TypeScript, you will want a monorepo.

A monorepo will enable you to work on a node module and import it in your app config like you would if it were published to npm. Expo config plugins have full monorepo support built-in so all you need to do is set up a project.

In your monorepo's `packages/` directory, create a module, and [bootstrap a config plugin](https://github.com/expo/expo/tree/main/packages/expo-module-scripts#-config-plugin) in it.

### Manually run a plugin

If you aren't comfortable setting up a monorepo, you can try manually running a plugin:

-   Run `npm pack` in the package with the config plugin
-   In your test project, run `npm install path/to/react-native-my-package-1.0.0.tgz`, this will add the package to your **package.json** `dependencies` object.
-   Add the package to the `plugins` array in your **app.json**: `{ "plugins": ["react-native-my-package"] }`
    -   If you have [VS Code Expo Tools](https://marketplace.visualstudio.com/items?itemName=expo.vscode-expo-tools) installed, autocomplete should work for the plugin.
-   If you need to update the package, change the `version` in the package's **package.json** and repeat the process.

## Modifying native files with plugins

### Modify AndroidManifest.xml

Packages should attempt to use the built-in **AndroidManifest.xml** [merging system](https://developer.android.com/studio/build/manage-manifests) before using a config plugin. This can be used for static, non-optional features like permissions. This will ensure features are merged during build-time and not prebuild-time, which minimizes the possibility of the configuration being missed due to users forgetting to prebuild. The drawback is that users cannot use [introspection](/config-plugins/development-and-debugging#introspection) to preview the changes and debug any potential issues.

Here is an example of a package's **AndroidManifest.xml**, which injects a required permission:

```xml
<manifest package="expo.modules.filesystem" xmlns:android="http://schemas.android.com/apk/res/android">
  <uses-permission android:name="android.permission.INTERNET"/>
</manifest>
```

If you're building a plugin for your local project, or if your package needs more control, then you should implement a plugin.

You can use built-in types and helpers to ease the process of working with complex objects. Here's an example of adding a `<meta-data android:name="..." android:value="..."/>` to the default `<application android:name=".MainApplication" />`.

```ts
import { AndroidConfig, ConfigPlugin, withAndroidManifest } from 'expo/config-plugins';
import { ExpoConfig } from 'expo/config';

// Using helpers keeps error messages unified and helps cut down on XML format changes.
const { addMetaDataItemToMainApplication, getMainApplicationOrThrow } = AndroidConfig.Manifest;

export const withMyCustomConfig: ConfigPlugin = config => {
  return withAndroidManifest(config, async config => {
    // Modifiers can be async, but try to keep them fast.
    config.modResults = await setCustomConfigAsync(config, config.modResults);
    return config;
  });
};

// Splitting this function out of the mod makes it easier to test.
async function setCustomConfigAsync(
  config: Pick<ExpoConfig, 'android'>,
  androidManifest: AndroidConfig.Manifest.AndroidManifest
): Promise<AndroidConfig.Manifest.AndroidManifest> {
  const appId = 'my-app-id';
  // Get the <application /> tag and assert if it doesn't exist.
  const mainApplication = getMainApplicationOrThrow(androidManifest);

  addMetaDataItemToMainApplication(
    mainApplication,
    // value for `android:name`
    'my-app-id-key',
    // value for `android:value`
    appId
  );

  return androidManifest;
}
```

### Modify Info.plist

Using the `withInfoPlist` is a bit safer than statically modifying the `expo.ios.infoPlist` object in the **app.json** because it reads the contents of the Info.plist and merges it with the `expo.ios.infoPlist`, this means you can attempt to keep your changes from being overwritten.

Here's an example of adding a `GADApplicationIdentifier` to the **Info.plist**:

```ts
import { ConfigPlugin, withInfoPlist } from 'expo/config-plugins';

// Pass `<string>` to specify that this plugin requires a string property.
export const withCustomConfig: ConfigPlugin<string> = (config, id) => {
  return withInfoPlist(config, config => {
    config.modResults.GADApplicationIdentifier = id;
    return config;
  });
};
```

### Modify iOS Podfile

The iOS **Podfile** is the config file for CocoaPods, the dependency manager on iOS. It is similar to **package.json** for iOS. The **Podfile** is a Ruby file, which means you **cannot** safely modify it from Expo config plugins and should opt for another approach, such as [Expo Autolinking](/modules/autolinking) hooks.

We do expose one mechanism for safely interacting with the Podfile, but it's very limited. The versioned [template Podfile](https://github.com/expo/expo/tree/main/templates/expo-template-bare-minimum/ios/Podfile) is hard coded to read from a static JSON file **Podfile.properties.json**, we expose a mod (`ios.podfileProperties`, `withPodfileProperties`) to safely read and write from this file. This is used by [expo-build-properties](/versions/latest/sdk/build-properties) and to configure the JavaScript engine.

### Add plugins to `pluginHistory`

`_internal.pluginHistory` was created to prevent duplicate plugins from running while migrating from legacy UNVERSIONED plugins to versioned plugins.

```ts
import { ConfigPlugin, createRunOncePlugin } from 'expo/config-plugins';

// Keeping the name, and version in sync with it's package.
const pkg = require('my-cool-plugin/package.json');

const withMyCoolPlugin: ConfigPlugin = config => config;

// A helper method that wraps `withRunOnce` and appends items to `pluginHistory`.
export default createRunOncePlugin(
  // The plugin to guard.
  withMyCoolPlugin,
  // An identifier used to track if the plugin has already been run.
  pkg.name,
  // Optional version property, if omitted, defaults to UNVERSIONED.
  pkg.version
);
```

### Configure Android app startup

You may find that your project requires configuration to be setup before the JS engine has started. For example, in `expo-splash-screen` on Android, we need to specify the resize mode in the **MainActivity.java**'s `onCreate` method. Instead of attempting to dangerously regex these changes into the `MainActivity` via a dangerous mod, we use a system of lifecycle hooks and static settings to safely ensure the feature works across all supported Android languages (Java, Kotlin), versions of Expo, and combination of config plugins.

This system is made up of three components:

-   `ReactActivityLifecycleListeners`: An interface exposed by `expo-modules-core` to get a native callback when the project `ReactActivity`'s `onCreate` method is invoked.
-   `withStringsXml`: A mod exposed by `expo/config-plugins` which writes a property to the Android **strings.xml** file, the library can safely read the strings.xml value and do initial setup. The string XML values follow a designated format for consistency.
-   `SingletonModule` (optional): An interface exposed by `expo-modules-core` to create a shared interface between native modules and `ReactActivityLifecycleListeners`.

Consider this example: We want to set a custom "value" string to a property on the Android `Activity`, directly after the `onCreate` method was invoked. We can do this safely by creating a node module `expo-custom`, implementing `expo-modules-core`, and Expo config plugins:

First, we register the `ReactActivity` listener in our Android native module, this will only be invoked if the user has `expo-modules-core` support, setup in their project (default in projects bootstrapped with Expo CLI, Create React Native App, Ignite CLI, and Expo prebuilding).

```kotlin
package expo.modules.custom

import android.content.Context
import expo.modules.core.BasePackage
import expo.modules.core.interfaces.ReactActivityLifecycleListener

class CustomPackage : BasePackage() {
  override fun createReactActivityLifecycleListeners(activityContext: Context): List<ReactActivityLifecycleListener> {
    return listOf(CustomReactActivityLifecycleListener(activityContext))
  }

  // ...
}
```

Next we implement the `ReactActivity` listener, this is passed the `Context` and is capable of reading from the project **strings.xml** file.

```kotlin
package expo.modules.custom

import android.app.Activity
import android.content.Context
import android.os.Bundle
import android.util.Log
import expo.modules.core.interfaces.ReactActivityLifecycleListener

class CustomReactActivityLifecycleListener(activityContext: Context) : ReactActivityLifecycleListener {
  override fun onCreate(activity: Activity, savedInstanceState: Bundle?) {
    // Execute static tasks before the JS engine starts.
    // These values are defined via config plugins.

    var value = getValue(activity)
    if (value != "") {
      // Do something to the Activity that requires the static value...
    }
  }

  // Naming is node module name (`expo-custom`) plus value name (`value`) using underscores as a delimiter
  // i.e. `expo_custom_value`
  // `@expo/vector-icons` + `iconName` -> `expo__vector_icons_icon_name`
  private fun getValue(context: Context): String = context.getString(R.string.expo_custom_value).toLowerCase()
}
```

We must define default **string.xml** values which the user will overwrite locally by using the same `name` property in their **strings.xml** file.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="expo_custom_value" translatable="false"></string>
</resources>
```

At this point, bare users can configure this value by creating a string in their local **strings.xml** file (assuming they also have `expo-modules-core` support setup):

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="expo_custom_value" translatable="false">I Love Expo</string>
</resources>
```

For managed users, we can expose this functionality (safely!) via an Expo config plugin:

```js
const { AndroidConfig, withStringsXml } = require('expo/config-plugins');

function withCustom(config, value) {
  return withStringsXml(config, config => {
    config.modResults = setStrings(config.modResults, value);
    return config;
  });
}

function setStrings(strings, value) {
  // Helper to add string.xml JSON items or overwrite existing items with the same name.
  return AndroidConfig.Strings.setStringItem(
    [
      // XML represented as JSON
      // <string name="expo_custom_value" translatable="false">value</string>
      { $: { name: 'expo_custom_value', translatable: 'false' }, _: value },
    ],
    strings
  );
}
```

Managed Expo users can now interact with this API like so:

```json
{
  "expo": {
    "plugins": [["expo-custom", "I Love Expo"]]
  }
}
```

By re-running `npx expo prebuild -p` (`eas build -p android`, or `npx expo run:ios`) the user can now see the changes, safely applied in their managed project!

As you can see from the example, we rely heavily on application code (expo-modules-core) to interact with application code (the native project). This ensures that our config plugins are safe and reliable, hopefully for a very long time!

## Debugging config plugins

You can debug config plugins by running `EXPO_DEBUG=1 expo prebuild`. If `EXPO_DEBUG` is enabled, the plugin stack logs will be printed, these are useful for viewing which mods ran, and in what order they ran in. To view all static plugin resolution errors, enable `EXPO_CONFIG_PLUGIN_VERBOSE_ERRORS`, this should only be needed for plugin authors. By default, some automatic plugin errors are hidden because they're usually related to versioning issues and aren't very helpful (that is, legacy package doesn't have a config plugin yet).

Running `npx expo prebuild --clean` will remove the generated native directories before compiling.

You can also run `npx expo config --type prebuild` to print the results of the plugins with the mods unevaluated (no code is generated).

Expo CLI commands can be profiled using `EXPO_PROFILE=1`.

## Introspection

Introspection is an advanced technique used to read the evaluated results of modifiers without generating any code in the project. This can be used to quickly debug the results of [static modifications](/config-plugins/development-and-debugging#static-modification) without needing to run prebuild. You can interact with introspection live, by using the [preview feature](https://github.com/expo/vscode-expo#expo-preview-modifier) of `vscode-expo`.

You can try introspection by running `expo config --type introspect` in a project.
