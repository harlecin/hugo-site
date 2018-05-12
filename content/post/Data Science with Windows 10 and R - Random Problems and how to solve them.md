+++
date = "2018-05-12"
title = "Data Science with Windows 10 - Quick Fixes"
+++

When you work for a large corporation you often have little choice in picking a specific operating system for your company laptop. This post is a collection of random problems I ran into in the past mostly with R and Python on Windows 10 and how to resolve them. I plan to update this post over time (hopefully not often:)

Let's get started:

## R

### Installing RStudio + R without administrator privileges
This is actually pretty easy. Install R + RStudio on a laptop where you have admin privileges (e.g. your own computer) onto a USB thumb drive. Copy the files to your company laptop, launch RStudio and point it to the directory where you put R and you are set:)

### Path length limit exceeded
By default, Windows limits file path lengths to 260 characters. On Windows 10 you can:

1. Run regedit as administrator
2. Go to: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. Open: `LongPathsEnabled` and set it to 1

You might need to reboot for changes to take effect.

### Error with install.packages(): unable to move temporary installation
This is almost certainly due to your company's Antivirus taking its job a little bit to seriously and locking the files R wants to move during installation.

There is a simple fix. Run:
```
trace(utils:::unpackPkgZip, edit=TRUE)
```
And change `Sys.sleep(0.5)` to `Sys.sleep(2.5)` on line 140. Unfortunately, this is a temporary fix that is only valid for the current R session.

### Cygwin Error when using Rtools to install a package
Remove Adobe Flash player and try again. Seriously, why did you install Flash player in the first place;)?

## Python

### Activate.bat with CMD
If you plan on using Python on Windows you should probably use Anaconda Python to avoid problems when you want to install additional packages.

When you work with conda environments, please not that the `activate.bat` script currently only works with CMD and not with Powershell.

