+++
date = "2020-04-05"
title = "Linux on Razer Blade 15 (mid 2019)"
+++

As a long time Macbook user I recently made the switch to a Windows laptop, specifically a Razer Blade 15 (mid 2019) model. While Apple has thankfully started to use proper keyboards again in their recent lineup, the lack of Nvidia gpus is somewhat sub-optimal if you want to use your laptop for deep learning prototyping and so here I am with a Windows computer. 

I do have to say, I quite like working with Windows 10. So far, everything worked very well, but once in a while I need Linux to run specific programs. On Windows 10, there are two major options if you want to run Linux:

1. Windows Subsystem for Linux (WSL) 2
2. Dual-Boot Linux

## WSL 2
WSL 2 is an amazing piece of engineering in my opinion. Microsoft basically allows you to install a fully functional linux kernel in Windows 10. Setting everything up and installing Ubuntu 18.04 took a couple of minutes and worked really well. The system launches almost instantly and gives you access to most everything you need from a linux system while allowing you to leverage VS Code with its remote extension to connect to WSL2 for coding. Only downside: as of now, WSL2 cannot access the gpu, so no gpu-accelerated computations unfortunately.

I decided to setup Ubuntu 18.04 in dual boot mode. I installed Lubuntu on an old laptop of mine a few years ago and the whole setup experience was not very smooth: the touchpad was poorly supported out of the box and I had to hunt down drivers quite a while. I was a bit afraid that driver support for my Razer Blade might be similary bad, but I took the jump:

## Dual Boot Ubuntu 18.04
In order to dual boot Linux, you should always install Windows first to avoid problems with the boot loader. Since W10 was already pre-installed that was not an issue.

I used [Rufus](rufus.ie) to create a bootable usb drive and downloaded Ubuntu 18.04 from Canonical. I shrank my Windows partition using disk manager to get free space for my Linux installation and disabled "Fast Startup".

> Note: Most guides recommend disabling secure boot to install Linux, but it is not strictly necessary as long as you are careful with your setup

Rebooting my laptop, I entered the Ubuntu setup wizard and everything appeared to work fine until the setup wizard crashed while I tried to create partitions. After rebooting, my laptop refused to load the install wizard with the following error message:

```
Failed to open \EFI\BOOT\mmx64.efi - Not Found
Failed to load image \EFI\BOOT\mmx64.efi: Not Fount
Failed to start MokManager: Not Found
Something has gone seriously wrong: import_mok_state() failed
: Not found
```

Sigh, ...

After googline a while, I found a post concering this error that described a fix for Asus laptops, but my BIOS does not have the options necessary to apply the fix. Thankfully, it turned out that simply going into the folder specified in the error message and renaming grub.efi to mmx64.efi does the trick as well.

Apparently this error is caused by the installer setting some variables before it finishes installing. This bug should be fixed in the latest Ubuntu version.

From this point onwards, installation went well. I chose to setup partitions manually as I read that the option to "Install Ubuntu alongside Windows" sometimes causes issues. I created a swap (16gb), root (40gb) and home partition (34gb) (all primary)  partition and finished installation without any further problems. After I booted into Ubuntu the first time, I noticed that my external monitor was not working properly. While I could see my mouse cursor apart from that everything was black. The problem is that my laptop has a dual graphic card setup and the drivers shipped with Ubuntu do not support my cards properly. When I plugged in an HDMI cable, both the primary and secondary display would go black, or only the secondary one if plugged into a DVI connection. 

Installing all recommended (but closed-source and hence not by default included) drivers fixed the issue for me. Simply run:

```
sudo ubuntu-drivers --autoinstall
```

This will install any necessary additional drivers for your machine if available.

> Note: You have to enroll your keys in Mok after restart, otherwise secure boot will not allow them to be loaded

I do have to say, Ubuntu works very well on my Razer Blade. Touchpad is very well supported as are my graphics cards now. Hibernate does not work, but apart from that I have not found any further issues so far.

Hope you found this post helpful!
