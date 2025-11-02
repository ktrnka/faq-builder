# Context

I have an old Macbook Pro (2014, Intel-based). The hardware is still in good condition, but Apple stopped providing OS X updates. Then Chrome stopped updating for the OS version. Then Docker stopped updating for it. I even ran had incompatibility with a Python module (DuckDB) which stopped supporting it.

Ubuntu has given the machine new life! I can use it for both casual web use as well as software development. I haven't gone and wiped the OS X partition because I don't need the space but eventually I will.

The install and setup was not always straightforward and some of the guides were outdated so I wanted to write it all down for anyone else trying this.

# Freeing up space
Freeing up space took extra effort. Apparently a while back, an OS X update created an entire new partition and I either didn't realize or forgot. That was the biggest amount of space to free up. Perplexity was helpful to guide me through it.

# Trying and installing Ubuntu
The system is very picky about the USB drive. What worked:
- Formatting as MS‑DOS (FAT) with GUID Partition Map in Disk Utility (other formats run on my other computer were not recognized) [link](https://discourse.ubuntu.com/t/create-a-bootable-usb-stick-on-macos/14016)
- dd to flash the iso (steps below)
- Boot with Option held down and choose EFI Boot.


I followed [these steps](https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command/) to flash the ISO.
```
# 1) List disks and identify your USB (e.g., /dev/disk2)
/usr/sbin/diskutil list

# 2) Unmount the whole USB device (not just a partition)
/usr/sbin/diskutil unmountDisk /dev/diskN

# 3) Write the ISO to the raw device for speed (DANGER: correct N!)
sudo dd if=/path/to/ubuntu-desktop.iso of=/dev/rdiskN bs=1m

# 4) Ensure buffers are flushed, then eject
sync
/usr/sbin/diskutil eject /dev/diskN
```

The steps above were maybe the 4th attempt. On previous attempts, either the USB wasn't listed in the boot menu or else it was listed but booting from it would just hang.

Also note that there were some light visual glitches when booted from USB but those issues didn't persist after installing it to disk.

# Installing wifi drivers (Broadcom BCM4360)
Ubuntu doesn't come with wifi drivers for the Broadcom BCM4360 chip. So I ordered a cheap USB Ethernet adapter and used it to test Ubuntu when booted from USB and then later I used it again to install wifi chip drivers.

When installing Ubuntu I made sure to select additional drivers, which I think enabled the restricted package source. Some guides say you need to add that explicitly but I didn't need to.

Then: `sudo apt install broadcom-sta-dkms` (Guides suggested an older package name that didn't exist anymore `bcmwl-kernel-source`)

Then I rebooted and it just worked!

# Installing webcam drivers (Broadcom FaceTime HD / 1570)
The guides were good about this and it worked smoothly. The hardware names I saw were "FaceTime HD webcam" and "Broadcom 1570 PCIe".

- Double-check the hardware model against the guide you're following. In my case `lspci -nn | grep -i 1570`
- Install prerequisites: `sudo apt install linux-headers-generic build-essential git curl cpio xz-utils`
- Install firmware: `git clone https://github.com/patjak/facetimehd-firmware.git && cd facetimehd-firmware && make && sudo make install`
- Install driver: `git clone https://github.com/patjak/bcwc_pcie.git && cd bcwc_pcie && make && sudo make install && sudo depmod`
- Load the driver: `sudo modprobe facetimehd` and verify in a one-person video call

Sources:
- [link](https://andreafortuna.org/2024/08/24/from-faceless-to-facetime-installing-webcam-drivers-on-a-debian-powered-macbook-air)
- [link](https://gist.github.com/johnjeffers/3006011ec7767a4101cdd118e8d64290)

# Issue: Red light from the audio jack

Sometimes a red light would shine through the audio jack.

> That red light shining through your MacBook’s headphone jack is the optical digital audio (TOSLINK / S/PDIF) output, which shares the same jack as the analog output on older Mac models like the 2014 MacBook Pro. When the light turns on, it means the hardware has switched the port into optical mode.

Steps to resolve:
- Run `alsamixer`
- Press F6 to pick your sound card, navigate to S/PDIF, IEC958, or Digital Output channels, then press M to mute.
- Run `sudo alsactl store`

I haven't had problems since.

# Improving battery life
Short version: TLP works well without additional customization. My other efforts were not successful.

Initially I wanted low-effort monitoring in the top bar. That led me to PowerTracker.
- Setup Gnome extensions and install PowerTracker [link](https://www.ubuntumint.com/powertracker-ubuntu-battery-life-monitor/)
- Manually edit `~/.local/share/gnome-shell/extensions/marcs14@gmail.com/metadata.json` to allow it in Gnome 49, then relogin. This isn't normally needed, but the extension hadn't been updated when I installed Ubuntu 25.10 with Gnome 49

After baselining for a few days I installed TLP, which is a common all-in-one package to optimize battery life. I've found that battery life while sleeping seems better, and it's a little better during normal usage (compared to balanced power mode all the time). I haven't actually noticed any major trends in PowerTracker, so that may have been a poor choice for monitoring. 

```
sudo apt install tlp
sudo tlp start
```

## Failed effort: Hardware video acceleration
This hardware has Intel Iris 5100 and can do hardware acceleration of h264 video.

I spent some time trying to get hardware video acceleration working for Youtube but I wasn't able to improve battery life that way.
- Didn't get it working in Chrome (using the deb package)
- Got it working in Firefox/Flatpak BUT when I benchmarked it against Chrome, the battery usage was similar.

If you're looking for steps, I think this is what worked:
`sudo apt install vainfo libva-intel-driver`

Then I could confirm that it saw the i965 chip with `vainfo`:

    libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/i965_drv_video.so
    libva info: Found init function __vaDriverInit_1_22
    libva info: va_openDriver() returns 0
    vainfo: VA-API version: 1.22 (libva 2.22.0)
    vainfo: Driver version: Intel i965 driver for Intel(R) Haswell - 2.4.1

Firefox setup:
```
flatpak install flathub org.mozilla.firefox
flatpak run org.mozilla.firefox
```

Then run `flatpak info org.mozilla.firefox` and note the version number under runtime or SDK. In my case it's 24.08.

I also had to install these:
```
flatpak install flathub org.freedesktop.Platform.ffmpeg-full//VERSION
flatpak install flathub org.freedesktop.Platform.VAAPI.Intel//VERSION
```

If you don't specify the version, you can pick it from a list.

And because my hardware only accelerates h264, I installed h264ify to force Youtube to use H264 streams rather than VP9/AV1 (because only h264 is supported by i965).

Older online guides said I'd need to edit Firefox settings but that's no longer needed.

intel-gpu-top is useful for confirming that it's working. To install:
`sudo apt install intel-gpu-tools`

Then run the top ocmmand while playing a video and confirm that there's non-zero usage in the Video row:
`sudo intel_gpu_top`

## Failed effort: Battery health saver
TLP has some pointers on how to set this up with Apple silicon (M chips) but not Intel. That said, I've noticed that it tends to stop at around 95% which is good enough for me.

# Failed effort: Wake speed
On OS X, my Macbook would wake from sleep in about 1 second. On Ubuntu, it takes maybe 10 seconds.

I can see the options in here:
```
> cat /sys/power/mem_sleep
s2idle [deep]
```

Then changed it to s2idle:
```echo s2idle | sudo tee /sys/power/mem_sleep```

Sadly that drainged the battery overnight, so I'll just live with the slower waking.


